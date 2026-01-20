document.addEventListener('DOMContentLoaded', function() {
    // 要素を取得
    const spot2Area = document.getElementById('spot2-area');
    const addBtn = document.getElementById('add-spot-btn');
    const spot2NameInput = document.querySelector('input[name="spot2_name"]');

    // スポット2を表示する関数
    function showSpot2() {
        if (spot2Area) {
            spot2Area.style.display = 'block'; // 表示
        }
        if (addBtn) {
            addBtn.style.display = 'none'; // 追加ボタンは隠す（最大2件のため）
        }
    }

    // ボタンクリック時のイベント
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            showSpot2();
        });
    }

    // 【重要】編集画面や、入力エラーで戻ってきた時の対策
    // もし最初からスポット2に名前が入っていれば、隠さずに表示しておく
    if (spot2NameInput && spot2NameInput.value.trim() !== "") {
        showSpot2();
    }
});