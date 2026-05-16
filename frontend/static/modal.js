const modalOverlay = document.getElementById('modalOverlay');
const closeModalButton = document.getElementById('closeModal');
const modalTitle = document.getElementById('modalTitle');
const modalContent = document.getElementById('modalContent');

//Переменная для хранения загруженных компонентов
let componentsData = null;

function openModal(componentName) {
    modalTitle.textContent = `${componentName}`;
    modalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    showComponentsForCategory(componentName);
}

function closeModal() {
    modalOverlay.classList.remove('active');
    document.body.style.overflow = '';
}

//Загрузка JSON файла
async function loadComponents() {
    try {
        const response = await fetch('/static/components.json');
        componentsData = await response.json();
    } catch (error) {
        console.error('Ошибка загрузки компонентов:', error);
        modalContent.innerHTML = '<div class="error-message">Ошибка загрузки компонентов</div>';
    }
}

function showComponentsForCategory(categoryName) {
    if (!componentsData) {
        return;
    }
    const category = componentsData.components.find(cat => cat.category === categoryName);
    let html = '<div class="components-list">';
    category.items.forEach(item => {
        html += `
            <div class="component-item">
                <div class="component-name">${item.name}</div>
                <div class="component-description">${item.description}</div>
                <div class="component-price"> ${item.price}</div>
                <button class="select-btn" onclick="selectComponent(${item.id}, '${item.name.replace(/'/g, "\\'")}')">Выбрать</button>
            </div>
        `;
    });

    html += '</div>';
    modalContent.innerHTML = html;
}

window.selectComponent = function(id, name) {
    closeModal();
};

loadComponents();
const modalButtons = document.querySelectorAll('.open-modal-btn');

//обработчик для каждой кнопки
modalButtons.forEach(button => {
    button.addEventListener('click', function() {
        const componentName = this.getAttribute('data-component');
        openModal(componentName);
    });
});

closeModalButton.addEventListener('click', closeModal);
