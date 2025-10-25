"""
ScienceSheetForge Web Application
Modern modal-based worksheet generator with NGSS standards
"""

from flask import Flask, render_template, send_file, request, jsonify
import os
import sys
from datetime import datetime

# Add generators to path
sys.path.insert(0, os.path.dirname(__file__))

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

# Create output directory
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


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


@app.route('/generate', methods=['POST'])
def generate():
    """Generate worksheet"""
    try:
        data = request.get_json()
        grade_level = data.get('grade_level')
        standard_code = data.get('standard_code')
        worksheet_format = data.get('worksheet_format')

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

        answer_key_filename = output_filename.replace('.png', '_ANSWER_KEY.png')

        return jsonify({
            'success': True,
            'worksheet': f'/view/{os.path.basename(output_filename)}',
            'answer_key': f'/view/{os.path.basename(answer_key_filename)}',
            'timestamp': timestamp,
            'worksheet_format': worksheet_format,
            'standard': standard_code
        })

    except Exception as e:
        print(f"Error generating worksheet: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/view/<filename>')
def view_file(filename):
    """View generated worksheet"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    return "File not found", 404


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated worksheet"""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return "File not found", 404


if __name__ == '__main__':
    print("=" * 70)
    print("SCIENCESHEETFORGE - Modern Worksheet Generator")
    print("=" * 70)
    print("\nStarting local server...")
    print("\nOpen your browser and go to: http://localhost:3000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    verify_runtime_environment()

    app.run(debug=True, host='127.0.0.1', port=3000)
