let btn = document.querySelector('#btn')
let sidebar = document.querySelector('.sidebar')
let srcBtn = document.querySelector('.bx-search'); 
const SignupButton = document.getElementById("signup");
const LoginButton = document.getElementById("login");
const container = document.getElementById("container");

SignupButton.addEventListener("click",() => {
    container.classList.add("right-panel-active");
});

LoginButton.addEventListener("click",() => {
    container.classList.remove("right-panel-active");
});

btn.onclick = function () {
    sidebar.classList.toggle('active')
};

srcBtn.onclick = function () {
    sidebar.classList.toggle('active')
};


// =====================================================================

// 簡単なログイン機能（ローカルストレージ使用）

// ユーザーデータの仮登録（本来はバックエンドから取得）
const users = [
    { email: "test@example.com", password: "password123" },
    { email: "user@example.com", password: "mypassword" }
];

// サインアップ処理
function signup() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("Email").value;
    const password = document.getElementById("password").value;
    
    if (!name || !email || !password) {
        alert("すべてのフィールドを入力してください。");
        return;
    }
    
    const existingUser = users.find(user => user.email === email);
    if (existingUser) {
        alert("このメールアドレスはすでに登録されています。");
        return;
    }
    
    users.push({ email, password });
    localStorage.setItem("users", JSON.stringify(users));
    alert("サインアップ成功！ログインしてください。");
}

// ログイン処理
function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    
    const storedUsers = JSON.parse(localStorage.getItem("users")) || users;
    const user = storedUsers.find(user => user.email === email && user.password === password);
    
    if (user) {
        localStorage.setItem("loggedInUser", email);
        alert("ログイン成功！");
        window.location.href = "home.html"; // ダッシュボードページへ遷移
    } else {
        alert("メールアドレスまたはパスワードが間違っています。");
    }
}

// ボタンイベントリスナー
window.onload = function() {
    document.querySelector(".signup-container button").addEventListener("click", function(event) {
        event.preventDefault();
        signup();
    });

    document.querySelector(".login-container button").addEventListener("click", function(event) {
        event.preventDefault();
        login();
    });
};
