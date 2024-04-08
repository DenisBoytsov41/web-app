document.addEventListener("DOMContentLoaded", function() {
    var themeToggle = document.querySelector('button[name="theme"]');
    if (themeToggle) {
        themeToggle.addEventListener("click", function() {
            this.textContent = this.textContent === "Темная тема" ? "Светлая тема" : "Темная тема";
        });
    }
});
