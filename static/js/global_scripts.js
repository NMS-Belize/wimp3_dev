$(function() {

    let sidebarCollapsed = true;
        
    // Auto dismiss alerts
    document.querySelectorAll(".alert").forEach(function(alert) {
        setTimeout(function() {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 5000);
    });

    const sidebar = document.querySelector('.sidebar');

    if (!sidebar) return;

    // Expand temporarily on hover
    sidebar.addEventListener('mouseenter', function() {
        if (sidebarCollapsed) {
            sidebar.classList.remove('collapsed');
        }
    });

    // Collapse again when mouse leaves
    sidebar.addEventListener('mouseleave', function() {
        if (sidebarCollapsed) {
            sidebar.classList.add('collapsed');
        }
    });

    // Expose function globally because onclick="toggleSidebar()" is in HTML
    window.toggleSidebar = function() {
        sidebarCollapsed = !sidebarCollapsed;

        sidebar.classList.toggle(
            'collapsed',
            sidebarCollapsed
        );
    };
    
    function toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebarCollapsed = !sidebarCollapsed;
        sidebar.classList.toggle('collapsed', sidebarCollapsed);
    }
});