import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { Box } from '@mui/material';

const ParticlesBackground = ({ 
  particleCount = 80,
  enableInteraction = true,
  enableAnimation = true,
  style = {}
}) => {
  const [particles, setParticles] = useState([]);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [windowSize, setWindowSize] = useState({ width: 0, height: 0 });

  // Single color scheme (AI Blue) -> updated to semantic-inspired accent set
  // Space-like color scheme with more visible particles
  const colors = useMemo(() => ({
    particles: '#66FFE0', // bright cyan-green primary
    lines: 'rgba(102,255,224,0.3)',
    background: 'transparent',
    accent: '#6366f1', // purple accent
    accentLines: 'rgba(99,102,241,0.2)'
  }), []);

  // Initialize particles
  const initParticles = useCallback(() => {
    const newParticles = [];
    for (let i = 0; i < particleCount; i++) {
      newParticles.push({
        id: i,
        x: Math.random() * windowSize.width,
        y: Math.random() * windowSize.height,
        vx: (Math.random() - 0.5) * 2, // More noticeable horizontal velocity
        vy: (Math.random() - 0.5) * 2, // More noticeable vertical velocity
        size: Math.random() * 2.5 + 0.5, // Smaller, more subtle particles
        opacity: Math.random() * 0.8 + 0.2, // Higher opacity for visibility
        colorType: Math.random() > 0.03 ? 'primary' : 'accent', // 97% cyan-green, 3% purple
        drift: (Math.random() - 0.5) * 0.5, // More noticeable drift for space feel
        wobble: Math.random() * Math.PI * 2, // Random wobble phase
        wobbleSpeed: (Math.random() + 0.5) * 0.05 // Faster wobble for visibility
      });
    }
    setParticles(newParticles);
  }, [particleCount, windowSize]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Initialize particles when window size changes
  useEffect(() => {
    if (windowSize.width > 0 && windowSize.height > 0) {
      initParticles();
    }
  }, [windowSize, initParticles]);

  // Handle mouse movement
  useEffect(() => {
    if (!enableInteraction) return;

    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [enableInteraction]);

  // Animation loop with more visible slow motion space feel
  useEffect(() => {
    if (!enableAnimation) return;

    const animationFrame = () => {
      setParticles(prevParticles => 
        prevParticles.map(particle => {
          let { x, y, vx, vy, drift, wobble, wobbleSpeed } = particle;

          // Update wobble for space-like floating effect
          wobble += wobbleSpeed;
          
          // Apply movement with more noticeable drift and wobble
          x += vx * 0.6 + drift + Math.sin(wobble) * 0.3; // More visible movement
          y += vy * 0.6 + Math.cos(wobble * 0.7) * 0.2; // More noticeable vertical wobble

          // Smooth boundary wrapping instead of bouncing for space feel
          if (x < -10) x = windowSize.width + 10;
          if (x > windowSize.width + 10) x = -10;
          if (y < -10) y = windowSize.height + 10;
          if (y > windowSize.height + 10) y = -10;

          // Gentle mouse interaction for space-like behavior
          if (enableInteraction) {
            const dx = mousePosition.x - x;
            const dy = mousePosition.y - y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 120) {
              const force = (120 - distance) / 120;
              vx += (dx / distance) * force * 0.05; // Slightly stronger force
              vy += (dy / distance) * force * 0.05;
            }
          }

          // Limit velocity to maintain controlled movement
          const maxVelocity = 2;
          if (Math.abs(vx) > maxVelocity) vx = vx > 0 ? maxVelocity : -maxVelocity;
          if (Math.abs(vy) > maxVelocity) vy = vy > 0 ? maxVelocity : -maxVelocity;

          // Add slight velocity decay for more natural movement
          vx *= 0.998;
          vy *= 0.998;

          return {
            ...particle,
            x,
            y,
            vx,
            vy,
            wobble
          };
        })
      );
    };

    const intervalId = setInterval(animationFrame, 40); // Faster frame rate for smoother movement
    return () => clearInterval(intervalId);
  }, [enableAnimation, mousePosition, windowSize, enableInteraction]);

  // Calculate connections between particles with more visible lines
  const connections = useMemo(() => {
    const lines = [];
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 160) { // Good connection distance
          lines.push({
            x1: particles[i].x,
            y1: particles[i].y,
            x2: particles[j].x,
            y2: particles[j].y,
            opacity: (160 - distance) / 160 * 0.4 // More visible connections
          });
        }
      }
    }
    return lines;
  }, [particles]);

  if (!windowSize.width || !windowSize.height) {
    return null;
  }

  const handleError = (error) => {
    console.error('ParticlesBackground error:', error);
    return null;
  };

  try {
    return (
      <Box
        sx={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          zIndex: -1,
          pointerEvents: 'none',
          background: colors.background,
          ...style
        }}
      >
        <svg
          width={windowSize.width}
          height={windowSize.height}
          style={{ display: 'block' }}
        >
          {/* Reduced motion: if user prefers reduced motion, render static minimal set */}
          {window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches && particles.slice(0,20)}
          {/* Render connections with dynamic colors */}
          {connections.map((line, index) => {
            const lineColor = Math.random() > 0.3 ? colors.lines : colors.accentLines;
            return (
              <line
                key={`line-${index}`}
                x1={line.x1}
                y1={line.y1}
                x2={line.x2}
                y2={line.y2}
                stroke={lineColor}
                strokeWidth="1"
                opacity={line.opacity}
              />
            );
          })}
          
          {/* Render particles with color variety */}
          {particles.map(particle => (
            <circle
              key={particle.id}
              cx={particle.x}
              cy={particle.y}
              r={particle.size}
              fill={particle.colorType === 'primary' ? colors.particles : colors.accent}
              opacity={particle.opacity}
            />
          ))}
        </svg>
      </Box>
    );
  } catch (error) {
    return handleError(error);
  }
};

export default ParticlesBackground;