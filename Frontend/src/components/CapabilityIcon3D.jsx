import React from 'react';
import { Box } from '@mui/material';
import { motion } from 'framer-motion';

/**
 * Realistic 3D Capability Icon Component
 * Creates ultra-realistic 3D objects with:
 * - Bright whitish glowing shadows for depth
 * - Multiple light sources for realistic lighting
 * - Surface highlights and reflections
 * - Deep shadow casting for 3D effect
 * - Interactive animations
 */
const CapabilityIcon3D = ({ 
  icon, 
  size = 80, 
  children,
  variant = 'automation',
  ...props 
}) => {
  
  // Enhanced gradient variants with realistic lighting
  const gradientVariants = {
    automation: {
      background: `
        radial-gradient(ellipse at 25% 25%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.3) 30%, transparent 70%),
        radial-gradient(ellipse at 75% 75%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)
      `,
      shadowMain: 'rgba(255, 255, 255, 0.4)',
      shadowGlow: 'rgba(79, 172, 254, 0.6)',
      innerShadow: 'rgba(0, 0, 0, 0.3)'
    },
    selfhealing: {
      background: `
        radial-gradient(ellipse at 25% 25%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.3) 30%, transparent 70%),
        radial-gradient(ellipse at 75% 75%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)
      `,
      shadowMain: 'rgba(255, 255, 255, 0.4)',
      shadowGlow: 'rgba(16, 185, 129, 0.6)',
      innerShadow: 'rgba(0, 0, 0, 0.3)'
    },
    analytics: {
      background: `
        radial-gradient(ellipse at 25% 25%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.3) 30%, transparent 70%),
        radial-gradient(ellipse at 75% 75%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)
      `,
      shadowMain: 'rgba(255, 255, 255, 0.4)',
      shadowGlow: 'rgba(102, 126, 234, 0.6)',
      innerShadow: 'rgba(0, 0, 0, 0.3)'
    },
    intelligence: {
      background: `
        radial-gradient(ellipse at 25% 25%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.3) 30%, transparent 70%),
        radial-gradient(ellipse at 75% 75%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)
      `,
      shadowMain: 'rgba(255, 255, 255, 0.4)',
      shadowGlow: 'rgba(240, 147, 251, 0.6)',
      innerShadow: 'rgba(0, 0, 0, 0.3)'
    },
    security: {
      background: `
        radial-gradient(ellipse at 25% 25%, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.3) 30%, transparent 70%),
        radial-gradient(ellipse at 75% 75%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)
      `,
      shadowMain: 'rgba(255, 255, 255, 0.4)',
      shadowGlow: 'rgba(118, 75, 162, 0.6)',
      innerShadow: 'rgba(0, 0, 0, 0.3)'
    }
  };

  const currentVariant = gradientVariants[variant] || gradientVariants.automation;

  return (
    <motion.div
      whileHover={{ 
        scale: 1.1,
        rotateY: 12,
        rotateX: 8,
        z: 20,
        transition: { 
          duration: 0.4, 
          ease: [0.23, 1, 0.32, 1],
          type: "spring",
          stiffness: 200,
          damping: 20
        }
      }}
      whileTap={{ scale: 0.95 }}
      initial={{ 
        opacity: 0, 
        scale: 0.8, 
        rotateY: -30,
        z: -20
      }}
      animate={{ 
        opacity: 1, 
        scale: 1, 
        rotateY: 0,
        z: 0,
        transition: { 
          duration: 0.6, 
          ease: [0.23, 1, 0.32, 1] 
        }
      }}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
      {...props}
    >
      <Box
        sx={{
          width: size,
          height: size,
          borderRadius: `${size * 0.3}px`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: `${size * 0.3}rem`,
          position: 'relative',
          transformStyle: 'preserve-3d',
          transition: 'all 0.4s cubic-bezier(0.23, 1, 0.32, 1)',
          cursor: 'pointer',
          
          // Main realistic 3D background with multiple light sources
          background: currentVariant.background,
          
          // Ultra-realistic shadow system with bright white glowing
          boxShadow: `
            0 ${size * 0.02}px ${size * 0.04}px ${currentVariant.shadowMain},
            0 ${size * 0.08}px ${size * 0.16}px rgba(255, 255, 255, 0.35),
            0 ${size * 0.15}px ${size * 0.3}px ${currentVariant.shadowGlow},
            0 ${size * 0.25}px ${size * 0.5}px rgba(0, 0, 0, 0.25),
            0 ${size * 0.4}px ${size * 0.8}px rgba(0, 0, 0, 0.15),
            0 ${size * 0.6}px ${size * 1.2}px rgba(0, 0, 0, 0.1),
            inset 0 ${size * 0.01}px ${size * 0.02}px rgba(255, 255, 255, 0.9),
            inset 0 -${size * 0.01}px ${size * 0.02}px ${currentVariant.innerShadow},
            inset ${size * 0.01}px ${size * 0.01}px ${size * 0.02}px rgba(255, 255, 255, 0.6),
            inset -${size * 0.01}px -${size * 0.01}px ${size * 0.02}px rgba(0, 0, 0, 0.3)
          `,
          
          // Primary surface highlight (brightest white spot)
          '&::before': {
            content: '""',
            position: 'absolute',
            top: `${size * 0.08}px`,
            left: `${size * 0.12}px`,
            width: `${size * 0.35}px`,
            height: `${size * 0.25}px`,
            borderRadius: `${size * 0.2}px`,
            background: `
              radial-gradient(ellipse at center, 
                rgba(255, 255, 255, 0.95) 0%, 
                rgba(255, 255, 255, 0.7) 30%, 
                rgba(255, 255, 255, 0.3) 60%,
                transparent 100%
              )
            `,
            zIndex: 5,
            pointerEvents: 'none',
            filter: 'blur(0.5px)',
            transform: 'rotateX(-15deg) rotateY(10deg)',
          },
          
          // Secondary highlight for depth
          '&::after': {
            content: '""',
            position: 'absolute',
            top: `${size * 0.05}px`,
            right: `${size * 0.1}px`,
            width: `${size * 0.12}px`,
            height: `${size * 0.12}px`,
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.8)',
            zIndex: 4,
            pointerEvents: 'none',
            filter: 'blur(1px)',
          },
          
          // Enhanced hover effects with brighter glow
          '&:hover': {
            boxShadow: `
              0 ${size * 0.03}px ${size * 0.06}px rgba(255, 255, 255, 0.6),
              0 ${size * 0.12}px ${size * 0.24}px rgba(255, 255, 255, 0.4),
              0 ${size * 0.2}px ${size * 0.4}px ${currentVariant.shadowGlow.replace('0.6', '0.8')},
              0 ${size * 0.3}px ${size * 0.6}px rgba(0, 0, 0, 0.3),
              0 ${size * 0.5}px ${size * 1}px rgba(0, 0, 0, 0.15),
              inset 0 ${size * 0.015}px ${size * 0.03}px rgba(255, 255, 255, 0.9),
              inset 0 -${size * 0.015}px ${size * 0.03}px ${currentVariant.innerShadow.replace('0.3', '0.4')},
              inset ${size * 0.015}px ${size * 0.015}px ${size * 0.03}px rgba(255, 255, 255, 0.6),
              inset -${size * 0.015}px -${size * 0.015}px ${size * 0.03}px rgba(0, 0, 0, 0.3)
            `,
            '&::before': {
              background: `
                radial-gradient(ellipse at center, 
                  rgba(255, 255, 255, 1) 0%, 
                  rgba(255, 255, 255, 0.8) 30%, 
                  rgba(255, 255, 255, 0.4) 60%,
                  transparent 100%
                )
              `,
              filter: 'blur(0.3px)',
            },
            '&::after': {
              background: 'rgba(255, 255, 255, 0.95)',
              filter: 'blur(0.5px)',
            }
          },
          
          // Icon styling with enhanced white glow
          '& > *': {
            position: 'relative',
            zIndex: 6,
            color: 'white',
            filter: `
              drop-shadow(0 2px 4px rgba(0, 0, 0, 0.6))
              drop-shadow(0 0 8px rgba(255, 255, 255, 0.5))
              drop-shadow(0 0 16px rgba(255, 255, 255, 0.2))
            `,
            transition: 'all 0.3s ease',
          }
        }}
      >
        {/* Additional bright rim lighting */}
        <Box
          sx={{
            position: 'absolute',
            top: `${-size * 0.005}px`,
            left: `${-size * 0.005}px`,
            right: `${-size * 0.005}px`,
            bottom: `${-size * 0.005}px`,
            borderRadius: `${size * 0.305}px`,
            border: `1px solid rgba(255, 255, 255, 0.4)`,
            zIndex: 1,
            pointerEvents: 'none',
          }}
        />
        
        {/* Outer glow aura */}
        <Box
          sx={{
            position: 'absolute',
            top: `${-size * 0.15}px`,
            left: `${-size * 0.15}px`,
            right: `${-size * 0.15}px`,
            bottom: `${-size * 0.15}px`,
            borderRadius: `${size * 0.45}px`,
            background: `
              radial-gradient(circle, 
                rgba(255, 255, 255, 0.3) 0%, 
                ${currentVariant.shadowGlow.replace('0.6', '0.4')} 30%,
                transparent 70%
              )
            `,
            zIndex: -1,
            filter: 'blur(8px)',
            pointerEvents: 'none',
            opacity: 0.8,
          }}
        />
        
        {/* Deep shadow beneath */}
        <Box
          sx={{
            position: 'absolute',
            bottom: `${-size * 0.3}px`,
            left: `${size * 0.1}px`,
            right: `${size * 0.1}px`,
            height: `${size * 0.15}px`,
            borderRadius: '50%',
            background: 'rgba(0, 0, 0, 0.3)',
            filter: 'blur(6px)',
            zIndex: -2,
            pointerEvents: 'none',
          }}
        />
        
        {icon || children}
      </Box>
    </motion.div>
  );
};

export default CapabilityIcon3D;
