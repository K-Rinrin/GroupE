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
        <div id="spots-container">
            <div class="spot-item">
                <h2>スポット ${nextCount}</h2>
                <table class="basic-info-table" border="1" cellpadding="8" cellspacing="0">
                    <tr>
                        <th><label>スポット名 </label><p class="required-point">＊</p><br></th>
                        <td>
                            <input type="text" name="spot_name_${nextCount }" required placeholder="例: 史跡若松城『鶴ヶ城』" style="width: 100%; max-width: 500px;">
                        </td>
                    </tr>
                    <tr>
                        <th><label>短い説明文 </label><p class="required-point">＊</p><br></th>
                        <td>
                            <textarea name="spot_short_${nextCount }" rows="3" style="width: 100%; max-width: 500px;"></textarea>
                        </td>
                    </tr>
                    <tr>
                        <th><label>詳細説明文 </label><p class="required-point">＊</p><br></th>
                        <td>
                            <textarea name="spot_detail_${nextCount }" rows="4" style="width: 100%; max-width: 500px;"></textarea>
                        </td>
                    </tr>
                    <tr>
                        <th><label>スポット画像 </label><p class="required-point">＊</p><br></th>
                        <td>
                            <input type="file" name="spot_image_${nextCount }" accept="image/*">
                        </td>
                    </tr>
                    <tr>
                        <th><label>補足情報 </label><p class="required-point">＊</p><br></th>
                        <td>
                            <textarea name="spot_note_${nextCount }" rows="2" style="width: 100%; max-width: 500px;"></textarea>
                        </td>
                    </tr>
                </table>
                <hr style="width:100%; margin-bottom: 10px; margin-top: 10px;">
            </div>
        </div>
        `;

        // 追加
        container.insertAdjacentHTML('beforeend', newSpotHtml);
    });
});