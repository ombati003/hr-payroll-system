// Global navigation handling
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const navItems = document.querySelectorAll('nav a');
    
    navItems.forEach(item => {
        item.classList.remove('bg-blue-600', 'text-white');
        if (item.getAttribute('href') === path) {
            item.classList.add('bg-blue-600', 'text-white');
            document.getElementById('page-title').textContent = item.textContent.trim();
        }
    });

    // Set current date
    const dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', dateOptions);
});
