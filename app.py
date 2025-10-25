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
from generators.crossword_generator import generate_crossword_tpt_style as generate_crossword
from generators.word_search_generator import generate_word_search
from generators.matching_generator import generate_matching

app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'output')

# Create output directory
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html',
                          worksheet_formats=WORKSHEET_FORMATS,
                          ngss_standards=NGSS_STANDARDS)


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

        # Generate worksheet based on format
        if worksheet_format == 'crossword':
            generate_crossword(standard_data, grade_level, output_filename)
        elif worksheet_format == 'word-search':
            generate_word_search(standard_data, grade_level, output_filename)
        elif worksheet_format == 'matching':
            generate_matching(standard_data, grade_level, output_filename)
        else:
            # Default to word search for now
            generate_word_search(standard_data, grade_level, output_filename)

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
    print("\nOpen your browser and go to: http://localhost:5555")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    app.run(debug=True, host='127.0.0.1', port=5555)
