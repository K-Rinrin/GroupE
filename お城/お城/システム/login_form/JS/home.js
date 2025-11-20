let btn = document.querySelector('#btn')
let sidebar = document.querySelector('.sidebar')
let srcBtn = document.querySelector('.bx-search'); 

btn.onclick = function () {
    sidebar.classList.toggle('active')
}

srcBtn.onclick = function () {
    sidebar.classList.toggle('active')
}


document.querySelector(".register_btn").addEventListener("click", () => {
    document.getElementById("stamp_register").style.display = "none";
    document.getElementById("stamp_register_done").style.display = "block";
});

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
