import React from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';
import { 
  Container, 
  Typography, 
  Box, 
  Stack,
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
import useScrollToTop from '../hooks/useScrollToTop';
import '../styles/corporate-parallax.css';

const AboutUsPage = () => {
  useScrollToTop();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  
  // Parallax scroll hook for smooth animations
  const { scrollY, scrollDirection, getParallaxOffset, getParallaxOpacity, getParallaxScale } = useParallaxScroll();
  
  // Framer Motion scroll hooks for advanced effects
  const { scrollYProgress } = useScroll();
  
  // Optimized smooth spring animations for performance
  const smoothY = useSpring(scrollY, { 
    stiffness: 80, 
    damping: 40, 
    mass: 0.5,
    restDelta: 0.01,
    restSpeed: 0.01
  });
  
  // Optimized parallax transforms for better performance
  const heroParallax = useTransform(smoothY, [0, 800], [0, -150]);
  const aboutParallax = useTransform(smoothY, [300, 1000], [0, -100]);
  const teamParallax = useTransform(smoothY, [600, 1200], [0, -80]);
  const valuesParallax = useTransform(smoothY, [900, 1500], [0, -60]);
  
  // Lighter background parallax for performance
  const backgroundParallax = useTransform(smoothY, [0, 2000], [0, -300]);

  const teamMembers = [
    {
      name: 'Rakesh Ranjan',
      role: 'Product Manager',
      avatar: <BusinessIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Product Strategy', 'User Experience', 'Market Analysis'],
      description: 'Driving product vision and ensuring our AI solutions meet enterprise needs and user expectations.'
    },
    {
      name: 'Devendra Desai',
      role: 'Teachnical Architect',
      avatar: <BusinessIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['System Design', 'Cloud Architecture', 'AI Integration', 'Scalability'],
      description: 'Designing enterprise-level architecture and ensuring technical excellence across all AI-driven solutions and platforms.'
    },
    {
      name: 'Anurag Thakur',
      role: 'Team Lead',
      avatar: <ScienceIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Machine Learning', 'Neural Networks', 'AI Ethics', 'Team Leadership'],
      description: 'Leading our AI research and development with experience in advanced machine learning systems.'
    },
    {
      name: 'Soumalya Mondal',
      role: 'Backend Developer',
      avatar: <CodeIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['Python', 'Flask', 'PostgreSQL', 'API Development'],
      description: 'Building robust backend systems and RESTful APIs that power our AI-driven applications with reliability and performance.'
    },
    {
      name: 'Chahat Kumar',
      role: 'Frontend Developer',
      avatar: <AnalyticsIcon sx={{ fontSize: 40, color: '#1a1a1a' }} />,
      expertise: ['React', 'Material-UI', 'JavaScript', 'Responsive Design'],
      description: 'Crafting intuitive and engaging user interfaces with modern frontend technologies to deliver seamless user experiences.'
    },
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
        staggerChildren: 0.1,
        delayChildren: 0.05
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
        ease: "easeOut"
      }
    }
  };

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 30
    },
    visible: (index) => ({
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut",
        delay: index * 0.02
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
              scale: useTransform(scrollYProgress, [0, 0.25], [1, 0.98]),
              opacity: useTransform(scrollYProgress, [0, 0.35], [1, 0.8])
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 'clamp(32px, 6vh, 48px)' }}>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
                {/* <Logo size={isMobile ? 'md' : 'lg'} /> */}
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

          {/* Mission & Vision */}
          <div>
            <Box sx={{ 
              display: 'grid',
              gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
              gap: 3,
              mb: 'clamp(32px, 6vh, 48px)' 
            }} data-section="mission">
              <Box>
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
                      Our mission is to empower data-driven decision-making and operational excellence through the E.S.O.A.R. analysis framework by systematically Evaluating, Simplifying, Optimizing, Automating, and Reimagining workflows. We strive to deliver intelligent, scalable, and sustainable solutions that enhance productivity, minimize manual effort, and foster enterprise-wide innovation.
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
              <Box>
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
                     To be the catalyst for transformative change by establishing E.S.O.A.R. as the gold standard in analytical and automation frameworks—empowering organizations to become agile, insight-driven, and future-ready ecosystems through continuous improvement and intelligent automation.
                    </Typography>
                  </CardContent>
                </Card>
              </Box>
            </Box>
          </div>

          {/* Values Section with Parallax */}
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={containerVariants}
            style={{
              y: valuesParallax,
              scale: useTransform(scrollYProgress, [0.18, 0.55], [0.88, 1.01]),
              opacity: useTransform(scrollYProgress, [0.12, 0.32, 0.75], [0.15, 1, 0.9])
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
              <Box sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', lg: '1fr 1fr 1fr 1fr' },
                gap: 2
              }}>
                {values.map((value, index) => (
                  <Box key={index}>
                    <motion.div
                      variants={cardVariants}
                      initial="hidden"
                      whileInView="visible"
                      viewport={{ once: true, amount: 0.3 }}
                      custom={index}
                      whileHover={{ 
                        y: -5,
                        transition: { 
                          duration: 0.2,
                          ease: "easeOut"
                        }
                      }}
                    >
                      <ValuesCard 
                        value={value} 
                        index={index} 
                        size="medium"
                      />
                    </motion.div>
                  </Box>
                ))}
              </Box>
            </Box>
          </motion.div>

          {/* Team Section with Parallax */}
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.2 }}
            variants={containerVariants}
            style={{
              y: teamParallax,
              scale: useTransform(scrollYProgress, [0.28, 0.65], [0.86, 1.01]),
              opacity: useTransform(scrollYProgress, [0.22, 0.42, 0.82], [0.15, 1, 0.95])
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
              <Box sx={{
                display: 'grid',
                gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: '1fr 1fr 1fr', lg: 'repeat(5, 1fr)' },
                gap: 2
              }}>
                {teamMembers.map((member, index) => (
                  <Box key={index}>
                    <motion.div
                      variants={cardVariants}
                      initial="hidden"
                      whileInView="visible"
                      viewport={{ once: true, amount: 0.3 }}
                      custom={index}
                      whileHover={{ 
                        y: -5,
                        transition: { 
                          duration: 0.2,
                          ease: "easeOut"
                        }
                      }}
                    >
                      <TeamMemberCard 
                        member={member} 
                        index={index} 
                        size="medium"
                      />
                    </motion.div>
                  </Box>
                ))}
              </Box>
            </Box>
          </motion.div>

        </motion.div>
      </Container>
    </Box>
  );
};

export default AboutUsPage;
