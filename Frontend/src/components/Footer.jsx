import React from 'react';
import Logo from './Logo';
import { 
  Box, 
  Typography, 
  Container, 
  useTheme,
  Grid,
  Divider,
  Link as MuiLink,
  Stack
} from '@mui/material';
import { 
  Bolt as BoltIcon, 
  Copyright as CopyrightIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  TrendingUp as TrendingUpIcon,
  Language as LanguageIcon,
  LinkedIn as LinkedInIcon,
  Twitter as TwitterIcon,
  Mail as MailIcon
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const Footer = () => {
  const theme = useTheme();

  // Business metrics to showcase
  const metrics = [
    { icon: TrendingUpIcon, value: '99.9%', label: 'Uptime' },
    { icon: SpeedIcon, value: '<100ms', label: 'Response Time' },
    { icon: SecurityIcon, value: 'SOC2', label: 'Compliant' },
  ];

  // Footer links organized by category
  const footerLinks = [
    {
      title: 'Product',
      links: [
        // { label: 'Features', href: '/404' },
        { label: 'Pricing', href: '/404' },
        { label: 'Security', href: '/404' },
        { label: 'Documentation', href: '/404' },
      ]
    },

    {
      title: 'Legal',
      links: [
        { label: 'Privacy Policy', href: '/404' },
        { label: 'Terms of Service', href: '/404' },
        // { label: 'Compliance', href: '/404' },
        { label: 'Accessibility', href: '/404' },
      ]
    }
  ];

  return (
    <Box
      component="footer"
      sx={{
        background: 'linear-gradient(135deg, #1e2a3a 0%, #2a3b4a 100%)',
        borderTop: '1px solid',
        borderColor: 'rgba(102, 255, 224, 0.1)',
        pt: 6,
        pb: 4,
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Background Pattern */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          opacity: 0.025,
          backgroundImage: `
            radial-gradient(circle at 25% 25%, #5fffe0 1px, transparent 1px),
            radial-gradient(circle at 75% 75%, #8b5cf6 1px, transparent 1px)
          `,
          backgroundSize: '30px 30px',
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        {/* SECTION 1: Top Hero Section - Logo & Description */}
        <Box sx={{ mb: 1 }}>
          <Grid container spacing={1} alignItems="stretch">
            {/* Left Column - Brand */}
            <Grid item xs={12} sm={6} md={5}>
              <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
                {/* Logo */}
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  style={{ width: 'fit-content', marginBottom: '0.5rem' }}
                >
                  <Logo size="md" />
                </motion.div>

                {/* Description */}
                {/* <Typography 
                  variant="body2" 
                  sx={{ 
                    color: 'rgba(255, 255, 255, 0.75)',
                    fontSize: '0.95rem',
                    lineHeight: 1.8,
                    letterSpacing: '0.3px',
                    flex: 1,
                    maxWidth: '350px'
                  }}
                >
                  Enterprise-grade AI automation and analytics platform transforming business operations through intelligent process optimization.
                </Typography> */}
              </Box>
            </Grid>


          </Grid>
        </Box>

        {/* SECTION 2: Resources Links - Full Width */}
        <Divider sx={{ 
          my: 0.5, 
          background: 'linear-gradient(90deg, transparent, rgba(102, 255, 224, 0.2), transparent)',
          borderColor: 'transparent'
        }} />

        <Box sx={{ mb: 1 }}>
          <Grid container spacing={1} sx={{ justifyContent: 'space-between' }}>
            {/* LEFT GROUP: Product & Legal */}
            {footerLinks.map((section, idx) => (
              <Grid item xs={6} sm={6} md={2.4} key={idx}>
                <Box>
                  <Typography 
                    sx={{ 
                      fontSize: '0.7rem',
                      fontWeight: 800,
                      color: '#66FFE0',
                      mb: 1,
                      textTransform: 'uppercase',
                      letterSpacing: '1.2px',
                      paddingBottom: '0.5rem',
                      borderBottom: '2px solid rgba(102, 255, 224, 0.15)'
                    }}
                  >
                    {section.title}
                  </Typography>
                  <Stack spacing={0.8}>
                    {section.links.map((link, linkIdx) => (
                      <motion.div key={linkIdx} whileHover={{ translateX: 8 }}>
                        <MuiLink
                          href={link.href}
                          sx={{
                            color: 'rgba(255, 255, 255, 0.68)',
                            textDecoration: 'none',
                            fontSize: '0.8rem',
                            transition: 'all 0.3s ease',
                            display: 'inline-block',
                            fontWeight: 500,
                            letterSpacing: '0.2px',
                            '&:hover': {
                              color: '#66FFE0',
                              paddingLeft: '6px'
                            }
                          }}
                        >
                          {link.label}
                        </MuiLink>
                      </motion.div>
                    ))}
                  </Stack>
                </Box>
              </Grid>
            ))}

            {/* RIGHT GROUP: Core Features, Compliance, Technology */}
            {/* Core Features */}
            <Grid item xs={6} sm={6} md={2.4}>
              <Box>
                <Typography sx={{ fontSize: '0.7rem', fontWeight: 800, color: '#66FFE0', mb: 1, textTransform: 'uppercase', letterSpacing: '1.2px', paddingBottom: '0.5rem', borderBottom: '2px solid rgba(102, 255, 224, 0.15)' }}>
                  Core Features
                </Typography>
                <Stack spacing={0.8}>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Ticket Analysis</Typography>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>AI Automation</Typography>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Analytics Engine</Typography>
                  {/* <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Workflow Hub</Typography> */}
                </Stack>
              </Box>
            </Grid>

            {/* Compliance */}
            <Grid item xs={6} sm={6} md={2.4}>
              <Box>
                <Typography sx={{ fontSize: '0.7rem', fontWeight: 800, color: '#66FFE0', mb: 1, textTransform: 'uppercase', letterSpacing: '1.2px', paddingBottom: '0.5rem', borderBottom: '2px solid rgba(102, 255, 224, 0.15)' }}>
                  Compliance
                </Typography>
                <Stack spacing={0.8}>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>SOC2 Type II</Typography>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>ISO 27001</Typography>
                  {/* <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>GDPR Ready</Typography> */}
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Data Encryption</Typography>
                </Stack>
              </Box>
            </Grid>

            {/* Technology */}
            <Grid item xs={6} sm={6} md={2.4}>
              <Box>
                <Typography sx={{ fontSize: '0.7rem', fontWeight: 800, color: '#66FFE0', mb: 1, textTransform: 'uppercase', letterSpacing: '1.2px', paddingBottom: '0.5rem', borderBottom: '2px solid rgba(102, 255, 224, 0.15)' }}>
                  Technology
                </Typography>
                <Stack spacing={0.8}>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Advanced AI Engine</Typography>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Real-time Analytics</Typography>
                  <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>ML Pipeline</Typography>
                  {/* <Typography sx={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.68)', letterSpacing: '0.2px', fontWeight: 500 }}>Cloud Native</Typography> */}
                </Stack>
              </Box>
            </Grid>
          </Grid>
        </Box>

        {/* SECTION 3: Bottom Section */}
        <Divider sx={{ 
          my: 0.5, 
          background: 'linear-gradient(90deg, transparent, rgba(102, 255, 224, 0.2), transparent)',
          borderColor: 'transparent'
        }} />

        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' },
            gap: 2,
            mb: 1,
            alignItems: 'center'
          }}
        >
          {/* Copyright Left */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.8 }}>
            <CopyrightIcon sx={{ fontSize: 13, color: 'rgba(255, 255, 255, 0.5)' }} />
            <Typography 
              variant="caption" 
              sx={{ 
                color: 'rgba(255, 255, 255, 0.65)',
                fontSize: '0.75rem',
                fontWeight: 600,
                letterSpacing: '0.3px'
              }}
            >
              {new Date().getFullYear()} PRISM ANALYTICS
            </Typography>
          </Box>

          {/* Center Status */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: { xs: 'flex-start', md: 'center' }, gap: 1.5, flexWrap: 'wrap' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box
                sx={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  background: '#10b981',
                  animation: 'pulse 2s ease-in-out infinite',
                  '@keyframes pulse': {
                    '0%, 100%': { opacity: 1 },
                    '50%': { opacity: 0.4 }
                  }
                }}
              />
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.65)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  letterSpacing: '0.3px'
                }}
              >
                All Systems Operational
              </Typography>
            </Box>
          </Box>

          {/* Right - Additional Badges */}
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: { xs: 'flex-start', md: 'flex-end' }, gap: 2.5, flexWrap: 'wrap' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.8 }}>
              <BoltIcon sx={{ fontSize: 15, color: '#66FFE0' }} />
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.65)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  letterSpacing: '0.3px'
                }}
              >
                AI Powered
              </Typography>
            </Box>

            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.8 }}>
              <SecurityIcon sx={{ fontSize: 15, color: '#6366f1' }} />
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'rgba(255, 255, 255, 0.65)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  letterSpacing: '0.3px'
                }}
              >
                Enterprise Grade
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* SECTION 5: Platform Tagline & CTA
        <Box sx={{ 
          textAlign: 'center', 
          borderTop: '1px solid rgba(102, 255, 224, 0.08)', 
          borderBottom: '1px solid rgba(102, 255, 224, 0.08)',
          pt: 1,
          pb: 1,
          px: 2,
          borderRadius: '12px',
          background: 'rgba(102, 255, 224, 0.02)',
          mb: 0.5
        }}>
          <Typography 
            variant="caption" 
            sx={{ 
              color: 'rgba(102, 255, 224, 0.85)',
              fontSize: { xs: '0.75rem', sm: '0.8rem' },
              fontWeight: 700,
              display: 'block',
              mb: 0.3,
              letterSpacing: '1px',
              textTransform: 'uppercase'
            }}
          >
            Transforming Enterprise Operations
          </Typography>
          <Typography 
            variant="caption" 
            sx={{ 
              color: 'rgba(255, 255, 255, 0.55)',
              fontSize: { xs: '0.7rem', sm: '0.75rem' },
              display: 'block',
              letterSpacing: '0.3px',
              lineHeight: 1.6
            }}
          >
            Through Intelligent Automation & Advanced Analytics
          </Typography>
        </Box> */}

        {/* SECTION 6: Bottom Footer Attribution */}
        <Box sx={{ textAlign: 'center', pb: 1 }}>
          <Typography 
            variant="caption" 
            sx={{ 
              color: 'rgba(255, 255, 255, 0.45)',
              fontSize: '0.7rem',
              fontWeight: 500,
              letterSpacing: '0.2px'
            }}
          >
            All rights reserved. Made with ❤️ by the PRISM ANALYTICS Team
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;