from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file:
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        # ここでファイルを編集し、新しいファイルを保存
        # 例: ファイルを読み込んで編集するコード

        edited_file_path = os.path.join('edited', 'edited_' + uploaded_file.filename)
        # ここで編集されたファイルを保存

        return jsonify({'message': 'File edited and saved successfully.', 'edited_file_path': edited_file_path})

    return 'File not uploaded.'

if __name__ == '__main__':
    app.run(debug=True)
