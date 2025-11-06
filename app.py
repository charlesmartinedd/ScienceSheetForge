"""
ScienceSheetForge Web Application
Modern modal-based worksheet generator with NGSS standards
"""

from flask import Flask, render_template, send_file, request, jsonify, abort
import os
import sys
import logging
import re
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename

# Add generators to path
sys.path.insert(0, os.path.dirname(__file__))

# Import new features
try:
    from pdf_export import png_to_pdf, create_worksheet_bundle_pdf
    PDF_EXPORT_AVAILABLE = True
except ImportError:
    PDF_EXPORT_AVAILABLE = False
    logger.warning("PDF export not available")

try:
    from batch_generator import batch_generate_worksheets, batch_generate_all_formats_for_standard
    BATCH_GENERATION_AVAILABLE = True
except ImportError:
    BATCH_GENERATION_AVAILABLE = False
    logger.warning("Batch generation not available")

from ngss_standards import NGSS_STANDARDS
from worksheet_formats import WORKSHEET_FORMATS

# Try to import smart generators first, fallback to regular ones
try:
    from generators.crossword_smart import generate_crossword_tpt_style as generate_crossword
    print("Using smart crossword generator")
except ImportError as e:
    from generators.crossword_generator import generate_crossword_tpt_style as generate_crossword
    print(f"Using standard crossword generator: {e}")

try:
    from generators.word_search_smart import generate_word_search
    print("Using smart word search generator")
except ImportError as e:
    from generators.word_search_generator import generate_word_search
    print(f"Using standard word search generator: {e}")

try:
    from generators.matching_smart import generate_matching
    print("Using smart matching generator")
except ImportError as e:
    from generators.matching_generator import generate_matching
    print(f"Using standard matching generator: {e}")

try:
    from generators.fill_in_blank import generate_fill_in_blank
    print("Using fill-in-blank generator")
except ImportError as e:
    print(f"Fill-in-blank generator not available: {e}")
    generate_fill_in_blank = None

try:
    from generators.short_answer import generate_short_answer
    print("Using short answer generator")
except ImportError as e:
    print(f"Short answer generator not available: {e}")
    generate_short_answer = None

try:
    from generators.true_false import generate_true_false
    print("Using true/false generator")
except ImportError as e:
    print(f"True/false generator not available: {e}")
    generate_true_false = None

FORMAT_GENERATORS = {
    'crossword': generate_crossword,
    'word-search': generate_word_search,
    'matching': generate_matching,
    'fill-blank': generate_fill_in_blank,
    'short-answer': generate_short_answer,
    'true-false': generate_true_false,
}

AVAILABLE_FORMAT_IDS = {fmt_id for fmt_id, func in FORMAT_GENERATORS.items() if callable(func)}

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'output')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
app.config['MAX_OUTPUT_FILES'] = 1000  # Maximum files to keep in output folder

# Create output directory
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sciencesheetforge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Allowed grade levels and formats for validation
ALLOWED_GRADE_LEVELS = ['K-2', '3-5', '6-8']
ALLOWED_STANDARD_PATTERN = re.compile(r'^[A-Z0-9\-]+$')  # Basic validation pattern


def verify_runtime_environment():
    """Emit warnings for missing optional runtime prerequisites."""
    try:
        from PIL import ImageFont  # pylint: disable=import-error
    except Exception as exc:  # Pillow not available should fail earlier, but be explicit.
        print("WARNING: Pillow is not installed or failed to import.", file=sys.stderr)
        print(f"         Worksheet generation will not function: {exc}", file=sys.stderr)
        return

    font_candidates = [
        "arial.ttf",
        "Arial.ttf",
        "DejaVuSans.ttf",
        "LiberationSans-Regular.ttf",
    ]

    for font_name in font_candidates:
        try:
            ImageFont.truetype(font_name, 40)
            return
        except OSError:
            continue

    print("WARNING: No common TrueType fonts were found (looked for Arial/DejaVu Sans).", file=sys.stderr)
    print("         Generated worksheets will fall back to Pillow's default bitmap font", file=sys.stderr)
    print("         which is lower quality. Install a TrueType font and restart.", file=sys.stderr)


@app.route('/')
def index():
    """Main page"""
    formats = []
    for fmt in WORKSHEET_FORMATS:
        fmt_copy = fmt.copy()
        fmt_copy['available'] = fmt['id'] in AVAILABLE_FORMAT_IDS
        formats.append(fmt_copy)

    return render_template(
        'index.html',
        worksheet_formats=formats,
        ngss_standards=NGSS_STANDARDS
    )


def validate_filename(filename):
    """Validate filename to prevent path traversal attacks"""
    if not filename:
        return False
    # Check for suspicious patterns BEFORE processing
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    # Must be a PNG file
    if not filename.endswith('.png'):
        return False
    # Must match expected pattern (alphanumeric, underscore, hyphen only)
    pattern = re.compile(r'^[\w\-]+\.png$')
    if not pattern.match(filename):
        return False
    # Additional check: basename should be same as original
    if os.path.basename(filename) != filename:
        return False
    return True


