import { createTheme } from '@mui/material/styles';
import { designTokens } from './designTokens';

// Professional Design System - Sophisticated color palette inspired by top-tier design companies
const professionalPalette = {
  dark: {
    // Core brand colors - sophisticated and mature
    primary: '#6366f1',        // Professional indigo - trustworthy and modern
    secondary: '#8b5cf6',      // Refined purple - creative and premium
    
    // Background hierarchy - deep and elegant
    background: '#1e2a3a',     // Navy blue background - professional depth
    surface: '#181832',        // Elevated surface - subtle contrast
    surfaceLight: '#242449',   // Light surface variant - layered depth
    
    // Text hierarchy - clear and readable
    text: '#f1f5f9',          // Clean white text - high contrast
    textSecondary: '#cbd5e1',  // Muted text - supporting information
    textMuted: '#94a3b8',     // Very muted text - least important
    
    // UI elements
    border: '#334155',         // Subtle borders - elegant separation
    accent: '#06b6d4',         // Cyan accent - attention grabbing
    accentSecondary: '#10b981', // Emerald accent - success/positive
    
    // Advanced gradients - premium feel
    gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
    gradientBg: 'linear-gradient(135deg, #0f0f23 0%, #181832 100%)',
    gradientAccent: 'linear-gradient(135deg, #06b6d4 0%, #10b981 100%)',
    gradientHero: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)',
    
    // Shadows - professional depth
    shadow: 'rgba(99, 102, 241, 0.15)',
    shadowLight: 'rgba(0, 0, 0, 0.25)',
    shadowHeavy: 'rgba(0, 0, 0, 0.4)',
    
    // Status colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#06b6d4'
  },
  light: {
    // Core brand colors - professional and accessible
    primary: '#4f46e5',        // Rich indigo - maintains brand identity
    secondary: '#7c3aed',      // Deep purple - sophisticated accent
    
    // Background hierarchy - clean and minimal
    background: '#fafafa',     // Clean light background - modern minimalism
    surface: '#ffffff',       // Pure white surface - clean canvas
    surfaceLight: '#f8fafc',  // Subtle surface variant - gentle layering
    
    // Text hierarchy - professional readability
    text: '#0f172a',          // Deep text - excellent contrast
    textSecondary: '#475569',  // Medium text - balanced hierarchy
    textMuted: '#64748b',     // Light text - supporting content
    
    // UI elements
    border: '#e2e8f0',       // Light borders - subtle definition
    accent: '#0891b2',        // Professional cyan - modern accent
    accentSecondary: '#059669', // Professional emerald - positive actions
    
    // Advanced gradients - clean and professional
    gradient: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
    gradientBg: 'linear-gradient(135deg, #fafafa 0%, #f8fafc 100%)',
    gradientAccent: 'linear-gradient(135deg, #0891b2 0%, #059669 100%)',
    gradientHero: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0891b2 100%)',
    
    // Shadows - subtle and refined
    shadow: 'rgba(79, 70, 229, 0.1)',
    shadowLight: 'rgba(0, 0, 0, 0.08)',
    shadowHeavy: 'rgba(0, 0, 0, 0.15)',
    
    // Status colors
    success: '#059669',
    warning: '#d97706',
    error: '#dc2626',
    info: '#0891b2'
  }
};

