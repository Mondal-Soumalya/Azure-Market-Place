import React, { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { 
  Container, 
  Typography, 
  Button, 
  Card, 
  CardContent, 
  Box,
  Grid,
  Chip,
  useTheme,
  useMediaQuery,
  Stack,
  Divider
} from '@mui/material';
import { 
  Analytics as AnalyticsIcon,
  SupportAgent as SupportAgentIcon,
   FlashOn as FlashOnIcon,  
  Psychology as PsychologyIcon,
  AutoAwesome as AutoAwesomeIcon,
  ArrowForward as ArrowForwardIcon,
  KeyboardArrowDown as KeyboardArrowDownIcon,
  Bolt as BoltIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  Settings as SettingsIcon,
  Build as BuildIcon,
  Timeline as TimelineIcon,
  SmartToy as SmartToyIcon
} from '@mui/icons-material';
import ParticlesBackground from '../components/ParticlesBackground';
import CapabilityCard3D from '../components/CapabilityCard3D';
import useScrollToTop from '../hooks/useScrollToTop';

const ProfessionalHomePage = () => {
  useScrollToTop();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // State to track when capabilities are floating
  const [isCapabilitiesFloating, setIsCapabilitiesFloating] = React.useState(false);
  
  React.useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      const shouldFloat = scrollPosition > 120;
      setIsCapabilitiesFloating(shouldFloat);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Professional fade-in cycling animation
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(0);
  const [fadeClass, setFadeClass] = useState('fade-in');

  const phrases = [
    'Intelligent Workflows', 
    'Smart Analytics',
    'Process Optimization',
    'Digital Innovation'
  ];

  useEffect(() => {
    const cycleInterval = setInterval(() => {
      setFadeClass('fade-out');
      
      setTimeout(() => {
        setCurrentPhraseIndex((prevIndex) => 
          (prevIndex + 1) % phrases.length
        );
        setFadeClass('fade-in');
      }, 500); // Half second fade-out duration
      
    }, 2000); // Change phrase every 2 seconds for a calmer pace

    return () => clearInterval(cycleInterval);
  }, []);

  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('sm'));

  // Professional feature set matching the uploaded images
  const features = [
    {
      icon: <PsychologyIcon sx={{ fontSize: 48, color: 'white' }} />,
      title: 'INCIDENT TICKET ANALYSIS',
      description: 'Comprehensive analysis of incident tickets to identify patterns, reduce noise, and uncover root causes, enabling faster resolution and improved service quality.',
      status: 'Active',
      path: '/analysisenginepage',
      gradient: 'linear-gradient(135deg, #00ffdc 0%, #5f7fff 2%, #00ffdc 100%)',
      features: [
    'Noise Reduction',
    'Root Cause Identification',
    'Ticket Categorization',
    'Resolution Insights',
  ],
      iconVariant: 'incident'
    },
  //   {
  //     icon: <SupportAgentIcon sx={{ fontSize: 48, color: 'white' }} />,
  //     title: 'SERVICE DESK TICKET ANALYSIS',
  //     description: 'Insightful analysis of service desk tickets to track resolution trends, improve response times, and enhance user experience through actionable insights.',
  //     status: 'Active',
  //     path: '/servicedeskanalysis',
  //     gradient: 'linear-gradient(135deg, #00ffdc 0%, #5f7fff 2%, #00ffdc 100%)',
  //     features: [
  //   'Resolution Time Tracking',
  //   'Trend Analysis',
  //   'User Experience Insights',
  //   'Team Performance Metrics',
  // ],
  //     iconVariant: 'servicedesk'
  //   },
    // {
    //   icon: <FlashOnIcon sx={{ fontSize: 48, color: 'white' }} />,
    //   title: 'REAL-TIME GENERATIVE AI',
    //   description: 'Cutting-edge generative AI that creates content, solutions, and responses in real-time with human-like intelligence and creativity.',
    //   status: 'AI-Powered',
    //   path: '/analysisenginepage',
    //   gradient: 'linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)',
    //   features: ['Content Generation', 'Real-time Processing', 'Creative AI', 'Intelligent Responses'],
    //   iconVariant: 'intelligence'
    // },
    // {
    //   icon: <SmartToyIcon sx={{ fontSize: 48, color: 'white' }} />,
    //   title: 'INTELLIGENT AGENTS',
    //   description: 'Autonomous AI agents that work 24/7 to monitor, manage, and optimize your systems with advanced machine learning capabilities.',
    //   status: 'Autonomous',
    //   path: '/analysisenginepage',
    //   gradient: 'linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)',
    //   features: ['24/7 Monitoring', 'Autonomous Actions', 'Smart Decisions', 'Continuous Learning'],
    //   iconVariant: 'intelligence'
    // }
  ];

  // Professional stats for credibility
  const stats = [
    { icon: <TrendingUpIcon />, value: '99.9%', label: 'Uptime' },
    { icon: <SpeedIcon />, value: '<100ms', label: 'Response Time' },
    { icon: <SecurityIcon />, value: 'SOC2', label: 'Compliant' },
    { icon: <AnalyticsIcon />, value: '24/7', label: 'Support' }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.22, 1, 0.36, 1]
      }
    }
  };

  const floatAnimation = {
    y: [0, -10, 0],
    transition: {
      duration: 6,
      repeat: Infinity,
      ease: "easeInOut"
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', position: 'relative', overflow: 'hidden' }}>
      <ParticlesBackground />
      
      {/* Hero Section - Professional and Impactful */}
      <Box
        component={motion.section}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          position: 'relative',
          px: { xs: 2, sm: 3, md: 4 },
          py: { xs: 8, sm: 10, md: 12 }
        }}
      >
        {/* Far Away Deep Space Background Pattern */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.15, // Increased from 0.08
            backgroundImage: `
              radial-gradient(circle at 20% 20%, #00ffdc 0.5px, rgba(0, 255, 220, 0.2) 1px, transparent 2px),
              radial-gradient(circle at 80% 80%, #5f7fff 0.5px, rgba(95, 127, 255, 0.15) 1px, transparent 1.5px),
              radial-gradient(circle at 40% 40%, #00bfff 0.3px, rgba(0, 191, 255, 0.1) 0.8px, transparent 1.2px),
              radial-gradient(circle at 60% 15%, rgba(100, 200, 255, 0.6) 0.2px, transparent 0.8px),
              radial-gradient(circle at 15% 70%, rgba(0, 255, 200, 0.5) 0.2px, transparent 0.6px),
              radial-gradient(circle at 90% 30%, rgba(0, 255, 220, 0.4) 0.2px, transparent 0.7px),
              radial-gradient(circle at 25% 50%, rgba(95, 127, 255, 0.3) 0.1px, transparent 0.5px),
              radial-gradient(circle at 75% 25%, rgba(0, 255, 200, 0.4) 0.1px, transparent 0.4px)
            `,
            backgroundSize: '400px 400px, 600px 600px, 300px 300px, 200px 200px, 250px 250px, 180px 180px, 150px 150px, 120px 120px',
            animation: 'distantStarFloat 80s ease-in-out infinite',
            '@keyframes distantStarFloat': {
              '0%, 100%': { 
                transform: 'translate(0, 0) rotate(0deg) scale(1)',
                filter: 'brightness(0.8) blur(0px)'
              },
              '25%': { 
                transform: 'translate(4px, -6px) rotate(0.2deg) scale(1.005)',
                filter: 'brightness(0.9) blur(0.2px)'
              },
              '50%': { 
                transform: 'translate(-3px, -4px) rotate(-0.1deg) scale(0.995)',
                filter: 'brightness(0.85) blur(0.1px)'
              },
              '75%': { 
                transform: 'translate(5px, 3px) rotate(0.1deg) scale(1.002)',
                filter: 'brightness(0.88) blur(0.15px)'
              }
            }
          }}
        />

        {/* Very Distant Twinkling Stars */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.6, // Increased from 0.4
            background: `
              radial-gradient(0.2px 0.2px at 25% 35%, rgba(0, 255, 220, 0.9), transparent),
              radial-gradient(0.3px 0.3px at 75% 65%, rgba(0, 255, 220, 0.7), transparent),
              radial-gradient(0.1px 0.1px at 45% 85%, rgba(95, 127, 255, 0.8), transparent),
              radial-gradient(0.2px 0.2px at 85% 25%, rgba(0, 255, 200, 0.7), transparent),
              radial-gradient(0.3px 0.3px at 15% 55%, rgba(0, 191, 255, 0.7), transparent),
              radial-gradient(0.1px 0.1px at 65% 10%, rgba(100, 200, 255, 0.8), transparent),
              radial-gradient(0.2px 0.2px at 35% 75%, rgba(0, 255, 220, 0.6), transparent),
              radial-gradient(0.1px 0.1px at 95% 50%, rgba(0, 255, 220, 0.7), transparent),
              radial-gradient(0.2px 0.2px at 10% 90%, rgba(95, 127, 255, 0.75), transparent),
              radial-gradient(0.1px 0.1px at 55% 20%, rgba(0, 255, 200, 0.8), transparent)
            `,
            backgroundSize: '800px 600px',
            animation: 'farTwinkle 15s ease-in-out infinite',
            '@keyframes farTwinkle': {
              '0%, 100%': { opacity: 0.4, transform: 'scale(1)' },
              '33%': { opacity: 0.2, transform: 'scale(0.98)' },
              '66%': { opacity: 0.6, transform: 'scale(1.01)' }
            }
          }}
        />

        {/* Ultra Distant Star Field */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            opacity: 0.5, // Increased from 0.3
            background: `
              radial-gradient(0.1px 0.1px at 12% 18%, rgba(0, 255, 220, 1), transparent),
              radial-gradient(0.1px 0.1px at 88% 82%, rgba(0, 255, 220, 0.9), transparent),
              radial-gradient(0.1px 0.1px at 32% 68%, rgba(95, 127, 255, 0.95), transparent),
              radial-gradient(0.1px 0.1px at 72% 28%, rgba(0, 191, 255, 0.8), transparent),
              radial-gradient(0.1px 0.1px at 18% 45%, rgba(0, 255, 200, 0.75), transparent),
              radial-gradient(0.1px 0.1px at 82% 55%, rgba(100, 200, 255, 0.85), transparent),
              radial-gradient(0.1px 0.1px at 48% 8%, rgba(0, 255, 220, 0.9), transparent),
              radial-gradient(0.1px 0.1px at 68% 92%, rgba(0, 255, 200, 0.8), transparent)
            `,
            backgroundSize: '1200px 900px',
            animation: 'ultraDistantDrift 120s linear infinite',
            '@keyframes ultraDistantDrift': {
              '0%': { 
                transform: 'translateX(0px) translateY(0px) scale(1)',
                filter: 'blur(0.3px) brightness(0.7)'
              },
              '100%': { 
                transform: 'translateX(-20px) translateY(-10px) scale(0.99)',
                filter: 'blur(0.5px) brightness(0.6)'
              }
            }
          }}
        />

        <Container maxWidth="lg" sx={{ pointerEvents: 'auto' }}>
          {/* Company Logo/Icon */}
          <div>
            <div style={{ 
              animation: 'gravitylessFloat 5s ease-in-out infinite',
              pointerEvents: 'none'
            }}>
              <Box
                sx={{
                  width: { xs: 100, sm: 120, md: 140 },
                  height: { xs: 100, sm: 120, md: 140 },
                  borderRadius: '32px',
                  background: 'linear-gradient(135deg, #00ffdc 0%, #5f7fff 2%, #00ffdc 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 40px',
                  boxShadow: '0 25px 60px rgba(0, 255, 220, 0.6)',
                  position: 'relative',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    inset: '-3px',
                    background: 'linear-gradient(135deg, #00ffdc, #5f7fff, #00ffdc, #00ff88)',
                    borderRadius: '35px',
                    zIndex: -1,
                    opacity: 0.9,
                    animation: 'rotate 12s linear infinite',
                  },
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    inset: '10px',
                    background: 'rgba(15, 15, 35, 0.9)',
                    borderRadius: '24px',
                    zIndex: -1,
                  },
                  '@keyframes rotate': {
                    '0%': { transform: 'rotate(0deg)' },
                    '100%': { transform: 'rotate(360deg)' }
                  }
                }}
              >
                <BoltIcon sx={{ fontSize: { xs: 40, sm: 48, md: 56 }, color: 'white', filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.3))' }} />
              </Box>
            </div>
          </div>

          {/* Main Headline with Typing Animation */}
          <div style={{ 
            pointerEvents: 'none', 
            marginBottom: '2rem',
            // Responsive margins
            marginTop: isMobile ? '1rem' : '1.5rem'
          }}>
            <Typography 
              variant="h1"
              sx={{ 
                fontWeight: 700, 
                mb: { xs: 2, sm: 3, md: 4 }, // Responsive bottom margin
                background: 'linear-gradient(135deg, #e0f7ff 0%, #b3e5fc 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                lineHeight: { xs: 1.3, sm: 1.2, md: 1.1 }, // Slightly increased for two lines
                letterSpacing: { xs: '-0.015em', sm: '-0.02em', md: '-0.025em' }, // Responsive letter spacing
                textAlign: 'center',
                maxWidth: '1000px',
                mx: 'auto',
                px: { xs: 2, sm: 3, md: 0 }, // Responsive padding
                // Responsive font sizes optimized for two-line layout
                fontSize: {
                  xs: '1.6rem',    // Mobile: 25.6px - slightly smaller for two lines
                  sm: '2rem',      // Small tablet: 32px  
                  md: '2.8rem',    // Medium: 44.8px
                  lg: '3.2rem',    // Large: 51.2px
                  xl: '3.6rem'     // Extra large: 57.6px
                },
                // Prevent text from breaking awkwardly
                wordBreak: 'keep-all',
                hyphens: 'none',
                // Better spacing for stacked layout
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: { xs: 0.5, sm: 0.5, md: 0.75 } // Gap between the two lines
              }}
            >
              <Box 
                component="span"
                sx={{
                  display: 'block', // Always display as block to create new line
                  mb: { xs: 1, sm: 1, md: 1.5 }, // Margin bottom for spacing between lines
                  fontSize: {
                    xs: '2rem',      // Mobile: 32px - larger than animated text
                    sm: '2.5rem',    // Small tablet: 40px  
                    md: '3.5rem',    // Medium: 56px - significantly larger
                    lg: '4rem',      // Large: 64px
                    xl: '4.5rem'     // Extra large: 72px
                  },
                  fontWeight: 800,   // Make it bolder
                  letterSpacing: { xs: '-0.02em', sm: '-0.025em', md: '-0.03em' }
                }}
              >
                Unlock Efficiency with
              </Box>
              <Box 
                component="span" 
                sx={{ 
                  background: 'linear-gradient(135deg, #00ffdc 0%, #5f7fff 2%, #00ffdc 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  minHeight: { xs: '1.5em', sm: '1.2em', md: '1.1em' }, // Responsive min height
                  display: 'block', // Display as block to be on new line
                  width: '100%', // Full width
                  textAlign: 'center', // Center the animated text
                  position: 'relative',
                  transition: 'opacity 0.5s ease-in-out',
                  opacity: fadeClass === 'fade-in' ? 1 : 0
                }}
              >
                {phrases[currentPhraseIndex]}
              </Box>
            </Typography>
          </div>

          {/* Hero Content Container - Simplified */}
          <Box
            sx={{
              position: 'relative',
              zIndex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              pointerEvents: 'none' // Container doesn't block clicks
            }}
          >
            {/* Floating Capabilities Component - Fixed pointer events */}
            <Box
              sx={{
                position: 'relative',
                width: '100%',
                transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
                ...(isCapabilitiesFloating && !isMobile && {
                  height: 0,
                  overflow: 'visible',
                  marginBottom: 0
                }),
                ...(!isCapabilitiesFloating && {
                  height: 'auto',
                  marginBottom: { xs: 2, sm: 3, md: 4 }
                }),
                pointerEvents: 'none' // Prevents blocking
              }}
            >
              {/* <HomeCapabilitiesFloating /> */}
            </Box>

            {/* Main Content - Simplified positioning */}
            <Box
              sx={{
                position: 'relative',
                width: '100%',
                maxWidth: '100%',
                transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
                transform: isCapabilitiesFloating && !isMobile 
                  ? 'translateY(-40px)' // Reduced from -80px to prevent overlap
                  : 'translateY(0)',
                paddingTop: isCapabilitiesFloating && !isMobile ? 2 : { xs: 1, sm: 2, md: 3 }, // Added minimum padding
                pointerEvents: 'none' // Container doesn't interfere
              }}
            >
              {/* Subtitle - Simplified */}
              <div 
                style={{
                  marginTop: isCapabilitiesFloating ? '3rem' : '2rem', // Increased spacing when floating
                  transition: 'margin-top 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
                  pointerEvents: 'none' // Text doesn't interfere
                }}
              >
            <Typography 
              variant="h5" 
              sx={{ 
                color: 'text.secondary', 
                maxWidth: 700, 
                mx: 'auto', 
                mb: 3,
                lineHeight: 1.6,
                fontWeight: 400,
                opacity: 0.9
              }}
            >
              Leverage AI and ML to analyze incident and service desk tickets with unmatched speed and precision—empowering smarter decisions through advanced analytics.
            </Typography>
          </div>

          {/* CTA Buttons */}
          <div style={{ pointerEvents: 'auto' }}>
            <Stack 
              direction={{ xs: 'column', sm: 'row' }} 
              spacing={2} 
              justifyContent="center" 
              alignItems="center"
              sx={{ mb: 6 }}
            >
              <Button
                component={Link}
                to="/about"
                variant="outlined"
                size="small"
                sx={{
                  borderColor: '#00ffdc',
                  color: '#00ffdc',
                  fontWeight: 600,
                  px: { xs: 2, sm: 2.5, md: 2.5 },
                  py: { xs: 0.8, sm: 1, md: 1 },
                  fontSize: { xs: '0.75rem', sm: '0.8rem', md: '0.8rem' },
                  minWidth: { xs: 120, sm: 140, md: 140 },
                  maxWidth: { xs: '180px', sm: 'none' },
                  borderWidth: 2,
                  borderRadius: '20px',
                  position: 'relative',
                  cursor: 'pointer',
                  zIndex: 1,
                  pointerEvents: 'auto',
                  '&:hover': {
                    borderColor: '#00f0e6',
                    backgroundColor: 'rgba(0, 255, 220, 0.15)',
                    color: '#ffffff',
                    transform: 'translateY(-2px)',
                    boxShadow: '0 6px 20px rgba(0, 255, 220, 0.4)',
                    zIndex: 10,
                    pointerEvents: 'auto'
                  },
                  '&:active': {
                    transform: 'translateY(0px)',
                    boxShadow: '0 2px 10px rgba(0, 255, 220, 0.3)'
                  },
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)'
                }}
              >
                Learn More
              </Button>
            </Stack>
          </div>

          {/* Discover More Section - After buttons */}
          <Box
            onClick={() => {
              const nextSection = document.querySelector('#capabilities-section') || 
                                document.querySelector('[data-section="next"]') ||
                                document.querySelector('.MuiContainer-root:nth-of-type(2)');
              if (nextSection) {
                nextSection.scrollIntoView({ 
                  behavior: 'smooth', 
                  block: 'start' 
                });
              } else {
                window.scrollBy({
                  top: window.innerHeight * 0.8,
                  behavior: 'smooth'
                });
              }
            }}
            sx={{
              maxWidth: 800,
              mx: 'auto',
              textAlign: 'center',
              mb: { xs: 2, sm: 3 },
              cursor: 'pointer',
              pointerEvents: 'auto'
            }}
          >
            <Typography
              variant="caption"
              sx={{
                color: isCapabilitiesFloating ? 'rgba(255, 255, 255, 0.8)' : 'rgba(255, 255, 255, 0.5)',
                  fontSize: '0.75rem',
                  fontWeight: 500,
                  letterSpacing: '1px',
                  textTransform: 'uppercase',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 1,
                  cursor: 'pointer',
                  transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    color: 'rgba(255, 255, 255, 0.9)',
                    transform: 'translateY(-1px)'
                  }
                }}
              >
                Discover More
                <KeyboardArrowDownIcon 
                  sx={{ 
                    fontSize: 16,
                    color: '#00ffdc',
                    filter: 'drop-shadow(0 2px 4px rgba(0, 255, 220, 0.5))',
                    transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)'
                  }} 
                />
              </Typography>
            </Box>
          
            </Box> {/* Close Main Content Container */}
          </Box> {/* Close Hero Content Container */}

          {/* Scroll Indicator */}
          <div
            style={{
              animation: 'bounce 2s infinite ease-in-out',
              pointerEvents: 'none'
            }}
          >
            <KeyboardArrowDownIcon 
              sx={{ 
                color: 'text.disabled', 
                fontSize: 32,
                opacity: 0.6
              }} 
            />
          </div>
        </Container>
      </Box>

      {/* All Sections Below Hero - Unified Space Filling Container */}
      <Box
        sx={{
          position: 'relative',
          transition: 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
          transform: isCapabilitiesFloating && !isMobile 
            ? 'translateY(-80px)' 
            : 'translateY(0)',
        }}
      >
        {/* Features Section - Professional showcase */}
        <Box
          id="capabilities-section"
          component={motion.section}
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          sx={{
            py: { xs: 8, sm: 10, md: 12 },
            position: 'relative',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              height: '1px',
              background: 'linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent)'
            }
          }}
        >
          <Container maxWidth="lg" sx={{ pointerEvents: 'auto' }}>
            <div style={{ pointerEvents: 'none' }}>
              <Box sx={{ textAlign: 'center', mb: 8 }}>
                <Typography 
                  variant="h2" 
                  sx={{ 
                    fontWeight: 600,
                    mb: 2,
                    background: 'linear-gradient(135deg, #00ffdc 0%, #5f7fff 2%, #00ffdc 100%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                  }}
                >
                  Platform Capabilities
                </Typography>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    color: 'text.secondary',
                    maxWidth: 600,
                    mx: 'auto',
                    fontWeight: 400,
                    lineHeight: 1.6
                  }}
                >
                  Discover enterprise-grade AI solutions designed to scale with your business
                </Typography>
              </Box>
            </div>

            {/* Grid layout with 3 columns on larger screens, 2 on medium, 1 on small */}
            <Grid container spacing={3} sx={{ justifyContent: 'center' }}>
              {features.map((feature, index) => (
                <Grid 
                  size={{ xs: 12, sm: 6, md: 4, lg: 4, xl: 4 }}
                  key={index}
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                  }}
                >
                  <Box sx={{ width: '100%', maxWidth: 350 }}> {/* Max width for consistency */}
                    <CapabilityCard3D
                      icon={feature.icon}
                      title={feature.title}
                      description={feature.description}
                      status={feature.status}
                      features={feature.features}
                      gradient={feature.gradient}
                      delay={index * 0.1}
                      onClick={() => window.location.href = feature.path}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Container>
        </Box>
      </Box>
    </Box>
  );
};

export default ProfessionalHomePage;
