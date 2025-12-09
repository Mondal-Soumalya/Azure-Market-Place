// js/typing-init.js
document.addEventListener('DOMContentLoaded', function () {
    const typedElement = document.getElementById('typed-output');
    if (typedElement) {
        var options = {
            strings: [
                'Enterprise AI Automation.',
                'Intelligent Document Insights.',
                'Streamlined Workflows.',
                'Data-Driven Decisions.'
            ],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 1500,
            startDelay: 500,
            loop: true,
            smartBackspace: true,
            showCursor: true,
            cursorChar: '|',
            autoInsertCss: false // Assume cursor CSS is in style.css now
        };
        var typed = new Typed(typedElement, options);
    } else {
        console.warn("Typed.js target element '#typed-output' not found on this page.");
    }
});