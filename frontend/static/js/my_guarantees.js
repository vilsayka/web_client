(async () => {
    const token = localStorage.getItem('token');
    if (!token) { window.location.href = '/login'; return; }

    const container = document.getElementById('guaranteesContainer');
    try {
        const res = await fetch('/api/v1/guarantees/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Ошибка сервера');
        const guarantees = await res.json();

        if (!guarantees.length) {
            container.innerHTML = '<p>У вас нет обращений по гарантии.</p>';
            return;
        }

        const statusMap = {
            'under consideration': 'На рассмотрении',
            'rejected': 'Отклонено',
            'accepted': 'Принято',
            'closed': 'Закрыто'
        };

        container.innerHTML = guarantees.map(g => `
            <div class="guarantee-card">
                <div><strong>Обращение №${g.id_repair_warranty}</strong></div>
                <div>Заказ №${g.id_order} | Компонент №${g.id_defective_component}</div>
                <div>Описание: ${g.problem_description}</div>
                <div>Статус: <span class="status-${g.status_repair.replace(' ', '_')}">${statusMap[g.status_repair] || g.status_repair}</span></div>
                <div>Создано: ${new Date(g.created_at).toLocaleString()}</div>
                ${g.date_repair_completion ? `<div>Завершено: ${new Date(g.date_repair_completion).toLocaleString()}</div>` : ''}
            </div>
        `).join('');
    } catch (e) {
        container.innerHTML = '<p class="error-message">Ошибка загрузки обращений</p>';
    }
})();