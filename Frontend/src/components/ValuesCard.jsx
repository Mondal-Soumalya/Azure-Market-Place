import React from 'react';
import { motion } from 'framer-motion';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box 
} from '@mui/material';

/**
 * Advanced Values Card Component
 * Features:
 * - Mathematical CSS calculations for responsive design
 * - Complex geometric animations
 * - Physics-based hover effects
 * - Dynamic gradient backgrounds
 * - Optimized typography scaling
 */
const ValuesCard = ({ 
  value, 
  index = 0,
  size = 'medium'
}) => {
  // Mathematical size calculations
  const sizeMap = {
    small: {
      card: { minHeight: 'clamp(160px, 20vh, 200px)', padding: 'clamp(12px, 2vw, 16px)' },
      icon: { size: 'clamp(24px, 4vw, 28px)', containerSize: 'clamp(40px, 6vw, 48px)' },
      typography: { 
        title: 'clamp(0.9rem, 2.5vw, 1.1rem)',
        description: 'clamp(0.7rem, 1.8vw, 0.8rem)'
      }
    },
    medium: {
      card: { minHeight: 'clamp(180px, 22vh, 220px)', padding: 'clamp(16px, 2.5vw, 20px)' },
      icon: { size: 'clamp(28px, 5vw, 32px)', containerSize: 'clamp(48px, 7vw, 56px)' },
      typography: { 
        title: 'clamp(1rem, 3vw, 1.2rem)',
        description: 'clamp(0.75rem, 2vw, 0.85rem)'
      }
    },
    large: {
      card: { minHeight: 'clamp(200px, 25vh, 240px)', padding: 'clamp(20px, 3vw, 24px)' },
      icon: { size: 'clamp(32px, 6vw, 36px)', containerSize: 'clamp(56px, 8vw, 64px)' },
      typography: { 
        title: 'clamp(1.1rem, 3.5vw, 1.3rem)',
        description: 'clamp(0.8rem, 2.2vw, 0.9rem)'
      }
    }
  };

  const currentSize = sizeMap[size];

  // Simplified animation variants to fix flash issues
  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 20
    },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: "easeOut"
      }
    }
  };

  const iconContainerVariants = {
    hover: {
      scale: 1.05,
      transition: {
        duration: 0.2,
        ease: "easeOut"
      }
    }
  };

  const iconVariants = {
    hover: {
      scale: 1.02,
      transition: {
        duration: 0.2,
        ease: "easeOut"
      }
    }
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      style={{
        perspective: '1000px'
      }}
    >
      <Card
        sx={{
          minHeight: currentSize.card.minHeight,
          background: `
            radial-gradient(circle at 20% 80%, rgba(95, 255, 224, 0.06) 0%, transparent 40%),
            rgba(255, 255, 255, 0.02)
          `,
          backdropFilter: 'blur(10px) saturate(150%)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 'clamp(10px, 1.8vw, 14px)',
          transition: 'all 0.3s ease-out',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: `
            0 2px 8px rgba(0, 0, 0, 0.06),
            0 1px 3px rgba(0, 0, 0, 0.04),
            inset 0 1px 0 rgba(255, 255, 255, 0.08)
          `,
          '&:hover': {
            transform: 'translateY(-3px)',
            boxShadow: `
              0 6px 20px rgba(95, 255, 224, 0.08),
              0 4px 12px rgba(0, 0, 0, 0.06),
              inset 0 1px 0 rgba(255, 255, 255, 0.12)
            `,
            borderColor: 'rgba(95, 255, 224, 0.15)'
          }
        }}
      >
        <CardContent 
          sx={{ 
            p: currentSize.card.padding,
            textAlign: 'center',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 'clamp(8px, 1.5vw, 12px)',
            position: 'relative',
            zIndex: 1
          }}
        >
          {/* Icon with complex nested animations */}
          <motion.div 
            variants={iconContainerVariants}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: currentSize.icon.containerSize,
              height: currentSize.icon.containerSize,
              borderRadius: '50%',
              background: `
                linear-gradient(135deg, 
                  rgba(95, 255, 224, 0.15) 0%, 
                  rgba(95, 255, 224, 0.08) 100%
                ),
                radial-gradient(circle at 30% 30%, 
                  rgba(255, 255, 255, 0.2) 0%, 
                  transparent 70%
                )
              `,
              boxShadow: `
                0 4px 12px rgba(95, 255, 224, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3)
              `,
              position: 'relative'
            }}
          >
            <motion.div variants={iconVariants}>
              {React.cloneElement(value.icon, {
                sx: { 
                  fontSize: currentSize.icon.size, 
                  color: '#66FFE0',
                  filter: 'drop-shadow(0 1px 3px rgba(0, 0, 0, 0.2))'
                }
              })}
            </motion.div>
          </motion.div>

          {/* Title with gradient text and optimized typography */}
          <Typography 
            variant="h6" 
            sx={{ 
              fontWeight: 600,
              fontSize: currentSize.typography.title,
              lineHeight: 1.3,
              background: 'linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
              letterSpacing: '-0.005em'
            }}
          >
            {value.title}
          </Typography>

          {/* Description with mathematical line spacing */}
          <Typography 
            variant="body2" 
            color="text.secondary" 
            sx={{ 
              fontSize: currentSize.typography.description,
              lineHeight: 1.6,
              opacity: 0.85,
              textAlign: 'center',
              display: '-webkit-box',
              WebkitLineClamp: 4,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
              letterSpacing: '0.01em'
            }}
          >
            {value.description}
          </Typography>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ValuesCard;
