
document.getElementById("imageInput").addEventListener("change", function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById("preview");

    // ファイルが選択されていない場合
    if (!file) {
        preview.innerHTML = "画像プレビューエリア";
        preview.style.backgroundImage = "";
        return;
    }

    // 画像URLを生成してプレビュー
    const imgURL = URL.createObjectURL(file);

    preview.style.backgroundImage = `url(${imgURL})`;
    preview.style.backgroundSize = "contain";
    preview.style.backgroundRepeat = "no-repeat";
    preview.style.backgroundPosition = "center";

    preview.innerHTML = ""; // テキストを消す
});
