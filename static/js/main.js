// CloudSentinel MarketLink - Main JavaScript

document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll(".flash");

    flashMessages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = "0";
            message.style.transform = "translateY(-10px)";
        }, 4000);
    });
});