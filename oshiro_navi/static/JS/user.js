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

document.addEventListener("DOMContentLoaded", () => {
    const openMenu = document.getElementById("openMenu");
    const closeMenu = document.getElementById("closeMenu");
    const sideMenu = document.getElementById("sideMenu");
    const overlay = document.getElementById("overlay");

    const mobileSwitchBtn = document.getElementById("mobileSwitchBtn");
    const container = document.getElementById("container"); // ← 追加！

    // --- ハンバーガーメニュー（スマホ） ---
    if (openMenu && sideMenu && overlay) {
        openMenu.addEventListener("click", (e) => {
            if (window.innerWidth <= 600) {
                e.preventDefault();
                sideMenu.classList.add("active");
                overlay.classList.add("active");
            }
        });
    }

    // 閉じる処理を関数化
    const closeSideMenu = () => {
        sideMenu.classList.remove("active");
        overlay.classList.remove("active");
    };

    closeMenu?.addEventListener("click", closeSideMenu);
    overlay?.addEventListener("click", closeSideMenu);

    // --- ログイン / 新規登録 切り替え（スマホ） ---
    if (mobileSwitchBtn && container) {
        mobileSwitchBtn.addEventListener("click", () => {
            container.classList.toggle("right-panel-active");

            mobileSwitchBtn.textContent =
                container.classList.contains("right-panel-active")
                    ? "ログインに戻る"
                    : "新規登録はこちら";
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menuIconText = document.getElementById('menu-icon-text');
    const userContainer = document.querySelector('.user-container');

    menuToggle.addEventListener('click', function() {
        // activeクラスを切り替え
        userContainer.classList.toggle('active');

        // アイコンを menu ↔ close で切り替え
        if (userContainer.classList.contains('active')) {
            menuIconText.textContent = 'close';
        } else {
            menuIconText.textContent = 'menu';
        }
    });

    // メニュー内のリンクをクリックしたらメニューを閉じる
    const navLinks = document.querySelectorAll('.nav a, .dropdown-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            userContainer.classList.remove('active');
            menuIconText.textContent = 'menu';
        });
    });
});

const toggleBtn = document.getElementById("menu-toggle");
    const nav = document.getElementById("mobile-nav");
    const iconText = document.getElementById("menu-icon-text");

    toggleBtn.addEventListener("click", () => {
    nav.classList.toggle("active");

    if (nav.classList.contains("active")) {
        iconText.textContent = "close";
    } else {
        iconText.textContent = "menu";
    }
    });