from flask import Flask, jsonify, request, send_file, render_template
from xhtml2pdf import pisa
import os
import io
import json

app = Flask(__name__)
port = int(os.getenv('PORT', 5000))


@app.route('/')
def hello():
    return jsonify(message="Hello from Flask in SAP BAS!")

@app.route('/generatePDF', methods=['GET', 'POST'])
def generate_pdf():
    data = {}
    if app.static_folder is None:
        raise RuntimeError("Static folder is not set.")

    # 1. Get JSON data from user or from file (static/content.json)
    if request.method == 'GET':
        file_path = os.path.join(app.static_folder, 'content.json')
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            return jsonify({"error": f"Failed to read content.json - {str(e)}"}), 500

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

    # 2.Read CSS content
    css_path = os.path.join(app.static_folder, 'style.css')
    try:
        with open(css_path, 'r') as f:
            css_content = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to read CSS - {str(e)}"}), 500

    # 2. Render the HTML using a Jinja2 template and pass the JSON data
    try:
        html = render_template('info.html', data=data, css=css_content)
    except Exception as e:
        return jsonify({"error": f"Template rendering failed - {str(e)}"}), 500

    # 3. Convert HTML to PDF using xhtml2pdf
    pdf_buffer = io.BytesIO()
    result = pisa.CreatePDF(io.StringIO(html), dest=pdf_buffer)

    if result.err:
        return jsonify({"error": "Failed to generate PDF"}), 500

    pdf_buffer.seek(0)

    # 4. Return PDF as downloadable file
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='generated.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)