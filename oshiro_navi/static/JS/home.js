
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

document.addEventListener("DOMContentLoaded", () => {

    const dropdown = document.querySelector(".dropdown");
    const btn = document.querySelector(".dropdown-btn");
    const menu = document.querySelector(".dropdown-menu");

    let fixed = false; // ← 固定状態のフラグ

    // ▼ クリックで固定/解除
    btn.addEventListener("click", (e) => {
        e.preventDefault();
        fixed = !fixed;  // ON / OFF
        menu.classList.toggle("active", fixed);
    });

    // ▼ ホバーで開く（固定されていない場合のみ）
    dropdown.addEventListener("mouseenter", () => {
        if (!fixed) {
            menu.classList.add("hover-open");
        }
    });

    dropdown.addEventListener("mouseleave", () => {
        if (!fixed) {
            menu.classList.remove("hover-open");
        }
    });

});
