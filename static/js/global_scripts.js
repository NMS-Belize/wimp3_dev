document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".auto-dismiss").forEach(function(alert) {
        setTimeout(function() {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }, 5000);
    });
});

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}