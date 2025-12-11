import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Button, 
  IconButton, 
  Box,
  useTheme,
  useMediaQuery,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Avatar
} from '@mui/material';
import { 
  Menu as MenuIcon,
  Home as HomeIcon,
  Add as AddIcon,
  Analytics as AnalyticsIcon,
  Close as CloseIcon,
  Settings as SettingsIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { motion, useAnimation } from 'framer-motion';

const Header = ({ isDarkMode, toggleTheme }) => {
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = React.useState(false);
  // Pulse trigger key to restart animation on route change
  const [pulseKey, setPulseKey] = useState(0); // retained if future key-based animations needed
  const mobileGearControls = useAnimation();
  const desktopGearControls = useAnimation();

  useEffect(() => {
    // Route change spring-based pulse sequence (async for chaining)
    (async () => {
      // Mobile cluster pulse
      await mobileGearControls.start({
        scale: 1.22,
        transition: { type: 'spring', stiffness: 260, damping: 18, mass: 0.9 }
      });
      await mobileGearControls.start({
        scale: 1,
        transition: { type: 'spring', stiffness: 180, damping: 20 }
      });
      // Desktop cluster pulse
      await desktopGearControls.start({
        scale: 1.25,
        transition: { type: 'spring', stiffness: 260, damping: 17, mass: 0.9 }
      });
      await desktopGearControls.start({
        scale: 1,
        transition: { type: 'spring', stiffness: 180, damping: 20 }
      });
    })();
    setPulseKey(k => k + 1); // keep for potential keyed re-renders
  }, [location.pathname, mobileGearControls, desktopGearControls]);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleDrawerClose = () => {
    setMobileOpen(false);
  };

  // Get page info based on route
  const getPageInfo = () => {
    switch (location.pathname) {
      case '/newrequest':
        return { title: 'New Request', icon: <AddIcon /> };
      case '/analysisenginepage':
        return { title: 'Analysis Engine', icon: <AnalyticsIcon /> };
      case '/about':
        return { title: 'About Us', icon: <InfoIcon /> };
      default:
        return { title: '', icon: null };
    }
  };

  const pageInfo = getPageInfo();

  // Navigation items
  const navItems = [
    { text: 'Home', path: '/', icon: <HomeIcon /> },
    { text: 'About', path: '/about', icon: <InfoIcon /> }
  ];

  const drawer = (
    <Box sx={{ width: 250 }} role="presentation" onClick={handleDrawerClose}>
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Dual stacked gears (mobile drawer) */}
          <motion.div
            animate={mobileGearControls}
            initial={false}
            onHoverStart={() => {
              mobileGearControls.start({ scale: 1.1, transition: { type: 'spring', stiffness: 320, damping: 18 } });
            }}
            onHoverEnd={() => {
              mobileGearControls.start({
                scale: [1.1, 1.03, 0.98, 1.015, 1],
                transition: { duration: 0.55, ease: 'easeOut' }
              });
            }}
          >
          <Box 
            sx={{ 
              position: 'relative', 
              width: 34, 
              height: 28,
              '&:hover .gear-rot': { animationPlayState: 'paused' }
            }}
          >
            <SettingsIcon
              sx={{
                position: 'absolute',
                left: 0,
                top: 2,
                fontSize: 22,
                color: '#66FFE0',
                filter: 'drop-shadow(0 2px 4px rgba(102,255,224,0.35))',
                animation: 'spinSlow 12s linear infinite',
                '@keyframes spinSlow': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' }
                }
              }}
              className="gear-rot gear-main"
            />
            <SettingsIcon
              sx={{
                position: 'absolute',
                left: 12,
                top: 10,
                fontSize: 16,
                // HSL-shaded variant of primary (#66FFE0 -> hsl(168,100%,70%)). Darker shade for contrast.
                color: 'hsl(168, 100%, 55%)',
                opacity: 0.9,
                animation: 'spinFast 6s linear infinite',
                '@keyframes spinFast': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(-360deg)' }
                }
              }}
              className="gear-rot gear-inner"
            />
          </Box>
          </motion.div>
          <Typography 
            variant="h6" 
            component="div" 
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #4FC3F7 0%, #29B6F6 50%, #0277BD 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              color: 'transparent',
              letterSpacing: '1px',
              fontFamily: '"Orbitron", "Inter", sans-serif'
            }}
          >
            PRISM ANALYTICS
          </Typography>
        </Box>
        <IconButton 
          onClick={handleDrawerClose}
          sx={{
            color: isDarkMode ? '#f1f5f9' : '#0f172a',
            '&:hover': {
              backgroundColor: isDarkMode 
                ? 'rgba(99, 102, 241, 0.1)' 
                : 'rgba(79, 70, 229, 0.1)',
            }
          }}
        >
          <CloseIcon />
        </IconButton>
      </Box>
      <Divider />
      <List>
        {navItems.map((item) => (
          <ListItem 
            key={item.text} 
            component={Link} 
            to={item.path}
            sx={{
              color: isDarkMode ? '#ccd6f6' : '#1e293b',
              textDecoration: 'none',
              '&:hover': {
                backgroundColor: isDarkMode 
                  ? 'rgba(100, 255, 218, 0.1)' 
                  : 'rgba(0, 102, 204, 0.1)',
              },
            }}
          >
            <ListItemIcon 
              sx={{ 
                color: isDarkMode ? '#5fffe0' : '#4fe6c7',
                minWidth: 40 
              }}
            >
              {item.icon}
            </ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar 
        position="fixed" 
        elevation={0}
        sx={{
          zIndex: theme.zIndex.drawer + 1,
          backdropFilter: 'blur(10px)',
          backgroundColor: isDarkMode 
            ? 'rgba(10, 25, 47, 0.85)' 
            : 'rgba(255, 255, 255, 0.85)',
          borderBottom: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between', minHeight: '64px !important' }}>
          {/* Enhanced Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {/* Dual stacked gears (desktop) */}
                <motion.div
                  animate={desktopGearControls}
                  initial={false}
                  onHoverStart={() => {
                    desktopGearControls.start({ scale: 1.12, transition: { type: 'spring', stiffness: 330, damping: 19 } });
                  }}
                  onHoverEnd={() => {
                    desktopGearControls.start({
                      scale: [1.12, 1.04, 0.985, 1.01, 1],
                      transition: { duration: 0.6, ease: 'easeOut' }
                    });
                  }}
                >
                <Box 
                  sx={{ 
                    position: 'relative', 
                    width: 42, 
                    height: 34,
                    '&:hover .gear-rot': { animationPlayState: 'paused' }
                  }}
                >
                  <SettingsIcon
                    sx={{
                      position: 'absolute',
                      left: 0,
                      top: 4,
                      fontSize: 30,
                      color: '#66FFE0',
                      filter: 'drop-shadow(0 3px 6px rgba(102,255,224,0.35))',
                      animation: 'spinSlow 14s linear infinite',
                      '@keyframes spinSlow': {
                        '0%': { transform: 'rotate(0deg)' },
                        '100%': { transform: 'rotate(360deg)' }
                      }
                    }}
                    className="gear-rot gear-main"
                  />
                  <SettingsIcon
                    sx={{
                      position: 'absolute',
                      left: 16,
                      top: 14,
                      fontSize: 18,
                      // HSL shaded variant for inner gear
                      color: 'hsl(168, 100%, 52%)',
                      opacity: 0.95,
                      animation: 'spinFast 6.5s linear infinite',
                      '@keyframes spinFast': {
                        '0%': { transform: 'rotate(0deg)' },
                        '100%': { transform: 'rotate(-360deg)' }
                      }
                    }}
                    className="gear-rot gear-inner"
                  />
                </Box>
                </motion.div>
                <Typography 
                  variant="h6" 
                  component="span"
                  className="logo-text"
                  sx={{ 
                    fontWeight: 700,
                    background: 'linear-gradient(135deg, #4FC3F7 0%, #29B6F6 50%, #0277BD 100%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    color: 'transparent',
                    letterSpacing: '1px',
                    fontSize: '1.35rem',
                    fontFamily: '"Orbitron", "Inter", sans-serif',
                    textShadow: 'none'
                  }}
                >
                  PRISM ANALYTICS
                </Typography>
              </Box>
            </Link>
          </motion.div>

          {/* Desktop Navigation */}
          {!isMobile && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
              {/* Navigation Links */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Button
                  component={Link}
                  to="/"
                  sx={{ 
                    color: location.pathname === '/' 
                      ? (isDarkMode ? '#5fffe0' : '#4fe6c7')
                      : (isDarkMode ? '#f1f5f9' : '#0f172a'), 
                    textTransform: 'none',
                    fontWeight: location.pathname === '/' ? 600 : 500,
                    '&:hover': { 
                      backgroundColor: isDarkMode 
                        ? 'rgba(95, 255, 224, 0.1)' 
                        : 'rgba(79, 230, 199, 0.1)'
                    }
                  }}
                >
                  Home
                </Button>
                <Button
                  component={Link}
                  to="/about"
                  sx={{ 
                    color: location.pathname === '/about' 
                      ? (isDarkMode ? '#5fffe0' : '#4fe6c7')
                      : (isDarkMode ? '#f1f5f9' : '#0f172a'), 
                    textTransform: 'none',
                    fontWeight: location.pathname === '/about' ? 600 : 500,
                    '&:hover': { 
                      backgroundColor: isDarkMode 
                        ? 'rgba(99, 102, 241, 0.1)' 
                        : 'rgba(79, 70, 229, 0.1)'
                    }
                  }}
                >
                  About
                </Button>
              </Box>
            </Box>
          )}

          {/* Mobile Menu Button */}
          {isMobile && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              {/* Mobile Menu */}
              <IconButton
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ 
                  ml: 1,
                  color: isDarkMode ? '#ccd6f6' : '#1e293b',
                  '&:hover': {
                    backgroundColor: isDarkMode 
                      ? 'rgba(100, 255, 218, 0.1)' 
                      : 'rgba(0, 102, 204, 0.1)',
                  }
                }}
              >
                <MenuIcon />
              </IconButton>
            </Box>
          )}
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      <Drawer
        variant="temporary"
        anchor="right"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: 'block', md: 'none' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: 250,
            backgroundColor: isDarkMode ? '#112240' : '#f8fafc',
            borderLeft: `1px solid ${isDarkMode ? '#233554' : '#e2e8f0'}`,
            color: isDarkMode ? '#ccd6f6' : '#1e293b',
            top: '64px'
          },
        }}
      >
        {drawer}
      </Drawer>

      {/* Toolbar spacer */}
      <Toolbar />
    </>
  );
};

export default Header;