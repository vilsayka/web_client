const modal = document.getElementById('modalOverlay');
const modalTitle = document.getElementById('modalTitle');
const modalContent = document.getElementById('modalContent');
const closeBtn = document.getElementById('closeModal');

let componentsData = null;
const selectedComponents = {};
const requiredComponents = [
    'Процессор',
    'Материнская плата',
    'Блок питания',
    'Корпус',
    'Видеокарта',
    'Охлаждение процессора',
    'Оперативная память',
    'Накопители'
];
async function loadComponents() {
    try {
        const res = await fetch('/api/v1/components/');
        componentsData = await res.json();
    } catch (e) {
        console.error('Ошибка загрузки:', e);
        modalContent.innerHTML = '<div class="error-message">Ошибка загрузки компонентов</div>';
    }
}

function openModal(category) {
    if (!componentsData) return;

    modalTitle.textContent = category;
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    const cat = componentsData.components.find(c => c.category === category);
    modalContent.innerHTML = `
        <div class="components-list">
            ${cat.items.map(item => `
                <div class="component-item">
                    <div class="component-name">${item.name}</div>
                    <div class="component-description">${item.description}</div>
                    <div class="component-price">${item.price}</div>
                    <button class="select-btn" data-id="${item.id}" data-name="${item.name}">Выбрать</button>
                </div>
            `).join('')}
        </div>
    `;
    modalContent.querySelectorAll('.select-btn').forEach(btn => {
        btn.onclick = () => selectComponent(category, btn.dataset.id, btn.dataset.name);
    });
}

function selectComponent(category, id, name) {
    selectedComponents[category] = { id, name };
    const block = document.querySelector(`[data-component="${category}"]`).closest('.component');
    const left = block.querySelector('.component-left');

    let label = left.querySelector('.selected-component');
    if (!label) {
        label = document.createElement('span');
        label.className = 'selected-component';
        left.appendChild(label);
    }
    label.textContent = name;
    block.querySelector('.open-modal-btn').textContent = 'Изменить';
    closeModal();
}

async function submitBuild() {
    const componentsCount = Object.keys(selectedComponents).length;
    if (componentsCount < 8) {
        alert(`Выбрано компонентов: ${componentsCount} из 8. Выберите все компоненты!`);
        return;
    }

    const missingComponents = requiredComponents.filter(comp => !selectedComponents[comp]);

    if (missingComponents.length > 0) {
        alert('Выберите все компоненты:\n' + missingComponents.join('\n'));
        return;
    }

    const componentIds = Object.values(selectedComponents).map(comp => comp.id);

    try {
        const response = await fetch('/api/v1/build/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ component_ids: componentIds })
        });

        if (!response.ok) {
            throw new Error('Ошибка сервера');
        }

        const result = await response.json();

        if (result.compatible) {
            alert('Конфигурация совместима! Заказ создан.');

        } else {
            alert('Найдены конфликты:\n\n' + result.conflicts.join('\n'));
        }
    } catch (error) {
        console.error('Ошибка при проверке сборки:', error);
        alert('Произошла ошибка при проверке конфигурации. Попробуйте позже.');
    }
}

function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

loadComponents();
closeBtn.onclick = closeModal;

document.querySelectorAll('.open-modal-btn').forEach(btn => {
    btn.onclick = () => openModal(btn.dataset.component);
});

const buildButton = document.querySelector('.create-pc-button-container .btn');
if (buildButton) {
    buildButton.addEventListener('click', submitBuild);
}