
// Funções CRUD para Profissionais
async function editProfessional(id) {
    try {
        const response = await fetch(`/api/professionals/${id}`);
        if (!response.ok) throw new Error('Erro ao buscar dados do profissional');

        const professional = await response.json();
        
        // Preencher o formulário de edição
        document.getElementById('edit-name').value = professional.name;
        document.getElementById('edit-specialty').value = professional.specialty;
        document.getElementById('edit-professional-id').value = professional.professional_id;
        document.getElementById('edit-email').value = professional.email;
        document.getElementById('edit-phone').value = professional.phone;
        
        // Configurar action do formulário
        document.getElementById('editProfessionalForm').action = `/professionals/${id}/edit`;
        
        // Abrir modal
        const modal = new bootstrap.Modal(document.getElementById('editProfessionalModal'));
        modal.show();
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao carregar dados do profissional');
    }
}

async function deleteProfessional(id) {
    if (confirm('Deseja realmente excluir este profissional?')) {
        try {
            const response = await fetch(`/professionals/${id}/delete`, {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error('Erro ao excluir profissional');
            
            window.location.reload();
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao excluir profissional');
        }
    }
}

// Validação do formulário
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});
