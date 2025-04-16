from flask import Flask, request, send_file
import tabula
import pandas as pd
import os
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_excel():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded file
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        # Extract tables from PDF
        tables = tabula.read_pdf(filepath, pages='all', multiple_tables=True)
        combined_df = pd.concat(tables, ignore_index=True)

        # Save Excel
        excel_path = filepath.replace(".pdf", ".xlsx")
        combined_df.to_excel(excel_path, index=False)

        return send_file(excel_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

app.run(debug=True)
