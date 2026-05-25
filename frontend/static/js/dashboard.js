(async () => {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = '/login'; return; }

    try {
        const res = await fetch('/api/v1/dashboard/stats', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Ошибка');
        const data = await res.json();

        // График заказов
        const orderLabels = data.orders_by_status.map(item => item.status);
        const orderCounts = data.orders_by_status.map(item => item.count);
        new Chart(document.getElementById('ordersChart'), {
            type: 'pie',
            data: {
                labels: orderLabels,
                datasets: [{
                    data: orderCounts,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                }]
            },
            options: { plugins: { title: { display: true, text: 'Заказы по статусам' } } }
        });

        // График пользователей
        const userLabels = data.users_by_role.map(item => item.role);
        const userCounts = data.users_by_role.map(item => item.count);
        new Chart(document.getElementById('usersChart'), {
            type: 'doughnut',
            data: {
                labels: userLabels,
                datasets: [{
                    data: userCounts,
                    backgroundColor: ['#FF9F40', '#4BC0C0', '#9966FF']
                }]
            },
            options: { plugins: { title: { display: true, text: 'Пользователи по ролям' } } }
        });

    } catch (e) {
        console.error(e);
        alert('Не удалось загрузить данные для дашборда');
    }
})();