def cleanup_old_files():
    """Remove old generated files if exceeding max count"""
    try:
        output_folder = app.config['OUTPUT_FOLDER']
        files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.png')]
        if len(files) > app.config['MAX_OUTPUT_FILES']:
            # Sort by modification time
            files.sort(key=os.path.getmtime)
            # Remove oldest files
            for f in files[:len(files) - app.config['MAX_OUTPUT_FILES']]:
                try:
                    os.remove(f)
                    logger.info(f"Removed old file: {f}")
                except Exception as e:
                    logger.error(f"Failed to remove file {f}: {e}")
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")


@app.route('/generate', methods=['POST'])
def generate():
    """Generate worksheet with input validation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        grade_level = data.get('grade_level')
        standard_code = data.get('standard_code')
        worksheet_format = data.get('worksheet_format')

        # Input validation
        if not grade_level or grade_level not in ALLOWED_GRADE_LEVELS:
            return jsonify({'success': False, 'error': 'Invalid grade level'}), 400

        if not standard_code or not ALLOWED_STANDARD_PATTERN.match(standard_code):
            return jsonify({'success': False, 'error': 'Invalid standard code'}), 400

        if not worksheet_format or worksheet_format not in AVAILABLE_FORMAT_IDS:
            return jsonify({'success': False, 'error': 'Invalid worksheet format'}), 400

        # Find the standard data
        standard_data = None
        for grade in NGSS_STANDARDS:
            for std in NGSS_STANDARDS[grade]:
                if std['code'] == standard_code:
                    standard_data = std
                    break
            if standard_data:
                break

        if not standard_data:
            return jsonify({'success': False, 'error': 'Standard not found'}), 404

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = os.path.join(
            app.config['OUTPUT_FOLDER'],
            f'{worksheet_format}_{standard_code}_{timestamp}.png'
        )

        generator = FORMAT_GENERATORS.get(worksheet_format)
        if not callable(generator):
            return jsonify({
                'success': False,
                'error': f"Worksheet format '{worksheet_format}' is not available yet."
            }), 400

        generator(standard_data, grade_level, output_filename)
        logger.info(f"Generated worksheet: {worksheet_format} for {standard_code}")

        # Cleanup old files periodically
        cleanup_old_files()

        answer_key_filename = output_filename.replace('.png', '_ANSWER_KEY.png')

        return jsonify({
            'success': True,
            'worksheet': f'/view/{os.path.basename(output_filename)}',
            'answer_key': f'/view/{os.path.basename(answer_key_filename)}',
            'timestamp': timestamp,
            'worksheet_format': worksheet_format,
            'standard': standard_code
        })

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({'success': False, 'error': 'Invalid input parameters'}), 400
    except Exception as e:
        logger.error(f"Error generating worksheet: {e}", exc_info=True)
        # Don't expose internal error details in production
        return jsonify({
            'success': False,
            'error': 'An error occurred while generating the worksheet. Please try again.'
        }), 500


@app.route('/view/<filename>')
def view_file(filename):
    """View generated worksheet with security checks"""
    # Validate filename to prevent path traversal
    if not validate_filename(filename):
        logger.warning(f"Invalid filename attempt: {filename}")
        abort(400, description="Invalid filename")

    # Secure the filename
    filename = secure_filename(filename)

    # Build safe file path
    output_folder = Path(app.config['OUTPUT_FOLDER']).resolve()
    file_path = (output_folder / filename).resolve()

    # Ensure file is within output folder (prevent path traversal)
    try:
        file_path.relative_to(output_folder)
    except ValueError:
        logger.warning(f"Path traversal attempt: {filename}")
        abort(403, description="Access denied")

    if file_path.exists() and file_path.is_file():
        return send_file(str(file_path), mimetype='image/png')

    logger.info(f"File not found: {filename}")
    abort(404, description="File not found")


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated worksheet with security checks"""
    # Validate filename to prevent path traversal
    if not validate_filename(filename):
        logger.warning(f"Invalid filename attempt: {filename}")
        abort(400, description="Invalid filename")

    # Secure the filename
    filename = secure_filename(filename)

    # Build safe file path
    output_folder = Path(app.config['OUTPUT_FOLDER']).resolve()
    file_path = (output_folder / filename).resolve()

    # Ensure file is within output folder (prevent path traversal)
    try:
        file_path.relative_to(output_folder)
    except ValueError:
        logger.warning(f"Path traversal attempt: {filename}")
        abort(403, description="Access denied")

    if file_path.exists() and file_path.is_file():
        return send_file(str(file_path), as_attachment=True, download_name=filename)

    logger.info(f"File not found: {filename}")
    abort(404, description="File not found")


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'ScienceSheetForge',
        'version': '2.0.0',
        'available_formats': list(AVAILABLE_FORMAT_IDS),
        'features': {
            'pdf_export': PDF_EXPORT_AVAILABLE,
            'batch_generation': BATCH_GENERATION_AVAILABLE
        }
    })


