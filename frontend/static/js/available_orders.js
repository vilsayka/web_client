(async () => {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = '/login'; return; }

    const container = document.getElementById('availableOrdersContainer');
    if (!container) return;

    try {
        const res = await fetch('/api/v1/orders/available', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Ошибка сервера');
        const orders = await res.json();

        if (!orders.length) {
            container.innerHTML = '<p>Нет доступных заказов.</p>';
            return;
        }

        container.innerHTML = orders.map(o => `
            <div class="order-card">
                <div>
                    <strong>Заказ №${o.id_order}</strong>
                    <div>Заказчик: ${o.customer_name}</div>
                    <div>Создан: ${new Date(o.created_at).toLocaleDateString()}</div>
                </div>
                <button class="btn-blue take-order-btn" data-order-id="${o.id_order}">Взять в работу</button>
            </div>
        `).join('');

        document.querySelectorAll('.take-order-btn').forEach(btn => {
            btn.addEventListener('click', () => takeOrder(btn.dataset.orderId));
        });
    } catch (e) {
        container.innerHTML = '<p class="error-message">Ошибка загрузки</p>';
    }
})();