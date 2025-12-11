import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Stack } from '@mui/material';
import { motion } from 'framer-motion';
import { ArrowForward as ArrowForwardIcon } from '@mui/icons-material';

/**
 * Modern 3D Capability Card Component
 * Creates beautiful, eye-catching cards with:
 * - Subtle 3D depth effects
 * - Smooth hover animations
 * - Glass morphism design
 * - Professional gradients
 * - Interactive states
 */
const CapabilityCard3D = ({ 
  icon,
  title, 
  description,
  status,
  features = [],
  gradient,
  onClick,
  delay = 0,
  ...props 
}) => {

  return (
    <motion.div
      initial={{ 
        opacity: 0, 
        y: 60,
        scale: 0.95,
        rotateX: 10
      }}
      animate={{ 
        opacity: 1, 
        y: 0,
        scale: 1,
        rotateX: 0
      }}
      transition={{ 
        duration: 0.8, 
        delay: delay,
        ease: [0.23, 1, 0.32, 1]
      }}
      whileHover={{ 
        y: -12,
        scale: 1.02,
        rotateX: 5,
        rotateY: 2,
        transition: { 
          duration: 0.3,
          ease: [0.23, 1, 0.32, 1]
        }
      }}
      style={{
        perspective: '1000px',
        transformStyle: 'preserve-3d',
      }}
      {...props}
    >
      <Card
        onClick={onClick}
        sx={{
          height: 280, // Fixed height for uniform cards
          width: '100%', // Full width of grid item
          position: 'relative',
          overflow: 'hidden',
          cursor: 'pointer',
          borderRadius: 3,
          border: '1px solid rgba(255, 255, 255, 0.08)',
          transformStyle: 'preserve-3d',
          
          // Transparent background with subtle gradient overlay
          background: `
            linear-gradient(145deg, 
              rgba(255, 255, 255, 0.03) 0%, 
              rgba(255, 255, 255, 0.01) 50%, 
              rgba(0, 0, 0, 0.02) 100%
            )
          `,
          
          // More subtle backdrop filter for transparency
          backdropFilter: 'blur(15px)',
          
          // Enhanced 3D shadow system with PRISM ANALYTICS colors
          boxShadow: `
            0 4px 8px rgba(79, 195, 247, 0.05),
            0 8px 16px rgba(41, 182, 246, 0.04),
            0 16px 32px rgba(0, 0, 0, 0.03),
            0 32px 64px rgba(0, 0, 0, 0.02),
            inset 0 1px 0 rgba(255, 255, 255, 0.05),
            inset 0 -1px 0 rgba(0, 0, 0, 0.05)
          `,
          
          transition: 'all 0.4s cubic-bezier(0.23, 1, 0.32, 1)',
          
          // Hover effects with PRISM ANALYTICS colors
          '&:hover': {
            boxShadow: `
              0 8px 16px rgba(79, 195, 247, 0.1),
              0 16px 32px rgba(41, 182, 246, 0.08),
              0 32px 64px rgba(2, 119, 189, 0.06),
              0 64px 128px rgba(0, 0, 0, 0.04),
              inset 0 1px 0 rgba(255, 255, 255, 0.1),
              inset 0 -1px 0 rgba(0, 0, 0, 0.05)
            `,
            transform: 'translateZ(20px)',
            borderColor: 'rgba(79, 195, 247, 0.2)',
            
            '& .capability-icon': {
              transform: 'scale(1.1) rotateY(10deg)',
            },
            
            '& .capability-arrow': {
              transform: 'translateX(8px)',
              opacity: 1,
            },
            
            '& .capability-features': {
              '& > *': {
                transform: 'translateY(-2px)',
              }
            }
          },
          
          // Animated border effect with PRISM ANALYTICS colors
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            borderRadius: 'inherit',
            padding: '1px',
            background: `
              linear-gradient(135deg, 
                rgba(79, 195, 247, 0.1) 0%, 
                rgba(41, 182, 246, 0.05) 50%, 
                rgba(2, 119, 189, 0.1) 100%
              )
            `,
            mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
            maskComposite: 'xor',
            WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
            WebkitMaskComposite: 'xor',
            zIndex: 1,
            pointerEvents: 'none',
          }
        }}
      >
        {/* Subtle ambient light overlay */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            height: '50%',
            background: `
              radial-gradient(ellipse at top center, 
                rgba(79, 195, 247, 0.08) 0%, 
                rgba(41, 182, 246, 0.03) 40%, 
                transparent 70%
              )
            `,
            zIndex: 2,
            pointerEvents: 'none',
          }}
        />
        
        <CardContent 
          sx={{ 
            p: 2.5, // Consistent padding
            height: '100%',
            position: 'relative',
            zIndex: 3,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between', // Distribute space evenly
          }}
        >
          {/* Icon Section */}
          <Box
            className="capability-icon"
            sx={{
              display: 'flex',
              justifyContent: 'center',
              mb: 1.5,
              transform: 'translateZ(10px)',
              transition: 'transform 0.4s cubic-bezier(0.23, 1, 0.32, 1)',
            }}
          >
            <Box
              sx={{
                width: 50, // Smaller consistent icon size
                height: 50,
                borderRadius: 2,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: `
                  radial-gradient(ellipse at 30% 30%, 
                    rgba(79, 195, 247, 0.2) 0%, 
                    rgba(41, 182, 246, 0.1) 50%, 
                    transparent 70%
                  ),
                  rgba(255, 255, 255, 0.05)
                `,
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(79, 195, 247, 0.15)',
                boxShadow: `
                  0 4px 8px rgba(41, 182, 246, 0.1),
                  0 8px 16px rgba(0, 0, 0, 0.05),
                  inset 0 1px 0 rgba(255, 255, 255, 0.1)
                `,
              }}
            >
              {React.cloneElement(icon, { 
                sx: { 
                  fontSize: 28, // Consistent icon size
                  color: '#5fffe0'
                } 
              })}
            </Box>
          </Box>
          
          {/* Status Chip */}
          <Box sx={{ display: 'flex', justifyContent: 'center', mb: 1 }}>
            <Chip
              label={status}
              size="small"
              sx={{
                backgroundColor: 'rgba(95, 255, 224, 0.1)',
                color: '#5fffe0',
                fontWeight: 600,
                fontSize: '0.65rem',
                height: '20px', // Fixed height
                border: '1px solid rgba(95, 255, 224, 0.2)',
                backdropFilter: 'blur(10px)',
                '&:hover': {
                  backgroundColor: 'rgba(95, 255, 224, 0.15)',
                }
              }}
            />
          </Box>
          
          {/* Title */}
          <Typography 
            variant="h6"
            sx={{ 
              mb: 1,
              fontWeight: 700,
              color: 'rgba(255, 255, 255, 0.95)',
              textAlign: 'center',
              textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
              letterSpacing: '0.3px',
              fontSize: '1rem', // Consistent font size
              lineHeight: 1.2,
              display: '-webkit-box',
              WebkitLineClamp: 2, // Limit to 2 lines
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {title}
          </Typography>
          
          {/* Description */}
          <Typography 
            variant="body2" 
            sx={{ 
              mb: 1.5,
              color: 'rgba(255, 255, 255, 0.8)',
              lineHeight: 1.4,
              textAlign: 'center',
              flex: 1,
              textShadow: '0 1px 2px rgba(0, 0, 0, 0.2)',
              fontSize: '0.8rem',
              display: '-webkit-box',
              WebkitLineClamp: 3, // Limit to 3 lines
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden',
            }}
          >
            {description}
          </Typography>
          
          {/* Features */}
          <Box 
            className="capability-features"
            sx={{ mb: 1.5 }}
          >
            <Stack spacing={0.3} direction="row" sx={{ flexWrap: 'wrap', justifyContent: 'center', gap: 0.5 }}>
              {features.slice(0, 3).map((feature, index) => (
                <Chip
                  key={index}
                  label={feature}
                  size="small"
                  sx={{
                    backgroundColor: 'rgba(79, 195, 247, 0.08)',
                    color: 'rgba(255, 255, 255, 0.8)',
                    fontSize: '0.6rem',
                    height: '18px',
                    fontWeight: 500,
                    border: '1px solid rgba(41, 182, 246, 0.1)',
                    transition: 'transform 0.3s ease',
                    transitionDelay: `${index * 0.05}s`,
                    '&:hover': {
                      transform: 'translateY(-1px)',
                      backgroundColor: 'rgba(2, 119, 189, 0.12)',
                    }
                  }}
                />
              ))}
            </Stack>
          </Box>
          
          {/* Action Arrow - More compact */}
          <Box 
            sx={{ 
              display: 'flex', 
              justifyContent: 'center',
              mt: 'auto'
            }}
          >
            <ArrowForwardIcon 
              className="capability-arrow"
              sx={{ 
                color: '#5fffe0',
                fontSize: 20, // Smaller arrow
                transition: 'all 0.3s ease',
                opacity: 0.7,
                filter: 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3))',
              }} 
            />
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default CapabilityCard3D;
