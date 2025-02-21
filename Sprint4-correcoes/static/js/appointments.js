
function editAppointment(id) {
    fetch(`/api/appointments/${id}`)
        .then(response => response.json())
        .then(data => {
            const form = document.getElementById('editAppointmentForm');
            form.action = `/appointments/${id}/edit`;
            
            document.getElementById('edit-client').value = data.client_id;
            document.getElementById('edit-professional').value = data.professional_id;
            document.getElementById('edit-procedure').value = data.procedure_id;
            document.getElementById('edit-status').value = data.status;
            
            const dateTime = new Date(data.date_time);
            document.getElementById('edit-date').value = dateTime.toISOString().split('T')[0];
            document.getElementById('edit-time').value = dateTime.toTimeString().slice(0,5);
            
            const modal = new bootstrap.Modal(document.getElementById('editAppointmentModal'));
            modal.show();
        });
}

function deleteAppointment(id) {
    if (confirm('Tem certeza que deseja excluir este agendamento?')) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/appointments/${id}/delete`;
        document.body.appendChild(form);
        form.submit();
    }
}
