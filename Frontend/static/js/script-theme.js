// js/script-theme.js
document.addEventListener('DOMContentLoaded', () => {
    const themeCheckbox = document.getElementById('theme-checkbox');
    const body = document.body;
    const defaultDarkThemeClass = 'blue-theme'; // Your default dark theme class
    const lightThemeClass = 'light-mode';

    // Function to apply theme based on state
    const applyTheme = (isLightMode) => {
        if (isLightMode) {
            body.classList.add(lightThemeClass);
            body.classList.remove(defaultDarkThemeClass);
        } else {
            body.classList.remove(lightThemeClass);
            body.classList.add(defaultDarkThemeClass);
        }
        // Update checkbox state visually
        if (themeCheckbox) {
            themeCheckbox.checked = isLightMode;
        }
    };

    // Check localStorage for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    // Check OS preference
    let prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
    let currentThemeIsLight;

    if (savedTheme) {
        // Use saved theme if it exists
        currentThemeIsLight = (savedTheme === 'light');
    } else {
        // Otherwise, use OS preference as default
        currentThemeIsLight = prefersLight;
        // Optionally save the detected OS preference as the initial setting
        // localStorage.setItem('theme', currentThemeIsLight ? 'light' : 'dark');
    }

    // Apply the determined theme on initial load
    applyTheme(currentThemeIsLight);

    // Add listener for the theme toggle checkbox change
    if (themeCheckbox) {
        themeCheckbox.addEventListener('change', () => {
            const isLight = themeCheckbox.checked;
            applyTheme(isLight);
            // Save the user's choice to localStorage
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        });
    }

    // Optional: Listen for OS theme changes and update if no manual override exists
    // Note: This might feel slightly unexpected to users if they manually toggled.
    // Consider commenting this out if the manual toggle should always take precedence.
    // window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', event => {
    //     const osPrefersLight = event.matches;
    //     // Only update based on OS change if there's no saved user preference
    //     // or if the saved preference matches the new OS preference (less common scenario)
    //     const currentSavedTheme = localStorage.getItem('theme');
    //     if (currentSavedTheme === null || currentSavedTheme === (osPrefersLight ? 'light' : 'dark')) {
    //          applyTheme(osPrefersLight);
    //          // Optionally update localStorage to reflect OS change when no manual toggle made
    //          // localStorage.setItem('theme', osPrefersLight ? 'light' : 'dark');
    //     }
    // });
});