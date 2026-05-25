(async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch('/api/v1/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('token');
                window.location.href = '/login';
                return;
            }
            throw new Error('Ошибка сервера');
        }
        const user = await response.json();

        document.querySelector('.profile-username').textContent = user.username;

        const roleMap = {
            customer: 'Заказчик',
            importer: 'Сборщик',
            admin: 'Администратор'
        };
        document.querySelector('.profile-role').textContent = roleMap[user.user_role] || user.user_role;

        if (user.user_role === 'importer') {
            const info = document.querySelector('.profile-info');

            const addField = (label, value) => {
                if (value) {
                    const span = document.createElement('span');
                    span.className = 'profile-extra';
                    span.textContent = `${label}: ${value}`;
                    info.appendChild(span);
                }
            };
            addField('Имя', user.full_name);
            addField('Email', user.email);
            addField('Телефон', user.telephone);
        }

const ordersLink = document.createElement('a');
ordersLink.href = '/orders';
ordersLink.className = 'btn';
ordersLink.textContent = 'Мои заказы';
document.querySelector('.profile-info').appendChild(ordersLink);

if (user.user_role === 'importer') {
    const availLink = document.createElement('a');
    availLink.href = '/available_orders';
    availLink.className = 'btn';
    availLink.textContent = 'Доступные заказы';
    document.querySelector('.profile-info').appendChild(availLink);
}
if (user.user_role === 'customer') {
    const guaranteeLink = document.createElement('a');
    guaranteeLink.href = '/my_guarantees';
    guaranteeLink.className = 'btn';
    guaranteeLink.textContent = 'Мои обращения по гарантии';
    document.querySelector('.profile-info').appendChild(guaranteeLink);
}
if (user.user_role === 'admin') {
    const adminLink = document.createElement('a');
    adminLink.href = 'http://127.0.0.1:5000';  
    adminLink.className = 'btn';
    adminLink.textContent = 'Админ-панель';
    document.querySelector('.profile-info').appendChild(adminLink);
}
    } catch (err) {
        console.error('Ошибка загрузки профиля:', err);
        alert('Не удалось загрузить профиль');
    }
})();

const refreshBtn = document.createElement('button');
refreshBtn.className = 'btn';
refreshBtn.textContent = 'Обновить токен';
refreshBtn.addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const res = await fetch('/api/v1/refresh', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('token', data.access_token);
            alert('Токен обновлён!');
        } else {
            const err = await res.json();
            alert('Ошибка: ' + err.detail);
        }
    } catch (e) {
        alert('Сетевая ошибка');
    }
});
document.querySelector('.profile-info').appendChild(refreshBtn);