@app.route('/api/standards')
def list_standards():
    """API endpoint to list all available NGSS standards"""
    standards_list = []
    for grade_level, standards in NGSS_STANDARDS.items():
        for std in standards:
            standards_list.append({
                'grade_level': grade_level,
                'code': std['code'],
                'title': std['title'],
                'description': std['description']
            })

    return jsonify({
        'success': True,
        'count': len(standards_list),
        'standards': standards_list
    })


@app.route('/api/formats')
def list_formats():
    """API endpoint to list all available worksheet formats"""
    formats_list = []
    for fmt in WORKSHEET_FORMATS:
        fmt_copy = fmt.copy()
        fmt_copy['available'] = fmt['id'] in AVAILABLE_FORMAT_IDS
        formats_list.append(fmt_copy)

    return jsonify({
        'success': True,
        'count': len(formats_list),
        'formats': formats_list
    })


@app.route('/api/export-pdf/<filename>')
def export_pdf(filename):
    """Export PNG worksheet to PDF format"""
    if not PDF_EXPORT_AVAILABLE:
        return jsonify({'success': False, 'error': 'PDF export not available'}), 503

    try:
        # Validate filename
        if not validate_filename(filename):
            logger.warning(f"Invalid filename for PDF export: {filename}")
            abort(400, description="Invalid filename")

        filename = secure_filename(filename)
        output_folder = Path(app.config['OUTPUT_FOLDER']).resolve()
        png_path = (output_folder / filename).resolve()

        # Security check
        try:
            png_path.relative_to(output_folder)
        except ValueError:
            abort(403, description="Access denied")

        if not png_path.exists():
            abort(404, description="PNG file not found")

        # Convert to PDF
        pdf_path = png_to_pdf(str(png_path))

        return jsonify({
            'success': True,
            'pdf_file': f'/download/{os.path.basename(pdf_path)}',
            'message': 'PDF exported successfully'
        })

    except Exception as e:
        logger.error(f"PDF export error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Failed to export PDF'
        }), 500


@app.route('/api/batch-generate', methods=['POST'])
def batch_generate():
    """Generate multiple worksheets in batch"""
    if not BATCH_GENERATION_AVAILABLE:
        return jsonify({'success': False, 'error': 'Batch generation not available'}), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        grade_level = data.get('grade_level')
        standard_codes = data.get('standard_codes', [])
        worksheet_formats = data.get('worksheet_formats', [])
        max_workers = data.get('max_workers', 4)

        # Validation
        if not grade_level or grade_level not in ALLOWED_GRADE_LEVELS:
            return jsonify({'success': False, 'error': 'Invalid grade level'}), 400

        if not standard_codes or not isinstance(standard_codes, list):
            return jsonify({'success': False, 'error': 'Invalid standard codes'}), 400

        if not worksheet_formats or not isinstance(worksheet_formats, list):
            return jsonify({'success': False, 'error': 'Invalid worksheet formats'}), 400

        # Validate all format IDs
        for fmt in worksheet_formats:
            if fmt not in AVAILABLE_FORMAT_IDS:
                return jsonify({'success': False, 'error': f'Invalid format: {fmt}'}), 400

        # Find standards
        standards_list = []
        for std_code in standard_codes:
            found = False
            for grade in NGSS_STANDARDS:
                for std in NGSS_STANDARDS[grade]:
                    if std['code'] == std_code:
                        standards_list.append(std)
                        found = True
                        break
                if found:
                    break

            if not found:
                return jsonify({'success': False, 'error': f'Standard not found: {std_code}'}), 404

        # Generate worksheets
        result = batch_generate_worksheets(
            FORMAT_GENERATORS,
            standards_list,
            grade_level,
            worksheet_formats,
            app.config['OUTPUT_FOLDER'],
            max_workers=min(max_workers, 8)  # Cap at 8 workers
        )

        logger.info(f"Batch generation completed: {result.summary()}")

        return jsonify({
            'success': True,
            'result': result.to_dict()
        })

    except Exception as e:
        logger.error(f"Batch generation error: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Batch generation failed'
        }), 500


@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:;"
    )
    return response


def main():
    """Main entry point for the application"""
    import argparse

    parser = argparse.ArgumentParser(description='ScienceSheetForge Web Application')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=3000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    print("=" * 70)
    print("SCIENCESHEETFORGE - Modern Worksheet Generator")
    print("=" * 70)
    print("\nStarting local server...")
    print(f"\nOpen your browser and go to: http://{args.host}:{args.port}")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    verify_runtime_environment()

    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
