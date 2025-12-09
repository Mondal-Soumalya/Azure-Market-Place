// js/script-index.js
document.addEventListener('DOMContentLoaded', function () {

    // Sticky Header Background on Scroll (Optional, less needed with fixed)
    // const header = document.querySelector('.app-header.sticky-header');
    // if (header) {
    //     window.addEventListener('scroll', () => {
    //         if (window.scrollY > 50) {
    //             header.style.backgroundColor = 'rgba(10, 25, 47, 0.95)'; // Adjust alpha based on theme var if needed
    //         } else {
    //             header.style.backgroundColor = 'rgba(10, 25, 47, 0.85)';
    //         }
    //     });
    // }

    // Smooth scrolling for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const hrefAttribute = this.getAttribute('href');
            if (hrefAttribute && hrefAttribute.length > 1 && hrefAttribute !== '#') {
                const targetElement = document.querySelector(hrefAttribute);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

});