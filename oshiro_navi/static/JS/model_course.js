document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('spots-container');
    const addBtn = document.getElementById('add-spot-btn');

   
    addBtn.addEventListener('click', function() {
       
        const currentCount = container.querySelectorAll('.spot-item').length;
        const nextCount = currentCount + 1;

        const newSpotHtml = `
            <div class="spot-item" data-index="${nextCount}">
                <h2>スポット ${nextCount}</h2>
                <div class="form-group">
                    <label>スポット名</label><br>
                    <input type="text" name="spot_name_${nextCount}" placeholder="スポット名を入力" style="width: 100%; max-width: 500px;">
                </div>
                <!-- ... 以下省略 (登録画面と同じ内容) ... -->
                <hr>
            </div>
        `;
        container.insertAdjacentHTML('beforeend', newSpotHtml);
    });
});