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

    # 3. Render the HTML using a Jinja2 template and pass the JSON data
    # Get the template based on user input
    sTemplate = ''
    if 'template' in data:
        sTemplate = getTemplate(data['template'])
        if sTemplate == None:
            return jsonify({"error":"Template doesnt exist"})
    else:
        return jsonify({"error":"Template details doesnt exist in payload"})
    try:
        html = render_template(sTemplate, data=data, css=css_content)
    except Exception as e:
        return jsonify({"error": f"Template rendering failed - {str(e)}"}), 500
        
    # return html, 200
    # 4. Convert HTML to PDF using xhtml2pdf
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

def getTemplate(sTemplate):
    match sTemplate:
        case 'userInfo':
            return "info.html"
        case _:
            return None

# In a table, if the row content is too much then entire row moves to next page 
# and there will be alot of empty space available in the current page
# to solve this, we can split the contents into mulitple rows and can remove the border
# so it will look like a cell
@app.template_filter('split_to_multiple_rows')
def split_to_multiple_rows(oContent, iColumnToSplit, iMaxCharsInRow = 60):
    #sContent - Structure contains entire row data
    #iColumnToSplit - the column which have the content we need to split. Column number starts with 0.
    #iMaxCharsInRow - the maximum allowed character in a row

    #convert contents to words. 
    aWords = (oContent[iColumnToSplit] or ' ').split()
    #Split the content into multiple chunks 
    aChunks = []
    sChunk = ""

    
    for sWord in aWords:
        #If <br> tag is there then we need to split the content
        if sWord != '<br>' and len(sChunk) + len(sWord) + 1 <= iMaxCharsInRow:
            #Add space values already exist
            sChunk += ( " " if sChunk else "") + sWord
        else:
            aChunks.append(sChunk)
            #if <br> tag is there then remove it
            sChunk = ("" if sWord == '<br>' else sWord)
    #if the last content is not <br> then append
    if sChunk and sChunk.strip() != '<br>':
        aChunks.append(sChunk)

    aRows = []
    for i, sChunk in enumerate(aChunks):
        col1 = '<td>' + ( oContent[0] if i==0 else "&nbsp;" ) + '</td>'
        col2 = '<td>' + ( oContent[1] if i==0 else "&nbsp;" ) + '</td>'
        col3 = '<td>' + sChunk  + '</td>'

        #Assign css to the rows
        #if aChunks length is 1 then there is only 1 row
        #For the first and for the last row then apply respective css
        if i == 0 and len(aChunks) == 1:
            rowCSS = 'splitRowSingle'
        elif i == 0:
            rowCSS = 'splitRowFirst'
        elif i == len(aChunks) - 1:
            rowCSS = 'splitRowLast'
        else:
            rowCSS = 'splitRow'  

        tr = '<tr class='+ rowCSS + '>' + col1 + col2 + col3 + '</tr>'
        aRows.append(tr)

    #Join all rows into a single html string
    sAllRows = "\n".join(aRows)
    return sAllRows

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)