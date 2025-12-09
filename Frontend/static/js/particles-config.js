// js/particles-config.js (Blue AI Theme)
tsParticles.load("particles-js", {
    fpsLimit: 60,
    particles: {
        number: {
            value: 50, // Keep density moderate
            density: { enable: true, value_area: 800 }
        },
        color: {
            // Use blues and cyan accent
            value: ["#172a45", "#233554", "#64ffda"] // Corresponds to bg-tertiary, border-color, accent-primary
        },
        shape: { type: "circle" },
        opacity: {
            value: { min: 0.1, max: 0.4 }, // Range for opacity
            animation: { enable: true, speed: 0.5, minimumValue: 0.1, sync: false }
        },
        size: {
            value: { min: 1, max: 3 }, // Range for size
        },
        links: {
            enable: true,
            distance: 130,
            color: "#a8b2d1", // Use text-muted color for links
            opacity: 0.15, // Make links very subtle
            width: 1
        },
        move: {
            enable: true,
            speed: 1.2, // Slightly faster
            direction: "none", random: true, straight: false,
            outModes: { default: "out" }, // Use new property name
            attract: { enable: false }
        }
    },
    interactivity: {
        detectsOn: "canvas", // Use new property name
        events: {
            onHover: { enable: true, mode: "grab" },
            onClick: { enable: true, mode: "push" },
            resize: true
        },
        modes: {
            grab: { distance: 120, link_opacity: 0.3 }, // Grab links slightly more visible
            push: { quantity: 3 }, // Push fewer particles
        }
    },
    detectRetina: true
});