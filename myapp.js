
const dropArea = document.getElementById('drop-area');
const fileList = document.getElementById('file-list');
const fileInput = document.getElementById('fileInput');
const downloadButton = document.getElementById('download-button');

// ドラッグ＆ドロップイベントリスナー
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('highlight');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList remove('highlight');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('highlight');
    const files = e.dataTransfer.files;

    // ドラッグ＆ドロップでアップロードされたファイルを表示
    for (const file of files) {
        handleUploadedFile(file);
    }
});

// fileInputの変更イベントリスナー
fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    for (const file of files) {
        handleUploadedFile(file);
    }
});

// ファイルを処理する共通の関数
function handleUploadedFile(file) {
    if (file.name.endsWith('.xlsx')) {
        const listItem = document.createElement('li');
        listItem.textContent = file.name;
        fileList.appendChild(listItem);

        // ファイルをサーバーにアップロード
        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
        .catch(error => {
            console.error(error);
        });
    } else {
        console.log('無効なファイルタイプです。.xlsx拡張子のExcelファイルをアップロードしてください。');
    }
}

// ファイルのダウンロードボタンのクリックイベント
downloadButton.addEventListener('click', () => {
    fetch('/download/edited_filename.xlsx', {
        method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'edited_filename.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    });
});
