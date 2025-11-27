const audio = document.getElementById("audio");
const playBtn = document.getElementById("playBtn");
const pauseBtn = document.getElementById("pauseBtn");
const progress = document.getElementById("progress");

// ▶ 再生
playBtn.addEventListener("click", () => {
    audio.play();
});  

// ⏸ 一時停止
pauseBtn.addEventListener("click", () => {
    audio.pause();
});

// 進捗バー更新
audio.addEventListener("timeupdate", () => {
    const percent = (audio.currentTime / audio.duration) * 100;
    progress.style.width = percent + "%";
});
