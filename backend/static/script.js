// 登出
function logout() {
    const myIndexUrl = document.getElementById('myindex-url').innerText;
    window.location.href = myIndexUrl; // 重定向到myindex
}
// 提交
function submitForm() {
    document.getElementById('car-form').submit(); // 提交汽车表单
}