document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('#reg-form');

    if (!form) return;

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const username = form.querySelector('input[name="username"]').value.trim();
        const password = form.querySelector('input[name="password"]').value.trim();

        if (!username || !password) {
            alert('Заполните все поля');
            return;
        }

        const apiUrl = window.location.origin + '/api/v1/register';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                alert('Регистрация успешна! Теперь войдите под своим логином.');
                window.location.href = '/main-user';
            } else {
                const error = await response.json();
                alert('Ошибка: ' + (error.detail || 'Неизвестная ошибка'));
            }
        } catch (err) {
            alert('Не удалось соединиться с сервером: ' + err.message);
        }
    });
});