document.addEventListener('DOMContentLoaded', function() {
    // コンテナとボタンを取得
    const container = document.getElementById('spots-container');
    const addBtn = document.getElementById('add-spot-btn');

    // エラー防止: 要素がない場合は何もしない
    if (!container || !addBtn) return;

    addBtn.addEventListener('click', function() {
        // 現在のスポット数を数える
        const currentCount = container.querySelectorAll('.spot-item').length;
        const nextCount = currentCount + 1;

        // HTMLを作成
        const newSpotHtml = `
            <div class="spot-item">
                <h2>スポット ${nextCount}</h2>
                <div class="form-group">
                    <label>スポット名 *</label><br>
                    <input type="text" name="spot_name_${nextCount}" placeholder="スポット名を入力" style="width: 100%; max-width: 500px;">
                </div>
                <div class="form-group">
                    <label>短い説明文</label><br>
                    <textarea name="spot_short_${nextCount}" rows="3" style="width: 100%; max-width: 500px;"></textarea>
                </div>
                <div class="form-group">
                    <label>詳細説明文</label><br>
                    <textarea name="spot_detail_${nextCount}" rows="4" style="width: 100%; max-width: 500px;"></textarea>
                </div>
                <div class="form-group">
                    <label>スポット画像</label><br>
                    <input type="file" name="spot_image_${nextCount}" accept="image/*">
                </div>
                <div class="form-group">
                    <label>補足情報</label><br>
                    <textarea name="spot_note_${nextCount}" rows="2" style="width: 100%; max-width: 500px;"></textarea>
                </div>
                <hr>
            </div>
        `;

        // 追加
        container.insertAdjacentHTML('beforeend', newSpotHtml);
    });
});