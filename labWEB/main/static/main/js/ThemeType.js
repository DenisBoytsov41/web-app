document.addEventListener("DOMContentLoaded", function() {
    $("#themeToggle").click(function(){
        $("body").toggleClass("dark-mode");
        var currentTheme = $("#themeToggle").text();
        var newTheme = currentTheme === "Темная тема" ? "Светлая тема" : "Темная тема";
        $("#themeToggle").text(newTheme);
    });
});
