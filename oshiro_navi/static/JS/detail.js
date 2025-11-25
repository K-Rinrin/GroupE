const STORAGE_KEY = 'castle_reviews_v1';
const qs = s => document.querySelector(s);
const qsa = s => Array.from(document.querySelectorAll(s));
const form = qs('#reviewForm');
const nameInput = qs('#name');
const titleInput = qs('#title');
const bodyInput = qs('#body');
const starEls = qsa('.star');
const avgRatingEl = qs('#avgRating');
const listEl = qs('#list');
const charCount = qs('#charCount');
const photoInput = qs('#photo');
const photoPreview = qs('#photoPreview');
const sortSelect = qs('#sortSelect');
const totalCount = qs('#totalCount');
const clearBtn = qs('#clearBtn');
let currentRating = 0;
let reviews = [];

function saveReviews(){ localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews)); }
function loadReviews(){ try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [] } catch { return [] } }

function formatDate(ts){
const d = new Date(ts);
return `${d.getFullYear()}/${(d.getMonth()+1).toString().padStart(2,'0')}/${d.getDate().toString().padStart(2,'0')} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`;
}

function escapeText(s){ return s.replace(/[&<>]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])) }

function render(){
listEl.innerHTML = '';
let items = [...reviews];
const sort = sortSelect.value;
if(sort==='rating_desc') items.sort((a,b)=>b.rating - a.rating);
else if(sort==='rating_asc') items.sort((a,b)=>a.rating - b.rating);
else items.sort((a,b)=>b.createdAt - a.createdAt);
totalCount.textContent = items.length;

items.forEach(r=>{
    const starsDisplay = '★'.repeat(r.rating) + '☆'.repeat(5 - r.rating);
    const el = document.createElement('div');
    el.className = 'review card';
    el.innerHTML = `
    <div class="avatar">${r.name ? escapeText(r.name.slice(0,2)) : '訪'}</div>
    <div class="content">
        <div class="meta">
        <span>${formatDate(r.createdAt)}</span>
        <span style="color:#FFD700">${starsDisplay}</span>
        </div>
        <h3>${escapeText(r.title)}</h3>
        <p>${escapeText(r.body)}</p>
        ${r.photo ? `<img src="${r.photo}" class="image-thumb">` : ''}
        <div class="controls">
        <button class="btn secondary" data-action="edit" data-id="${r.id}">編集</button>
        <button class="btn" data-action="delete" data-id="${r.id}">削除</button>
        </div>
    </div>`;
    listEl.appendChild(el);

    el.querySelectorAll('button[data-action]').forEach(btn=>{
    btn.addEventListener('click', e=>{
        const id = e.currentTarget.dataset.id;
        if(btn.dataset.action==='delete'){
        if(confirm('この口コミを削除しますか？')){
            reviews = reviews.filter(x=>x.id!==id);
            saveReviews(); render(); updateAvg();
        }
        } else {
        const rdata = reviews.find(x=>x.id===id);
        nameInput.value = rdata.name || '';
        titleInput.value = rdata.title;
        bodyInput.value = rdata.body;
        setRating(rdata.rating);
        if(rdata.photo){ photoPreview.innerHTML = `<img src="${rdata.photo}" class="image-thumb">`; }
        reviews = reviews.filter(x=>x.id!==id);
        saveReviews(); render(); updateAvg();
        window.scrollTo({top:0,behavior:'smooth'});
        }
    });
    });
});
}

function updateAvg(){
if(reviews.length===0){ avgRatingEl.textContent = '0.0'; return }
const avg = reviews.reduce((a,b)=>a+b.rating,0)/reviews.length;
avgRatingEl.textContent = avg.toFixed(1);
}

function setRating(n){
currentRating = +n;
starEls.forEach(st=>{
    st.style.color = st.dataset.value <= n ? '#FFD700' : '#ccc';
});
}

starEls.forEach(st=>st.addEventListener('click', ()=>setRating(st.dataset.value)));

photoInput.addEventListener('change', ()=>{
const f = photoInput.files[0];
if(!f) return photoPreview.innerHTML='';
const reader = new FileReader();
reader.onload = e=>photoPreview.innerHTML=`<img src="${e.target.result}" class="image-thumb">`;
reader.readAsDataURL(f);
});

bodyInput.addEventListener('input', ()=>charCount.textContent = bodyInput.value.length);

form.addEventListener('submit', async e=>{
e.preventDefault();
const title = titleInput.value.trim();
const body = bodyInput.value.trim();
if(!title||!body){ alert('タイトルと本文を入力してください'); return; }

let photoData=null;
const f = photoInput.files[0];
if(f){
    if(f.size>3*1024*1024){ alert('画像は3MB以下にしてください'); return; }
    photoData = await new Promise(res=>{
    const r=new FileReader(); r.onload=()=>res(r.result); r.readAsDataURL(f);
    });
}

const newReview={id:Date.now()+Math.random().toString(36).slice(2),name:nameInput.value,title,body,rating:currentRating,photo:photoData,createdAt:Date.now()};
reviews.unshift(newReview);
saveReviews(); render(); updateAvg();
form.reset(); photoPreview.innerHTML=''; setRating(0); charCount.textContent='0';
});

clearBtn.addEventListener('click', ()=>{ form.reset(); photoPreview.innerHTML=''; setRating(0); charCount.textContent='0'; });

sortSelect.addEventListener('change', render);

document.addEventListener('DOMContentLoaded', ()=>{
reviews=loadReviews(); render(); updateAvg(); setRating(0);
});

// タブ切り替え
document.querySelectorAll('.tab').forEach(tab=>{
tab.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
});
});