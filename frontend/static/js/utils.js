function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(c =>
        '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
    ).join(''));
    return JSON.parse(jsonPayload);
}

async function takeOrder(orderId) {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const res = await fetch(`/api/v1/orders/${orderId}/take`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            alert('Заказ принят в работу!');
            location.reload();
        } else {
            const err = await res.json();
            alert('Ошибка: ' + (err.detail || 'Не удалось взять заказ'));
        }
    } catch (e) {
        alert('Сетевая ошибка при взятии заказа');
    }
}

async function changeStatus(orderId, newStatus) {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
        const res = await fetch(`/api/v1/orders/${orderId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ new_status: newStatus })
        });
        if (res.ok) {
            alert('Статус обновлён!');
            location.reload();
        } else {
            const err = await res.json();
            alert('Ошибка: ' + (err.detail || 'Не удалось обновить статус'));
        }
    } catch (e) {
        alert('Сетевая ошибка при смене статуса');
    }
}

function openGuaranteeModal(order) {
    const oldModal = document.getElementById('guaranteeModal');
    if (oldModal) oldModal.remove();

    const modalHtml = `
        <div id="guaranteeModal" class="modal-overlay active" style="z-index:1000;">
            <div class="window" style="width:500px; margin: 100px auto;">
                <div class="title-bar">
                    <div class="title-bar-text">Обращение по гарантии</div>
                    <div class="title-bar-controls">
                        <button aria-label="Close" onclick="closeGuaranteeModal()"></button>
                    </div>
                </div>
                <div class="window-body">
                    <p><strong>Заказ №${order.id_order}</strong></p>
                    <label>Компонент:</label>
                    <select id="guaranteeComponent" class="big-input">
                        ${order.components.map(c => `<option value="${c.id_component}">${c.manufacturer} ${c.model} (${c.title})</option>`).join('')}
                    </select>
                    <label>Описание проблемы:</label>
                    <textarea id="guaranteeDescription" class="big-input" rows="4" maxlength="300" placeholder="Опишите неисправность (минимум 10 символов)"></textarea>
                    <div style="margin-top:15px; display:flex; gap:10px; justify-content:flex-end;">
                        <button class="btn" onclick="closeGuaranteeModal()">Отмена</button>
                        <button class="btn-blue" onclick="submitGuarantee(${order.id_order})">Отправить</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

function closeGuaranteeModal() {
    const modal = document.getElementById('guaranteeModal');
    if (modal) modal.remove();
}

async function submitGuarantee(orderId) {
    const token = localStorage.getItem('token');
    const componentId = document.getElementById('guaranteeComponent').value;
    const description = document.getElementById('guaranteeDescription').value.trim();

    if (description.length < 10) {
        alert('Описание проблемы должно быть не менее 10 символов');
        return;
    }

    try {
        const res = await fetch('/api/v1/guarantees/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                order_id: orderId,
                defective_component_id: parseInt(componentId),
                problem_description: description
            })
        });

        if (res.ok) {
            alert('Обращение успешно отправлено!');
            closeGuaranteeModal();
        } else {
            const err = await res.json();
            alert('Ошибка: ' + (err.detail || 'Не удалось отправить обращение'));
        }
    } catch (e) {
        alert('Сетевая ошибка');
    }
}