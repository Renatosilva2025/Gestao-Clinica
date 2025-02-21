// Máscara para CPF
function maskCPF(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d)/, '$1.$2');
    value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    input.value = value;
}

// Máscara para telefone
function maskPhone(input) {
    let value = input.value.replace(/\D/g, '');
    value = value.replace(/^(\d{2})(\d)/g, '($1) $2');
    value = value.replace(/(\d)(\d{4})$/, '$1-$2');
    input.value = value;
}

// Formatação de moeda
function formatCurrency(input) {
    let value = input.value.replace(/\D/g, '');
    value = (parseFloat(value) / 100).toFixed(2);
    input.value = value;
}

// Validação de formulários
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar máscaras aos campos
    const cpfInputs = document.querySelectorAll('input[name="cpf"]');
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    const priceInputs = document.querySelectorAll('input[name="price"]');

    cpfInputs.forEach(input => {
        input.addEventListener('input', () => maskCPF(input));
    });

    phoneInputs.forEach(input => {
        input.addEventListener('input', () => maskPhone(input));
    });

    priceInputs.forEach(input => {
        input.addEventListener('input', () => formatCurrency(input));
    });

    // Validação de formulários
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(form)) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Função de validação de formulário
function validateForm(form) {
    let isValid = true;

    // Validar CPF
    const cpfInput = form.querySelector('input[name="cpf"]');
    if (cpfInput && !validateCPF(cpfInput.value)) {
        isValid = false;
        showError(cpfInput, 'CPF inválido');
    }

    // Validar email
    const emailInput = form.querySelector('input[name="email"]');
    if (emailInput && !validateEmail(emailInput.value)) {
        isValid = false;
        showError(emailInput, 'Email inválido');
    }

    // Validar telefone
    const phoneInput = form.querySelector('input[name="phone"]');
    if (phoneInput && !validatePhone(phoneInput.value)) {
        isValid = false;
        showError(phoneInput, 'Telefone inválido');
    }

    return isValid;
}

// Funções auxiliares de validação
function validateCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    return cpf.length === 11;
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    phone = phone.replace(/[^\d]/g, '');
    return phone.length >= 10 && phone.length <= 11;
}

function showError(input, message) {
    input.setCustomValidity(message);
    const feedback = input.parentElement.querySelector('.invalid-feedback') || 
                    document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    input.parentElement.appendChild(feedback);
}

// Funções CRUD para Clientes
async function editClient(id) {
    try {
        const response = await fetch(`/api/clients/${id}`);
        if (!response.ok) throw new Error('Erro ao buscar dados do cliente');

        const client = await response.json();

        // Preencher o formulário de edição
        document.getElementById('edit-name').value = client.name;
        document.getElementById('edit-email').value = client.email;
        document.getElementById('edit-phone').value = client.phone;
        document.getElementById('edit-cpf').value = client.cpf;

        // Configurar action do formulário
        document.getElementById('editClientForm').action = `/clients/${id}/edit`;

        // Abrir modal
        const modal = new bootstrap.Modal(document.getElementById('editClientModal'));
        modal.show();
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar dados do cliente');
    }
}

async function deleteClient(id) {
    if (confirm('Deseja realmente excluir este cliente?')) {
        try {
            const response = await fetch(`/clients/${id}/delete`, {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Erro ao excluir cliente');
            window.location.reload();
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao excluir cliente');
        }
    }
}

// Funções CRUD para Profissionais
async function editProfessional(id) {
    try {
        const response = await fetch(`/api/professionals/${id}`);
        if (!response.ok) throw new Error('Erro ao buscar dados do profissional');

        const professional = await response.json();
        const modal = new bootstrap.Modal(document.getElementById('editProfessionalModal'));

        // Preencher o modal de edição
        document.getElementById('edit-name').value = professional.name;
        document.getElementById('edit-specialty').value = professional.specialty;
        document.getElementById('edit-email').value = professional.email;
        document.getElementById('edit-phone').value = professional.phone;

        // Configurar o formulário para edição
        const form = document.getElementById('editProfessionalForm');
        form.setAttribute('action', `/professionals/${id}/edit`);

        modal.show();
    } catch (error) {
        showAlert('Erro ao carregar dados do profissional', 'danger');
        console.error(error);
    }
}

async function deleteProfessional(id) {
    if (confirm('Deseja realmente excluir este profissional?')) {
        try {
            const response = await fetch(`/professionals/${id}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) throw new Error('Erro ao excluir profissional');

            showAlert('Profissional excluído com sucesso', 'success');
            setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            showAlert('Erro ao excluir profissional', 'danger');
            console.error(error);
        }
    }
}

// Funções CRUD para Procedimentos
async function editProcedure(id) {
    try {
        const response = await fetch(`/api/procedures/${id}`);
        if (!response.ok) throw new Error('Erro ao buscar dados do procedimento');

        const procedure = await response.json();
        const modal = new bootstrap.Modal(document.getElementById('editProcedureModal'));

        // Preencher o modal de edição
        document.getElementById('edit-name').value = procedure.name;
        document.getElementById('edit-description').value = procedure.description;
        document.getElementById('edit-duration').value = procedure.duration;
        document.getElementById('edit-price').value = procedure.price;

        // Configurar o formulário para edição
        const form = document.getElementById('editProcedureForm');
        form.setAttribute('action', `/procedures/${id}/edit`);

        modal.show();
    } catch (error) {
        showAlert('Erro ao carregar dados do procedimento', 'danger');
        console.error(error);
    }
}

async function deleteProcedure(id) {
    if (confirm('Deseja realmente excluir este procedimento?')) {
        try {
            const response = await fetch(`/procedures/${id}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) throw new Error('Erro ao excluir procedimento');

            showAlert('Procedimento excluído com sucesso', 'success');
            setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            showAlert('Erro ao excluir procedimento', 'danger');
            console.error(error);
        }
    }
}

// Função auxiliar para mostrar alertas
function showAlert(message, type) {
    const alertPlaceholder = document.getElementById('alertPlaceholder') || createAlertPlaceholder();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    alertPlaceholder.appendChild(wrapper);
}

function createAlertPlaceholder() {
    const placeholder = document.createElement('div');
    placeholder.id = 'alertPlaceholder';
    placeholder.style.position = 'fixed';
    placeholder.style.top = '20px';
    placeholder.style.right = '20px';
    placeholder.style.zIndex = '9999';
    document.body.appendChild(placeholder);
    return placeholder;
}