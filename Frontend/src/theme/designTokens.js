// designTokens.js - Semantic design token system (Phase 1)
// Purpose: decouple raw palette values from component usage; enable future palette iteration

const neutralDark = [
  '#0E1113', '#161B1E', '#1F2529', '#2A3136', '#364047', '#46525A', '#5A6872', '#6E7D88', '#8896A1', '#A7B3BC', '#C5CED4', '#E2E7EA'
];
const neutralLight = [
  '#FFFFFF', '#F5F7FA', '#EDF1F5', '#E4EAF0', '#D8E0E7', '#CBD5DD', '#B8C4CE', '#A5B2BD', '#8E9CA7', '#76848F', '#5E6B75', '#48535B'
];

// Brand & functional base (can be tuned later)
const brand = {
  primary: {
    50: '#EEF0FF', 100: '#E0E3FF', 200: '#C2C6FF', 300: '#A4A9FF', 400: '#858CFF',
    500: '#6366F1', 600: '#4F51DA', 700: '#3A3DB7', 800: '#2E318F', 900: '#232667'
  },
  accent: {
    cyan: '#06B6D4', cyanDark: '#0891B2', teal: '#10B981'
  },
  states: {
    success: '#2FAF72', warning: '#D88A1A', danger: '#D14B55', info: '#3C8DFF'
  }
};

export const designTokens = {
  dark: {
    mode: 'dark',
    color: {
      bg: { base: neutralDark[0], alt: neutralDark[1], subtle: neutralDark[2] },
      surface: { 0: 'transparent', 1: neutralDark[2], 2: neutralDark[3], 3: neutralDark[4], 4: neutralDark[5], 5: neutralDark[6] },
      border: { subtle: neutralDark[3], normal: neutralDark[4], strong: neutralDark[6] },
      text: { primary: '#F1F5F9', secondary: '#CBD5E1', tertiary: '#94A3B8', inverse: neutralDark[0] },
      accent: { primary: brand.primary[500], primaryHover: brand.primary[400], focusOuter: 'rgba(99,102,241,0.45)', focusInner: '#FFFFFF' },
      support: { ...brand.states },
      gradient: {
        brandSm: 'linear-gradient(135deg,#6366F1 0%,#7C3AED 100%)',
        brandXl: 'linear-gradient(135deg,#6366F1 0%,#8B5CF6 50%,#06B6D4 100%)'
      },
      shadowTint: 'rgba(0,0,0,0.65)',
      ring: { outer: 'rgba(99,102,241,0.5)', inner: '#1F2529' }
    },
    motion: { duration: { fast: 120, base: 200, slow: 320 }, easing: { standard: 'cubic-bezier(.4,.2,.2,1)', enter: 'cubic-bezier(.4,0,.2,1)', exit: 'cubic-bezier(.4,0,.6,1)' } },
    elevation: [
      'none',
      '0 1px 2px -1px rgba(0,0,0,0.4),0 1px 3px rgba(0,0,0,0.25)',
      '0 2px 4px -1px rgba(0,0,0,0.45),0 3px 6px rgba(0,0,0,0.3)',
      '0 4px 10px -2px rgba(0,0,0,0.5),0 6px 16px rgba(0,0,0,0.35)',
      '0 8px 18px -4px rgba(0,0,0,0.55),0 10px 28px rgba(0,0,0,0.4)',
      '0 12px 32px -6px rgba(0,0,0,0.6),0 18px 40px rgba(0,0,0,0.45)',
      '0 18px 48px -8px rgba(0,0,0,0.65),0 28px 64px rgba(0,0,0,0.5)'
    ]
  },
  light: {
    mode: 'light',
    color: {
      bg: { base: neutralLight[1], alt: neutralLight[0], subtle: neutralLight[2] },
      surface: { 0: 'transparent', 1: neutralLight[0], 2: neutralLight[2], 3: neutralLight[3], 4: neutralLight[4], 5: neutralLight[5] },
      border: { subtle: '#DCE2E8', normal: '#CBD5DD', strong: '#A5B2BD' },
      text: { primary: '#0F172A', secondary: '#475569', tertiary: '#64748B', inverse: '#FFFFFF' },
      accent: { primary: '#4F46E5', primaryHover: '#5B61F6', focusOuter: 'rgba(99,102,241,0.55)', focusInner: '#FFFFFF' },
      support: { ...brand.states },
      gradient: {
        brandSm: 'linear-gradient(135deg,#4F46E5 0%,#7C3AED 100%)',
        brandXl: 'linear-gradient(135deg,#4F46E5 0%,#7C3AED 50%,#0891B2 100%)'
      },
      shadowTint: 'rgba(15,23,42,0.15)',
      ring: { outer: 'rgba(99,102,241,0.55)', inner: '#FFFFFF' }
    },
    motion: { duration: { fast: 120, base: 200, slow: 320 }, easing: { standard: 'cubic-bezier(.4,.2,.2,1)', enter: 'cubic-bezier(.4,0,.2,1)', exit: 'cubic-bezier(.4,0,.6,1)' } },
    elevation: [
      'none',
      '0 1px 2px -1px rgba(15,23,42,0.12),0 1px 3px rgba(15,23,42,0.08)',
      '0 2px 4px -1px rgba(15,23,42,0.15),0 3px 6px rgba(15,23,42,0.10)',
      '0 4px 10px -2px rgba(15,23,42,0.18),0 6px 16px rgba(15,23,42,0.12)',
      '0 8px 18px -4px rgba(15,23,42,0.22),0 10px 28px rgba(15,23,42,0.16)',
      '0 12px 32px -6px rgba(15,23,42,0.26),0 18px 40px rgba(15,23,42,0.20)',
      '0 18px 48px -8px rgba(15,23,42,0.30),0 28px 64px rgba(15,23,42,0.24)'
    ]
  }
};

export const getDesignTokens = (mode = 'dark') => designTokens[mode];

// Utility: elevation style retrieval
export const getElevation = (mode, level = 0) => ({
  boxShadow: designTokens[mode].elevation[Math.min(level, designTokens[mode].elevation.length - 1)]
});

// Focus ring helper
export const focusRingStyle = (mode) => ({
  boxShadow: `0 0 0 3px ${designTokens[mode].color.accent.focusOuter}, 0 0 0 1.5px ${designTokens[mode].color.accent.primary}`
});
