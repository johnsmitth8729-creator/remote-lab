// Main JavaScript App File
document.addEventListener('DOMContentLoaded', () => {
    console.log("Remote Virtual Laboratory loaded successfully.");

    // Auto-hide alert messages after 5 seconds if they exist
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
});
