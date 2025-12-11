import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Typography, Button, Container } from '@mui/material';
import { Home, ArrowBack } from '@mui/icons-material';

const PageNotFound = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '80vh',
          textAlign: 'center',
          gap: 3,
        }}
      >
        {/* 404 Large Text */}
        <Typography
          variant="h1"
          sx={{
            fontSize: { xs: '6rem', md: '8rem' },
            fontWeight: 'bold',
            background: 'linear-gradient(45deg, #66FFE0 30%, #6366f1 90%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            lineHeight: 1,
          }}
        >
          404
        </Typography>

        {/* Error Message */}
        <Box sx={{ mb: 2 }}>
          <Typography
            variant="h4"
            sx={{
              fontWeight: 600,
              mb: 2,
              color: 'text.primary',
            }}
          >
            Page Not Found
          </Typography>
          <Typography
            variant="h6"
            sx={{
              color: 'text.secondary',
              maxWidth: '500px',
              lineHeight: 1.6,
            }}
          >
            Oops! The page you're looking for doesn't exist. It might have been moved, deleted, or you entered the wrong URL.
          </Typography>
        </Box>

        {/* Action Buttons */}
        <Box
          sx={{
            display: 'flex',
            gap: 2,
            flexDirection: { xs: 'column', sm: 'row' },
            alignItems: 'center',
          }}
        >
          <Button
            component={Link}
            to="/"
            variant="contained"
            size="large"
            startIcon={<Home />}
            sx={{
              background: 'linear-gradient(45deg, #66FFE0 30%, #6366f1 90%)',
              color: 'black',
              fontWeight: 600,
              px: 4,
              py: 1.5,
              '&:hover': {
                background: 'linear-gradient(45deg, #4DCCAA 30%, #4F46E5 90%)',
                transform: 'translateY(-2px)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            Go to Home
          </Button>
          
          <Button
            onClick={() => window.history.back()}
            variant="outlined"
            size="large"
            startIcon={<ArrowBack />}
            sx={{
              borderColor: '#66FFE0',
              color: '#66FFE0',
              px: 4,
              py: 1.5,
              '&:hover': {
                borderColor: '#4DCCAA',
                color: '#4DCCAA',
                backgroundColor: 'rgba(102, 255, 224, 0.1)',
              },
            }}
          >
            Go Back
          </Button>
        </Box>

        {/* Decorative Elements */}
        <Box
          sx={{
            position: 'absolute',
            top: '20%',
            left: '10%',
            width: '100px',
            height: '100px',
            borderRadius: '50%',
            background: 'linear-gradient(45deg, #66FFE0 30%, #6366f1 90%)',
            opacity: 0.1,
            animation: 'float 6s ease-in-out infinite',
            '@keyframes float': {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-20px)' },
            },
          }}
        />
        
        <Box
          sx={{
            position: 'absolute',
            top: '60%',
            right: '15%',
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            background: 'linear-gradient(45deg, #6366f1 30%, #66FFE0 90%)',
            opacity: 0.1,
            animation: 'float 4s ease-in-out infinite reverse',
          }}
        />
      </Box>
    </Container>
  );
};

export default PageNotFound;
