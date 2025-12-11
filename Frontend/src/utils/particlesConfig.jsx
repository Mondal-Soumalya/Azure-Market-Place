export const particlesConfig = {
  fpsLimit: 60,
  particles: {
    number: {
      value: 80,
      density: { enable: true, value_area: 800 }
    },
    color: {
      // Harmonized with new brand: space-like colors
      value: ['#66FFE0', '#66FFE0', '#6366F1', '#4F46E5', '#7C3AED']
    },
    shape: { type: "circle" },
    opacity: {
      value: { min: 0.05, max: 0.3 },
      animation: { 
        enable: true, 
        speed: 0.3, 
        minimumValue: 0.05, 
        sync: false 
      }
    },
    size: {
      value: { min: 0.5, max: 2.5 },
      animation: {
        enable: true,
        speed: 0.2,
        minimumValue: 0.5,
        sync: false
      }
    },
    links: {
      enable: true,
      distance: 150,
      color: "#66FFE0",
      opacity: 0.08,
      width: 0.8
    },
    move: {
      enable: true,
      speed: 0.5,
      direction: "none", 
      random: true, 
      straight: false,
      outModes: { default: "out" },
      attract: { enable: false },
      drift: 0.2,
      wobble: {
        enable: true,
        distance: 10,
        speed: 0.1
      }
    }
  },
  interactivity: {
    detectsOn: "canvas",
    events: {
      onHover: { enable: true, mode: "grab" },
      onClick: { enable: true, mode: "push" },
      resize: true
    },
    modes: {
      grab: { distance: 100, link_opacity: 0.2 },
      push: { quantity: 2 },
    }
  },
  detectRetina: true
};