// Main JavaScript App File
document.addEventListener('DOMContentLoaded', () => {
    console.log("Remote Virtual Laboratory loaded successfully.");

    // Auto-hide alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });

    // ===== MOBILE DRAWER =====
    const openDrawerBtn = document.getElementById('openDrawerBtn');
    const closeDrawerBtn = document.getElementById('closeDrawerBtn');
    const mobileDrawer = document.getElementById('mobileDrawer');
    const drawerOverlay = document.getElementById('drawerOverlay');

    function openDrawer() {
        if (mobileDrawer) mobileDrawer.classList.add('open');
        if (drawerOverlay) drawerOverlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        if (mobileDrawer) mobileDrawer.classList.remove('open');
        if (drawerOverlay) drawerOverlay.classList.remove('open');
        document.body.style.overflow = '';
    }

    if (openDrawerBtn) openDrawerBtn.addEventListener('click', openDrawer);
    if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
    if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

    // Close drawer on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDrawer();
    });
});
