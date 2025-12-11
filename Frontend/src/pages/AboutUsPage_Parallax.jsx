import React from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Avatar,
  Chip,
  useTheme,
  useMediaQuery,
  Paper,
  Divider
} from '@mui/material';
import { 
  Bolt as BoltIcon,
  Psychology as PsychologyIcon,
  AutoAwesome as AutoAwesomeIcon,
  TrendingUp as TrendingUpIcon,
  Security as SecurityIcon,
  Group as GroupIcon,
  Business as BusinessIcon,
  Science as ScienceIcon,
  Code as CodeIcon,
  Analytics as AnalyticsIcon,
  Speed as SpeedIcon
} from '@mui/icons-material';
import ParticlesBackground from '../components/ParticlesBackground';
import Logo from '../components/Logo';
import TeamMemberCard from '../components/TeamMemberCard';
import ValuesCard from '../components/ValuesCard';
import useParallaxScroll from '../hooks/useParallaxScroll';
import '../styles/corporate-parallax.css';

const AboutUsPage = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Parallax scroll hook for smooth animations
  const { scrollY, scrollDirection, getParallaxOffset, getParallaxOpacity, getParallaxScale } = useParallaxScroll();
  
  // Framer Motion scroll hooks for advanced effects
  const { scrollYProgress } = useScroll();
  
  // Smooth spring animations for corporate feel
  const smoothY = useSpring(scrollY, { stiffness: 100, damping: 30 });
  
  // Mathematical parallax transforms for different sections
  const heroParallax = useTransform(smoothY, [0, 1000], [0, -200]);
  const aboutParallax = useTransform(smoothY, [200, 1200], [0, -150]);
  const teamParallax = useTransform(smoothY, [800, 1800], [0, -100]);
  const valuesParallax = useTransform(smoothY, [1200, 2200], [0, -80]);
  
  // Background parallax for depth
  const backgroundParallax = useTransform(smoothY, [0, 2000], [0, -400]);

  const teamMembers = [
    {
      name: 'Devendra Dessai',
      role: 'Technical Architect',
      avatar: <ScienceIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Machine Learning', 'Neural Networks', 'AI Ethics'],
      description: 'Leading our AI research and development with 15+ years of experience in advanced machine learning systems.'
    },
    {
      name: 'Marcus Rodriguez',
      role: 'Head of Engineering',
      avatar: <CodeIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['System Architecture', 'Cloud Computing', 'DevOps'],
      description: 'Architecting scalable solutions and leading our engineering team to deliver enterprise-grade AI platforms.'
    },
    {
      name: 'Dr. Emily Watson',
      role: 'Data Science Lead',
      avatar: <AnalyticsIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Data Analytics', 'Predictive Modeling', 'RAG Systems'],
      description: 'Specializing in data-driven insights and implementing cutting-edge RAG technologies for knowledge extraction.'
    },
    {
      name: 'Alex Thompson',
      role: 'Product Manager',
      avatar: <BusinessIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Product Strategy', 'User Experience', 'Market Analysis'],
      description: 'Driving product vision and ensuring our AI solutions meet enterprise needs and user expectations.'
    }
  ];

  const values = [
    {
      icon: <SecurityIcon sx={{ fontSize: 32, color: '#66FFE0' }} />,
      title: 'Security First',
      description: 'Enterprise-grade security with end-to-end encryption and compliance with industry standards.'
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 32, color: '#66FFE0' }} />,
      title: 'Performance Optimized',
      description: 'Lightning-fast AI processing with sub-100ms response times and 99.9% uptime guarantee.'
    },
    {
      icon: <AutoAwesomeIcon sx={{ fontSize: 32, color: '#66FFE0' }} />,
      title: 'Innovation Driven',
      description: 'Cutting-edge AI research and continuous improvement of our machine learning models.'
    },
    {
      icon: <TrendingUpIcon sx={{ fontSize: 32, color: '#66FFE0' }} />,
      title: 'Scalable Solutions',
      description: 'Cloud-native architecture designed to scale with your business needs and growth.'
    }
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
    hidden: { opacity: 0, y: 30, scale: 0.95 },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: {
        duration: 0.8,
        ease: [0.25, 0.46, 0.45, 0.94],
        staggerChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 50,
      scale: 0.9,
      rotateX: 10
    },
    visible: (index) => ({
      opacity: 1,
      y: 0,
      scale: 1,
      rotateX: 0,
      transition: {
        duration: 0.6 + (index * 0.1),
        ease: [0.25, 0.46, 0.45, 0.94],
        delay: index * 0.1
      }
    })
  };

  return (
    <Box sx={{ minHeight: '100vh', position: 'relative', overflow: 'hidden' }} className="corporate-parallax-container">
      {/* Corporate Scroll Progress Indicator */}
      <motion.div
        className="scroll-progress-indicator"
        style={{ scaleX: scrollYProgress }}
      />
      
      {/* Background with parallax effect */}
      <motion.div
        style={{
          y: backgroundParallax,
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: -1
        }}
      >
        <ParticlesBackground />
        <div className="corporate-gradient-overlay" />
      </motion.div>
      
      <Container maxWidth="lg" sx={{ pt: 'clamp(48px, 8vh, 64px)', pb: 'clamp(32px, 6vh, 48px)' }}>
        {/* Hero Section with Parallax */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          style={{
            y: heroParallax,
          }}
        >
          <motion.div 
            variants={itemVariants}
            style={{
              scale: useTransform(scrollYProgress, [0, 0.2], [1, 0.95]),
              opacity: useTransform(scrollYProgress, [0, 0.3], [1, 0.7])
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 'clamp(32px, 6vh, 48px)' }}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                <Logo size={isMobile ? 'md' : 'lg'} />
                <Typography 
                  variant={isMobile ? 'h5' : 'h4'}
                  sx={{ 
                    fontWeight: 700, 
                    mb: 'clamp(12px, 2vh, 16px)',
                    fontSize: 'clamp(1.3rem, 4vw, 2.5rem)',
                    background: 'linear-gradient(135deg, #66FFE0, #6366f1)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    color: 'transparent'
                  }}
                  className="corporate-text-reveal"
                >
                  ABOUT US
                </Typography>
                <Typography 
                  variant="h6" 
                  sx={{ 
                    color: 'text.secondary', 
                    maxWidth: 'clamp(300px, 80%, 600px)', 
                    mx: 'auto',
                    fontSize: 'clamp(0.9rem, 2.5vw, 1.1rem)',
                    lineHeight: 1.7,
                    fontWeight: 400
                  }}
                >
                  Empowering businesses with cutting-edge AI solutions and intelligent automation 
                  that transform how businesses operate, analyze, and innovate.
                </Typography>
              </Box>
            </Box>
          </motion.div>

          {/* Mission & Vision with Parallax */}
          <motion.div 
            variants={itemVariants}
            style={{
              y: aboutParallax,
              scale: useTransform(scrollYProgress, [0.1, 0.4], [0.95, 1]),
              opacity: useTransform(scrollYProgress, [0.05, 0.2, 0.6], [0.3, 1, 0.8])
            }}
          >
            <Grid container spacing={3} sx={{ mb: 'clamp(32px, 6vh, 48px)' }} data-section="mission">
              <Grid size={{ xs: 12, md: 6 }}>
                <Card sx={{ 
                  height: '100%', 
                  background: 'rgba(255, 255, 255, 0.03)', 
                  backdropFilter: 'blur(8px)',
                  borderRadius: 'clamp(8px, 1.5vw, 12px)',
                  minHeight: 'clamp(140px, 18vh, 180px)'
                }} className="corporate-card-hover">
                  <CardContent sx={{ p: 'clamp(16px, 3vw, 24px)' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 'clamp(12px, 2vh, 16px)' }}>
                      <BoltIcon sx={{ fontSize: 'clamp(24px, 4vw, 28px)', color: '#66FFE0', mr: 2 }} />
                      <Typography variant="h6" sx={{ fontWeight: 600, fontSize: 'clamp(1rem, 2.5vw, 1.2rem)' }}>
                        Our Mission
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ 
                      lineHeight: 1.6, 
                      color: 'text.secondary',
                      fontSize: 'clamp(0.8rem, 2vw, 0.9rem)'
                    }}>
                      To democratize artificial intelligence by providing accessible, secure, and powerful 
                      AI solutions that empower businesses to make data-driven decisions and achieve 
                      unprecedented levels of efficiency and innovation.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid size={{ xs: 12, md: 6 }}>
                <Card sx={{ 
                  height: '100%', 
                  background: 'rgba(255, 255, 255, 0.03)', 
                  backdropFilter: 'blur(8px)',
                  borderRadius: 'clamp(8px, 1.5vw, 12px)',
                  minHeight: 'clamp(140px, 18vh, 180px)'
                }} className="corporate-card-hover">
                  <CardContent sx={{ p: 'clamp(16px, 3vw, 24px)' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 'clamp(12px, 2vh, 16px)' }}>
                      <AutoAwesomeIcon sx={{ fontSize: 'clamp(24px, 4vw, 28px)', color: '#66FFE0', mr: 2 }} />
                      <Typography variant="h6" sx={{ fontWeight: 600, fontSize: 'clamp(1rem, 2.5vw, 1.2rem)' }}>
                        Our Vision
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ 
                      lineHeight: 1.6, 
                      color: 'text.secondary',
                      fontSize: 'clamp(0.8rem, 2vw, 0.9rem)'
                    }}>
                      To be the global leader in AI innovation, creating a future where intelligent 
                      technology seamlessly integrates with human potential to solve complex challenges 
                      and unlock new possibilities across industries.
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </motion.div>

          {/* Values Section with Parallax */}
          <motion.div 
            variants={itemVariants}
            style={{
              y: valuesParallax,
              scale: useTransform(scrollYProgress, [0.2, 0.5], [0.9, 1]),
              opacity: useTransform(scrollYProgress, [0.15, 0.3, 0.7], [0.2, 1, 0.85])
            }}
          >
            <Box sx={{ mb: 'clamp(32px, 6vh, 48px)' }} data-section="values" className="corporate-section">
              <Typography variant="h4" sx={{ 
                textAlign: 'center', 
                mb: 'clamp(24px, 4vh, 32px)', 
                fontWeight: 600,
                fontSize: 'clamp(1.5rem, 4vw, 2rem)'
              }}>
                Our Core Values
              </Typography>
              <Grid container spacing={2}>
                {values.map((value, index) => (
                  <Grid key={index} size={{ xs: 12, sm: 6, lg: 3 }}>
                    <motion.div
                      variants={cardVariants}
                      initial="hidden"
                      whileInView="visible"
                      viewport={{ once: true, amount: 0.3 }}
                      custom={index}
                      whileHover={{ 
                        y: -8,
                        scale: 1.02,
                        transition: { duration: 0.3 }
                      }}
                    >
                      <ValuesCard 
                        value={value} 
                        index={index} 
                        size="medium"
                      />
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </motion.div>

          {/* Team Section with Parallax */}
          <motion.div 
            variants={itemVariants}
            style={{
              y: teamParallax,
              scale: useTransform(scrollYProgress, [0.3, 0.6], [0.9, 1]),
              opacity: useTransform(scrollYProgress, [0.25, 0.4, 0.8], [0.2, 1, 0.9])
            }}
          >
            <Box sx={{ mb: 'clamp(32px, 6vh, 48px)' }} data-section="team" className="corporate-section">
              <Typography variant="h4" sx={{ 
                textAlign: 'center', 
                mb: 'clamp(16px, 3vh, 24px)', 
                fontWeight: 600,
                fontSize: 'clamp(1.5rem, 4vw, 2rem)'
              }}>
                Meet Our Team
              </Typography>
              <Typography 
                variant="body1" 
                sx={{ 
                  textAlign: 'center', 
                  mb: 'clamp(24px, 4vh, 32px)', 
                  color: 'text.secondary',
                  maxWidth: 'clamp(300px, 70%, 500px)',
                  mx: 'auto',
                  fontSize: 'clamp(0.85rem, 2.2vw, 1rem)',
                  lineHeight: 1.6
                }}
              >
                Our diverse team of AI experts, engineers, and innovators work together 
                to push the boundaries of what's possible with artificial intelligence.
              </Typography>
              <Grid container spacing={2}>
                {teamMembers.map((member, index) => (
                  <Grid key={index} size={{ xs: 12, sm: 6, lg: 3 }}>
                    <motion.div
                      variants={cardVariants}
                      initial="hidden"
                      whileInView="visible"
                      viewport={{ once: true, amount: 0.3 }}
                      custom={index}
                      whileHover={{ 
                        y: -10,
                        rotateY: 5,
                        transition: { duration: 0.3 }
                      }}
                    >
                      <TeamMemberCard 
                        member={member} 
                        index={index} 
                        size="medium"
                      />
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </motion.div>

          {/* Contact CTA with Parallax */}
          <motion.div 
            variants={itemVariants}
            style={{
              y: useTransform(scrollYProgress, [0.6, 1], [100, -50]),
              scale: useTransform(scrollYProgress, [0.6, 0.9], [0.95, 1]),
              opacity: useTransform(scrollYProgress, [0.5, 0.7, 1], [0.3, 1, 0.9])
            }}
          >
            <Card sx={{ 
              background: 'linear-gradient(135deg, rgba(95, 255, 224, 0.15), rgba(99, 102, 241, 0.15))',
              backdropFilter: 'blur(10px)',
              border: 'rgba(95, 255, 224, 0.3)',
              borderRadius: 'clamp(12px, 2vw, 16px)',
              minHeight: 'clamp(180px, 22vh, 220px)'
            }} className="corporate-card-hover">
              <CardContent sx={{ p: 'clamp(24px, 4vw, 32px)', textAlign: 'center' }}>
                <Typography variant="h5" sx={{ 
                  mb: 'clamp(16px, 3vh, 24px)', 
                  fontWeight: 600,
                  fontSize: 'clamp(1.2rem, 3.5vw, 1.5rem)'
                }}>
                  Ready to Transform Your Business?
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ 
                  mb: 'clamp(20px, 4vh, 28px)', 
                  maxWidth: 'clamp(300px, 70%, 500px)', 
                  mx: 'auto',
                  fontSize: 'clamp(0.85rem, 2.2vw, 1rem)',
                  lineHeight: 1.6
                }}>
                  Join thousands of businesses already leveraging PRISM ANALYTICS's AI capabilities 
                  to drive innovation and achieve remarkable results.
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
                  <Chip
                    label="Get Started"
                    sx={{
                      background: '#66FFE0',
                      color: 'black',
                      fontWeight: 600,
                      px: 'clamp(12px, 2vw, 16px)',
                      py: 'clamp(4px, 1vh, 6px)',
                      fontSize: 'clamp(0.85rem, 2vw, 1rem)',
                      cursor: 'pointer',
                      minHeight: 'clamp(32px, 6vw, 40px)',
                      '&:hover': {
                        background: '#4ce8c9',
                        transform: 'translateY(-1px)'
                      }
                    }}
                    className="corporate-performance-optimized"
                  />
                  <Chip
                    label="Contact Sales"
                    variant="outlined"
                    sx={{
                      borderColor: '#66FFE0',
                      color: '#66FFE0',
                      fontWeight: 600,
                      px: 'clamp(12px, 2vw, 16px)',
                      py: 'clamp(4px, 1vh, 6px)',
                      fontSize: 'clamp(0.85rem, 2vw, 1rem)',
                      cursor: 'pointer',
                      minHeight: 'clamp(32px, 6vw, 40px)',
                      '&:hover': {
                        background: 'rgba(102, 255, 224, 0.1)',
                        transform: 'translateY(-1px)'
                      }
                    }}
                    className="corporate-performance-optimized"
                  />
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      </Container>
    </Box>
  );
};

export default AboutUsPage;
