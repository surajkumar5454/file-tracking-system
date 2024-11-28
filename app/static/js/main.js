// Confirm delete action
function confirmDelete(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        // Send delete request
        fetch(`/admin/users/${userId}/delete`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    }
}

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.getElementsByClassName('alert');
        for (let alert of alerts) {
            alert.style.display = 'none';
        }
    }, 5000);
});

// Dynamic form validation
const forms = document.getElementsByTagName('form');
for (let form of forms) {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
} 