// Professional typography system - inspired by premium design systems
const createTypographySystem = (isDarkMode) => ({
  fontFamily: '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  fontWeightLight: 300,
  fontWeightRegular: 400,
  fontWeightMedium: 500,
  fontWeightSemiBold: 600,
  fontWeightBold: 700,
  
  // Display typography - hero sections and major headings
  h1: {
    fontSize: 'clamp(2.5rem, 6vw, 4rem)',
    fontWeight: 700,
    lineHeight: 1.1,
    letterSpacing: '-0.025em',
    '@media (max-width: 768px)': {
      fontSize: 'clamp(2rem, 8vw, 2.5rem)',
    }
  },
  
  // Section headings
  h2: {
    fontSize: 'clamp(2rem, 4vw, 3rem)',
    fontWeight: 600,
    lineHeight: 1.2,
    letterSpacing: '-0.02em',
    '@media (max-width: 768px)': {
      fontSize: 'clamp(1.75rem, 6vw, 2rem)',
    }
  },
  
  // Subsection headings
  h3: {
    fontSize: 'clamp(1.5rem, 3vw, 2.25rem)',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.015em',
    '@media (max-width: 768px)': {
      fontSize: 'clamp(1.375rem, 5vw, 1.5rem)',
    }
  },
  
  // Card titles and component headings
  h4: {
    fontSize: 'clamp(1.25rem, 2.5vw, 1.75rem)',
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '-0.01em',
  },
  
  // Small headings
  h5: {
    fontSize: 'clamp(1.125rem, 2vw, 1.375rem)',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  
  h6: {
    fontSize: 'clamp(1rem, 1.5vw, 1.125rem)',
    fontWeight: 600,
    lineHeight: 1.5,
  },
  
  // Body text - optimized for readability
  body1: {
    fontSize: '1rem',
    lineHeight: 1.6,
    fontWeight: 400,
    '@media (max-width: 768px)': {
      fontSize: '0.9rem',
      lineHeight: 1.7,
    }
  },
  
  body2: {
    fontSize: '0.875rem',
    lineHeight: 1.5,
    fontWeight: 400,
    '@media (max-width: 768px)': {
      fontSize: '0.825rem',
    }
  },
  
  // UI text
  caption: {
    fontSize: '0.75rem',
    lineHeight: 1.4,
    fontWeight: 400,
    opacity: 0.8,
  },
  
  button: {
    fontSize: '0.875rem',
    fontWeight: 600,
    textTransform: 'none',
    letterSpacing: '0.01em',
    '@media (max-width: 768px)': {
      fontSize: '0.9rem',
    }
  },
  
  // Additional professional typography
  subtitle1: {
    fontSize: '1.125rem',
    lineHeight: 1.5,
    fontWeight: 400,
  },
  
  subtitle2: {
    fontSize: '0.875rem',
    lineHeight: 1.4,
    fontWeight: 500,
  },
});

// Professional component overrides - inspired by top design systems
const createComponentOverrides = (colors, isDarkMode) => ({
  // Buttons - professional and accessible
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 12,
        padding: '12px 24px',
        fontWeight: 600,
        textTransform: 'none',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        minHeight: 48,
        boxShadow: 'none',
        '@media (max-width: 768px)': {
          padding: '14px 28px',
          minHeight: 52,
          fontSize: '0.9rem',
        },
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: `0 8px 25px ${colors.shadow}`,
        },
        '&:active': {
          transform: 'translateY(0)',
        }
      },
      contained: {
        background: colors.gradient,
        color: isDarkMode ? '#ffffff' : '#ffffff',
        '&:hover': {
          background: colors.gradient,
          boxShadow: `0 12px 30px ${colors.shadow}`,
        }
      },
      outlined: {
        borderColor: colors.primary,
        color: colors.primary,
        borderWidth: '2px',
        '&:hover': {
          backgroundColor: `${colors.primary}10`,
          borderWidth: '2px',
        }
      },
      text: {
        color: colors.textSecondary,
        '&:hover': {
          backgroundColor: `${colors.primary}08`,
          color: colors.primary,
        }
      }
    }
  },

  // Cards - elegant and modern
  MuiCard: {
    styleOverrides: {
      root: {
        background: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: 20,
        transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
        boxShadow: `0 4px 20px ${colors.shadowLight}`,
        '@media (max-width: 768px)': {
          borderRadius: 16,
        },
        '&:hover': {
          transform: 'translateY(-6px)',
          boxShadow: `0 20px 40px ${colors.shadow}`,
          borderColor: colors.primary + '40',
          '@media (max-width: 768px)': {
            transform: 'translateY(-3px)',
            boxShadow: `0 12px 25px ${colors.shadow}`,
          }
        }
      }
    }
  },

  // Card content - proper spacing
  MuiCardContent: {
    styleOverrides: {
      root: {
        padding: '32px',
        '@media (max-width: 768px)': {
          padding: '24px',
        },
        '&:last-child': {
          paddingBottom: '32px',
          '@media (max-width: 768px)': {
            paddingBottom: '24px',
          }
        }
      }
    }
  },

  // App bar - premium navigation
  MuiAppBar: {
    styleOverrides: {
      root: {
        background: `${colors.background}95`,
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${colors.border}`,
        boxShadow: `0 4px 20px ${colors.shadowLight}`,
      }
    }
  },

  // Text fields - professional forms
  MuiTextField: {
    styleOverrides: {
      root: {
        '& .MuiOutlinedInput-root': {
          borderRadius: 12,
          fontSize: '0.9rem',
          transition: 'all 0.3s ease',
          '@media (max-width: 768px)': {
            fontSize: '1rem',
            borderRadius: 8,
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: colors.primary,
            borderWidth: '2px',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: colors.primary,
            borderWidth: '2px',
            boxShadow: `0 0 0 3px ${colors.primary}20`,
          }
        }
      }
    }
  },

  // Chips - modern tags
  MuiChip: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        fontWeight: 500,
        fontSize: '0.75rem',
        '@media (max-width: 768px)': {
          fontSize: '0.7rem',
          height: '32px',
        }
      }
    }
  },

  // Container - proper spacing
  MuiContainer: {
    styleOverrides: {
      root: {
        paddingLeft: '24px',
        paddingRight: '24px',
        '@media (max-width: 768px)': {
          paddingLeft: '16px',
          paddingRight: '16px',
        }
      }
    }
  },

  // Paper - consistent surfaces
  MuiPaper: {
    styleOverrides: {
      root: {
        background: colors.surface,
        border: `1px solid ${colors.border}`,
        borderRadius: 16,
      }
    }
  },
});

// Create professional theme (updated to use semantic design tokens phase 1)
export const createProfessionalTheme = (isDarkMode = true) => {
  const mode = isDarkMode ? 'dark' : 'light';
  const tokens = designTokens[mode];
  const colors = isDarkMode ? professionalPalette.dark : professionalPalette.light; // retain legacy for now

  return createTheme({
    palette: {
      mode: isDarkMode ? 'dark' : 'light',
      primary: {
        main: tokens.color.accent.primary,
        light: tokens.color.accent.primaryHover,
        dark: tokens.color.accent.primary,
        contrastText: '#ffffff',
      },
      secondary: {
        main: colors.secondary,
        light: colors.accent,
        dark: colors.secondary,
        contrastText: '#ffffff',
      },
      background: {
        default: tokens.color.bg.base,
        paper: tokens.color.surface[2],
      },
      surface: {
        main: tokens.color.surface[2],
        light: tokens.color.surface[3],
      },
      text: {
        primary: tokens.color.text.primary,
        secondary: tokens.color.text.secondary,
        disabled: tokens.color.text.tertiary,
      },
      divider: tokens.color.border.subtle,
      success: { main: tokens.color.support.success },
      warning: { main: tokens.color.support.warning },
      error: { main: tokens.color.support.danger },
      info: { main: tokens.color.support.info },
      accent: {
        main: tokens.color.accent.primary,
        secondary: colors.accentSecondary,
      }
    },
    breakpoints: {
      values: { 
        xs: 0, 
        sm: 600, 
        md: 900, 
        lg: 1200, 
        xl: 1536 
      },
    },
    typography: createTypographySystem(isDarkMode),
    shape: { 
      borderRadius: 12 
    },
    shadows: [
      'none',
      tokens.elevation[1],
      tokens.elevation[2],
      tokens.elevation[3],
      tokens.elevation[4],
      tokens.elevation[5],
      tokens.elevation[6],
      ...Array(18).fill('none'),
    ],
    components: createComponentOverrides(colors, isDarkMode),
  });
};

// Export theme variants
export const createDarkTheme = () => createProfessionalTheme(true);
export const createLightTheme = () => createProfessionalTheme(false);
export const professionalDarkTheme = createDarkTheme();
export const professionalLightTheme = createLightTheme();

// Export color palette for direct access
export { professionalPalette };
