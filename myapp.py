from flask import Flask, request, jsonify, send_file
import os
import main_function as mf
import pandas as pd
from openpyxl import load_workbook

app = Flask(__name)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        if upload_file.filename.endwith('.xlsx'):
            file_path = os.path.join('uploads', uploaded_file.filename)
            uploaded_file.save(file_path)
            df = pd.read_excel(filepath)
            df1 = mf.function1(df)
            df2 = mf.function2(df)

            edited_file_path = os.path.join('edited', 'edited_' + uploaded_file.filename)
            df1.to_excel(edited_file_path, index=False, engine='openpyxl', sheet_name="債券リスト")
            df2.to_excel(edited_file_path, index=False, engine='openpyxl', sheet_name="金利CF表")
            # ここで編集されたファイルを保存

            return jsonify({'message': 'File edited and saved successfully.', 'edited_file_path': edited_file_path})
        else:
            return jsonify({'error': 'Invalid file type. Please uploed an Excel file with the .xlsx extension.'})
    return 'File not uploaded.'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    edited_file_path = os.path.join('edited', filename)
    return send_file(edited_file_path, as_attachment=True)
    
if __name__ == '__main__':
    app.run(debug=True)
