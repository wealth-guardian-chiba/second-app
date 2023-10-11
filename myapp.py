from flask import Flask, request, jsonify, send_file
import os
import main_function as mf

app = Flask(__name)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        df = pd.read_excel(filepath)
        df1 = mf.function1(df)
        df2 = mf.function2(df)

        edited_file_path1 = os.path.join('edited', 'edited1_' + uploaded_file.filename)
        edited_file_path2 = os.path.join('edited', 'edited2_' + uploaded_file.filename)
        # ここで編集されたファイルを保存

        return jsonify({'message': 'File edited and saved successfully.', 'edited_file_path': edited_file_path1}), jsonify({'message': 'File edited and saved successfully.', 'edited_file_path': edited_file_path2})

    return 'File not uploaded.'

if __name__ == '__main__':
    app.run(debug=True)
