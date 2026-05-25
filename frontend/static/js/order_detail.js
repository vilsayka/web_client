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
    const orderId = new URLSearchParams(window.location.search).get('id');
    if (!token || !orderId) { window.location.href = '/login'; return; }

    let currentRole, currentUserId;
    try {
        const payload = parseJwt(token);
        currentRole = payload.user_role;
        currentUserId = payload.user_id;
    } catch (e) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        return;
    }

    const container = document.getElementById('orderDetails');
    document.getElementById('orderId').textContent = orderId;

    try {
        const response = await fetch(`/api/v1/orders/${orderId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) { localStorage.removeItem('token'); window.location.href = '/login'; return; }
        if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);

        const order = await response.json();

        let componentsHtml = order.components?.length
            ? order.components.map(c => `<tr><td>${c.manufacturer} ${c.model}</td><td>${c.title}</td><td>${c.price} ₽</td><td>${c.quantity}</td></tr>`).join('')
            : '<tr><td colspan="4">Нет комплектующих</td></tr>';

        let actionsHtml = '';
        if (currentRole === 'importer') {
            if (order.status_order === 'ожидает сборщика') actionsHtml += `<button class="btn-blue" id="takeOrderBtn">Взять в работу</button>`;
            if (order.id_importer === currentUserId && order.status_order === 'на сборке') actionsHtml += `<button class="btn-blue" id="finishOrderBtn">Завершить сборку</button>`;
        }
        if (currentRole === 'customer' && order.status_order === 'собрана') actionsHtml += `<button class="btn-blue" id="guaranteeBtn">Обратиться по гарантии</button>`;

        container.innerHTML = `
            <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                <div>
                    <p><strong>Заказчик:</strong> ${order.customer_name || '—'}</p>
                    <p><strong>Сборщик:</strong> ${order.importer_name || 'Не назначен'}</p>
                    <p><strong>Статус:</strong> ${order.status_order}</p>
                </div>
                <div>
                    <p><strong>Гарантия:</strong> ${order.warranty_period} мес.</p>
                    <p><strong>Создан:</strong> ${new Date(order.created_at).toLocaleString()}</p>
                    <p><strong>Сумма:</strong> ${order.total_price} ₽</p>
                </div>
            </div>
            <h4>Комплектующие</h4>
            <table class="component-table"><thead><tr><th>Название</th><th>Тип</th><th>Цена</th><th>Кол-во</th></tr></thead><tbody>${componentsHtml}</tbody></table>
            <div class="actions">${actionsHtml}</div>
        `;

        document.getElementById('takeOrderBtn')?.addEventListener('click', () => takeOrder(orderId));
        document.getElementById('finishOrderBtn')?.addEventListener('click', () => changeStatus(orderId, 'собрана'));
        document.getElementById('guaranteeBtn')?.addEventListener('click', () => openGuaranteeModal(order));
    } catch (error) {
        container.innerHTML = `<p class="error-message">Ошибка загрузки: ${error.message}</p>`;
    }
})();