
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
