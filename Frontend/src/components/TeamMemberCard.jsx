import React from 'react';
import { motion } from 'framer-motion';
import { 
  Card, 
  CardContent, 
  Avatar, 
  Typography, 
  Chip, 
  Box 
} from '@mui/material';

/**
 * Advanced Team Member Card Component
 * Features:
 * - Mathematical CSS calculations for responsive sizing
 * - Complex animations and transforms
 * - Dynamic hover effects with physics-based movements
 * - Optimized typography scaling
 * - Geometric shadow patterns
 */
const TeamMemberCard = ({ 
  member, 
  index = 0,
  variant = 'default',
  size = 'medium' 
}) => {
  // Mathematical size calculations
  const sizeMap = {
    small: {
      card: { minHeight: 'clamp(200px, 25vh, 280px)', padding: 'clamp(12px, 2vw, 16px)' },
      avatar: { size: 'clamp(48px, 8vw, 56px)', iconSize: 'clamp(24px, 4vw, 28px)' },
      typography: { 
        name: 'clamp(0.9rem, 2.5vw, 1.1rem)',
        role: 'clamp(0.75rem, 2vw, 0.85rem)',
        description: 'clamp(0.7rem, 1.8vw, 0.8rem)'
      }
    },
    medium: {
      card: { minHeight: 'clamp(240px, 30vh, 320px)', padding: 'clamp(16px, 2.5vw, 20px)' },
      avatar: { size: 'clamp(56px, 10vw, 64px)', iconSize: 'clamp(28px, 5vw, 32px)' },
      typography: { 
        name: 'clamp(1rem, 3vw, 1.25rem)',
        role: 'clamp(0.8rem, 2.2vw, 0.9rem)',
        description: 'clamp(0.75rem, 2vw, 0.85rem)'
      }
    },
    large: {
      card: { minHeight: 'clamp(280px, 35vh, 360px)', padding: 'clamp(20px, 3vw, 24px)' },
      avatar: { size: 'clamp(64px, 12vw, 72px)', iconSize: 'clamp(32px, 6vw, 36px)' },
      typography: { 
        name: 'clamp(1.1rem, 3.5vw, 1.4rem)',
        role: 'clamp(0.85rem, 2.5vw, 1rem)',
        description: 'clamp(0.8rem, 2.2vw, 0.9rem)'
      }
    }
  };

  const currentSize = sizeMap[size];

  // Simplified animation variants
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

  const avatarVariants = {
    hover: {
      scale: 1.05,
      transition: {
        duration: 0.2,
        ease: "easeOut"
      }
    }
  };

  const chipVariants = {
    hover: {
      scale: 1.05,
      transition: {
        duration: 0.2
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
            radial-gradient(circle at 15% 85%, rgba(95, 255, 224, 0.08) 0%, transparent 40%),
            rgba(255, 255, 255, 0.03)
          `,
          backdropFilter: 'blur(12px) saturate(180%)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: 'clamp(12px, 2vw, 16px)',
          transition: 'all 0.3s ease-out',
          position: 'relative',
          overflow: 'hidden',
          boxShadow: `
            0 2px 12px rgba(0, 0, 0, 0.08),
            0 1px 3px rgba(0, 0, 0, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.1)
          `,
          '&:hover': {
            transform: 'translateY(-3px)',
            boxShadow: `
              0 6px 24px rgba(95, 255, 224, 0.1),
              0 4px 12px rgba(0, 0, 0, 0.08),
              inset 0 1px 0 rgba(255, 255, 255, 0.15)
            `,
            borderColor: 'rgba(95, 255, 224, 0.2)'
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
            gap: 'clamp(8px, 1.5vw, 12px)'
          }}
        >
          {/* Avatar with complex animations */}
          <motion.div variants={avatarVariants}>
            <Avatar
              sx={{
                width: currentSize.avatar.size,
                height: currentSize.avatar.size,
                mx: 'auto',
                background: `
                  linear-gradient(135deg, #66FFE0 0%, #4ce8c9 100%),
                  radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.3) 0%, transparent 70%)
                `,
                boxShadow: `
                  0 4px 12px rgba(95, 255, 224, 0.3),
                  inset 0 1px 0 rgba(255, 255, 255, 0.5),
                  inset 0 -1px 0 rgba(0, 0, 0, 0.1)
                `,
                position: 'relative',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: '10%',
                  left: '20%',
                  width: '30%',
                  height: '30%',
                  background: 'rgba(255, 255, 255, 0.4)',
                  borderRadius: '50%',
                  filter: 'blur(2px)'
                }
              }}
            >
              {React.cloneElement(member.avatar, {
                sx: { 
                  fontSize: currentSize.avatar.iconSize, 
                  color: '#1a1a1a',
                  filter: 'drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2))'
                }
              })}
            </Avatar>
          </motion.div>

          {/* Name with mathematical font scaling */}
          <Typography 
            variant="h6" 
            sx={{ 
              fontWeight: 600,
              fontSize: currentSize.typography.name,
              lineHeight: 1.2,
              color: 'text.primary',
              textShadow: '0 1px 2px rgba(0, 0, 0, 0.1)',
              letterSpacing: '-0.01em'
            }}
          >
            {member.name}
          </Typography>

          {/* Role with gradient text */}
          <Typography 
            variant="body2" 
            sx={{ 
              fontSize: currentSize.typography.role,
              fontWeight: 500,
              background: 'linear-gradient(135deg, #66FFE0 0%, #4ce8c9 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              lineHeight: 1.3
            }}
          >
            {member.role}
          </Typography>

          {/* Description with optimized line height */}
          <Typography 
            variant="body2" 
            color="text.secondary" 
            sx={{ 
              fontSize: currentSize.typography.description,
              lineHeight: 1.5,
              opacity: 0.9,
              flexGrow: 1,
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden'
            }}
          >
            {member.description}
          </Typography>

          {/* Expertise chips with staggered animations */}
          <Box 
            sx={{ 
              display: 'flex', 
              flexWrap: 'wrap', 
              gap: 'clamp(4px, 1vw, 6px)', 
              justifyContent: 'center',
              mt: 'auto'
            }}
          >
            {member.expertise.map((skill, idx) => (
              <motion.div
                key={idx}
                variants={chipVariants}
                whileHover="hover"
                custom={idx}
              >
                <Chip
                  label={skill}
                  size="small"
                  sx={{
                    fontSize: 'clamp(0.65rem, 1.5vw, 0.7rem)',
                    height: 'clamp(20px, 4vw, 24px)',
                    background: `
                      linear-gradient(135deg, 
                        rgba(95, 255, 224, 0.12) 0%, 
                        rgba(95, 255, 224, 0.08) 100%
                      )
                    `,
                    color: '#66FFE0',
                    fontWeight: 500,
                    border: '1px solid rgba(95, 255, 224, 0.2)',
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      background: `
                        linear-gradient(135deg, 
                          rgba(95, 255, 224, 0.2) 0%, 
                          rgba(95, 255, 224, 0.15) 100%
                        )
                      `,
                      borderColor: 'rgba(95, 255, 224, 0.4)',
                      transform: 'translateY(-1px)'
                    }
                  }}
                />
              </motion.div>
            ))}
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default TeamMemberCard;
