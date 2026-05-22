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

        // Если импортёр – показываем дополнительные данные
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
    } catch (err) {
        console.error('Ошибка загрузки профиля:', err);
        alert('Не удалось загрузить профиль');
    }
})();