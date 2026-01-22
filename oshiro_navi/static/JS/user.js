document.addEventListener("DOMContentLoaded", () => {

    // --- 1. ドロップダウンメニューの制御 ---
    const dropdown = document.querySelector(".dropdown");
    const btn = document.querySelector(".dropdown-btn");
    const menu = document.querySelector(".dropdown-menu");

    if (btn && menu) {
        let fixed = false; // 固定状態のフラグ

        // クリックで固定/解除
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            fixed = !fixed;
            menu.classList.toggle("active", fixed);
        });

        // ホバーで開く（固定されていない場合のみ）
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
    }
        if (document.querySelector(".multiSwiper")) {
            const swiper = new Swiper(".multiSwiper", {
                loop: true,           // ループ
                slidesPerView: 3,     // 1画面に3枚
                spaceBetween: 25,     // カード同士の隙間
                slidesPerGroup: 1,    // 1枚ずつズレる
                
                // 自動再生
                autoplay: {
                    delay: 5000,
                    disableOnInteraction: false,
                },
                
                // ナビゲーション
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
                
                // ページネーション（ドット）
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },

                // レスポンシブ（スマホ対応）
                breakpoints: {
                    320: { slidesPerView: 1 },
                    768: { slidesPerView: 2 },
                    1024: { slidesPerView: 3 }
                }
            });
        }
    });