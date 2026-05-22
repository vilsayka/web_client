document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#login-form');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // Для OAuth2PasswordRequestForm нужен формат x-www-form-urlencoded
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const apiUrl = window.location.origin + '/api/v1/login';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                window.location.href = '/main_user';
            } else {
                const error = await response.json();
                alert('Ошибка входа: ' + (error.detail || 'Неверные данные'));
            }
        } catch (err) {
            alert('Ошибка соединения с сервером');
        }
    });
});