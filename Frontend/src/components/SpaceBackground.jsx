import React from 'react';
import { Box } from '@mui/material';

/**
 * SpaceBackground Component
 * Creates a sophisticated three-layer deep space background with:
 * - Layer 1: Far away main stars with atmospheric effects
 * - Layer 2: Very distant twinkling stars
 * - Layer 3: Ultra distant star field
 * - Realistic distance effects with microscopic star sizes
 * - Atmospheric blur and vast spacing patterns
 * - Slow drift animations for immersive depth
 */
const SpaceBackground = ({ children, ...props }) => {
  return (
    <Box
      sx={{
        position: 'relative',
        minHeight: '100vh',
        overflow: 'hidden',
        backgroundColor: '#1e2a3a',
        ...props.sx
      }}
      {...props}
    >
      {/* Layer 1: Far away main stars with atmospheric blur */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(0.1px 0.1px at 20px 30px, rgba(255,255,255,0.08), transparent),
            radial-gradient(0.2px 0.2px at 120px 80px, rgba(255,255,255,0.12), transparent),
            radial-gradient(0.15px 0.15px at 200px 150px, rgba(255,255,255,0.1), transparent),
            radial-gradient(0.3px 0.3px at 320px 200px, rgba(255,255,255,0.15), transparent),
            radial-gradient(0.1px 0.1px at 180px 300px, rgba(255,255,255,0.08), transparent),
            radial-gradient(0.25px 0.25px at 400px 350px, rgba(255,255,255,0.14), transparent),
            radial-gradient(0.2px 0.2px at 50px 450px, rgba(255,255,255,0.11), transparent),
            radial-gradient(0.4px 0.4px at 380px 500px, rgba(255,255,255,0.18), transparent),
            radial-gradient(0.15px 0.15px at 480px 250px, rgba(255,255,255,0.09), transparent),
            radial-gradient(0.5px 0.5px at 100px 600px, rgba(255,255,255,0.2), transparent)
          `,
          backgroundSize: '400px 400px, 500px 500px, 450px 450px, 550px 550px, 400px 400px, 600px 600px, 400px 400px, 580px 580px, 500px 500px, 600px 600px',
          filter: 'blur(0.1px)',
          animation: 'spaceDrift1 80s linear infinite',
          opacity: 0.4,
        }}
      />

      {/* Layer 2: Very distant twinkling stars */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(0.1px 0.1px at 80px 60px, rgba(255,255,255,0.15), transparent),
            radial-gradient(0.15px 0.15px at 240px 120px, rgba(255,255,255,0.18), transparent),
            radial-gradient(0.1px 0.1px at 400px 200px, rgba(255,255,255,0.12), transparent),
            radial-gradient(0.2px 0.2px at 160px 280px, rgba(255,255,255,0.2), transparent),
            radial-gradient(0.1px 0.1px at 320px 360px, rgba(255,255,255,0.14), transparent),
            radial-gradient(0.3px 0.3px at 480px 420px, rgba(255,255,255,0.22), transparent),
            radial-gradient(0.15px 0.15px at 120px 500px, rgba(255,255,255,0.16), transparent),
            radial-gradient(0.1px 0.1px at 360px 580px, rgba(255,255,255,0.13), transparent)
          `,
          backgroundSize: '800px 600px, 700px 600px, 750px 600px, 800px 600px, 700px 600px, 900px 600px, 750px 600px, 800px 600px',
          filter: 'blur(0.3px)',
          animation: 'spaceDrift2 100s linear infinite reverse',
          opacity: 0.3,
        }}
      />

      {/* Layer 3: Ultra distant star field */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(0.1px 0.1px at 60px 90px, rgba(255,255,255,0.08), transparent),
            radial-gradient(0.1px 0.1px at 180px 150px, rgba(255,255,255,0.1), transparent),
            radial-gradient(0.1px 0.1px at 300px 210px, rgba(255,255,255,0.07), transparent),
            radial-gradient(0.1px 0.1px at 420px 270px, rgba(255,255,255,0.09), transparent),
            radial-gradient(0.1px 0.1px at 540px 330px, rgba(255,255,255,0.06), transparent),
            radial-gradient(0.1px 0.1px at 660px 390px, rgba(255,255,255,0.08), transparent),
            radial-gradient(0.1px 0.1px at 140px 450px, rgba(255,255,255,0.07), transparent),
            radial-gradient(0.1px 0.1px at 260px 510px, rgba(255,255,255,0.09), transparent),
            radial-gradient(0.1px 0.1px at 380px 570px, rgba(255,255,255,0.06), transparent),
            radial-gradient(0.1px 0.1px at 500px 630px, rgba(255,255,255,0.08), transparent),
            radial-gradient(0.1px 0.1px at 620px 690px, rgba(255,255,255,0.05), transparent),
            radial-gradient(0.1px 0.1px at 740px 750px, rgba(255,255,255,0.07), transparent)
          `,
          backgroundSize: '1200px 900px, 1100px 900px, 1300px 900px, 1200px 900px, 1400px 900px, 1100px 900px, 1200px 900px, 1300px 900px, 1200px 900px, 1400px 900px, 1100px 900px, 1200px 900px',
          filter: 'blur(0.5px)',
          animation: 'spaceDrift3 120s linear infinite',
          opacity: 0.2,
        }}
      />

      {/* Content layer */}
      <Box
        sx={{
          position: 'relative',
          zIndex: 1,
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default SpaceBackground;