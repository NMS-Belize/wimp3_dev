let sidebarCollapsed = true;

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');

    if (!sidebar) {
        console.error('Sidebar not found');
        return;
    }

    sidebarCollapsed = !sidebarCollapsed;

    sidebar.classList.toggle('collapsed', sidebarCollapsed);

    const icon = document.querySelector('.toggle-btn i');

    if (icon) {
        if (sidebarCollapsed) {
            icon.classList.remove('fa-chevron-left');
            icon.classList.add('fa-chevron-right');
        } else {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-left');
        }
    }
}


$(function () {

    const sidebar = document.querySelector('.sidebar');

    if (!sidebar) {
        console.error('Sidebar not found');
        return;
    }

    // Start collapsed
    sidebar.classList.add('collapsed');


    // Auto dismiss alerts
    document.querySelectorAll(".auto-dismiss").forEach(function (alert) {
        setTimeout(function () {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 5000);
    });


    sidebar.addEventListener('mouseenter', function (event) {

        if (!sidebarCollapsed) {
            return;
        }

        const collapsedWidth = parseInt(
            getComputedStyle(document.documentElement)
                .getPropertyValue('--sidebar-width-collapsed')
        );

        if (event.clientX <= collapsedWidth) {
            sidebar.classList.remove('collapsed');
        }
    });

    // Collapse again when mouse leaves
    sidebar.addEventListener('mouseleave', function () {

        if (sidebarCollapsed) {
            sidebar.classList.add('collapsed');
        }

    });

});