import React from 'react';
import { Box, Typography } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import { motion } from 'framer-motion';

/**
 * Unified PRISM ANALYTICS Logo Component
 * Props:
 *  - variant: 'inline' | 'stacked'
 *  - size: 'sm' | 'md' | 'lg'
 *  - animate: boolean (enable rotation)
 *  - pulseKey: number (optional external trigger for pulse)
 */
const sizeMap = {
  sm: { outer: 24, inner: 14, boxW: 30, boxH: 22, font: '0.95rem' },
  md: { outer: 30, inner: 18, boxW: 40, boxH: 30, font: '1.25rem' },
  lg: { outer: 40, inner: 24, boxW: 52, boxH: 40, font: '1.7rem' }
};

const Logo = ({ variant='inline', size='md', animate=true, pulse=false, sx={}, textColor='#FFFFFF' }) => {
  const dims = sizeMap[size] || sizeMap.md;
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, ...sx }}>
      <Box
        sx={{
          position: 'relative',
          width: dims.boxW,
          height: dims.boxH,
          '&:hover .gear-rot': { animationPlayState: animate ? 'paused' : 'running' }
        }}
      >
        <SettingsIcon
          className="gear-rot"
          sx={{
            position: 'absolute',
            left: 0,
            top: size === 'lg' ? 4 : 2,
            fontSize: dims.outer,
            color: '#66FFE0',
            filter: 'drop-shadow(0 2px 4px rgba(102,255,224,0.35))',
            animation: animate ? 'spinSlow 14s linear infinite' : 'none',
            '@keyframes spinSlow': {
              '0%': { transform: 'rotate(0deg)' },
              '100%': { transform: 'rotate(360deg)' }
            }
          }}
        />
        <SettingsIcon
          className="gear-rot"
          sx={{
            position: 'absolute',
            left: dims.outer/2 - dims.inner/3,
            top: dims.outer/2,
            fontSize: dims.inner,
            color: 'hsl(168, 100%, 55%)',
            opacity: 0.95,
            animation: animate ? 'spinFast 6.5s linear infinite' : 'none',
            '@keyframes spinFast': {
              '0%': { transform: 'rotate(0deg)' },
              '100%': { transform: 'rotate(-360deg)' }
            }
          }}
        />
      </Box>
      <Typography
        variant="h6"
        sx={{
          m: 0,
          p: 0,
          fontWeight: 700,
            fontSize: dims.font,
          letterSpacing: '1px',
          fontFamily: '"Orbitron", "Inter", sans-serif',
          background: 'linear-gradient(135deg, #4FC3F7 0%, #29B6F6 50%, #0277BD 100%)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          textShadow: 'none'
        }}
      >
        PRISM ANALYTICS
      </Typography>
    </Box>
  );
};

export default Logo;
