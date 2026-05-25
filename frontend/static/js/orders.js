function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));
    return JSON.parse(jsonPayload);
}
(async () => {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = '/login'; return; }

    const container = document.getElementById('ordersContainer');
    if (!container) return;

    try {
        const response = await fetch('/api/v1/orders/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }
        if (!response.ok) throw new Error('Ошибка сервера');

        const orders = await response.json();
        if (!orders.length) {
            container.innerHTML = '<p>У вас пока нет заказов.</p>';
            return;
        }

        const role = parseJwt(token).user_role;
        let html = orders.map(order => `
            <div class="order-card">
                <div class="order-info">
                    <strong>Заказ №${order.id_order}</strong>
                    <span>Статус: ${order.status_order}</span>
                    <span>Создан: ${new Date(order.created_at).toLocaleDateString()}</span>
                </div>
                <a href="/order_detail?id=${order.id_order}" class="btn">Подробнее</a>
            </div>
        `).join('');
        if (role === 'importer') {
            html += `<div class="order-card" style="justify-content:center"><a href="/available_orders" class="btn">Доступные заказы</a></div>`;
        }
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = '<p class="error-message">Ошибка загрузки заказов</p>';
    }
})();

