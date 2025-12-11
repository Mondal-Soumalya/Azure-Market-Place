import React from 'react';
import { Box, Typography, Button, Container } from '@mui/material';
import { Error as ErrorIcon, Refresh as RefreshIcon } from '@mui/icons-material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Error caught by boundary:', error, errorInfo);
    }
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container maxWidth="md" sx={{ py: 8 }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              minHeight: '60vh',
              textAlign: 'center',
              p: 4,
              borderRadius: 2,
              background: 'rgba(255, 255, 255, 0.05)',
              backdropFilter: 'blur(10px)',
              border: '1px solid',
              borderColor: 'divider'
            }}
          >
            <ErrorIcon 
              sx={{ 
                fontSize: 64, 
                color: 'error.main', 
                mb: 2,
                opacity: 0.8
              }} 
            />
            
            <Typography 
              variant="h4" 
              sx={{ 
                mb: 2, 
                fontWeight: 600,
                color: 'text.primary'
              }}
            >
              Oops! Something went wrong
            </Typography>
            
            <Typography 
              variant="body1" 
              sx={{ 
                mb: 4, 
                color: 'text.secondary',
                maxWidth: 500,
                lineHeight: 1.6
              }}
            >
              We encountered an unexpected error. Please try refreshing the page or contact support if the problem persists.
            </Typography>

            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', justifyContent: 'center' }}>
              <Button
                variant="contained"
                startIcon={<RefreshIcon />}
                onClick={this.handleReset}
                sx={{
                  background: 'linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5fffe0 0%, #6366f1 2%, #5fffe0 100%)',
                  }
                }}
              >
                Refresh Page
              </Button>
              
              <Button
                variant="outlined"
                onClick={() => window.history.back()}
                sx={{
                  borderColor: 'divider',
                  color: 'text.secondary',
                  '&:hover': {
                    borderColor: 'primary.main',
                    color: 'primary.main',
                  }
                }}
              >
                Go Back
              </Button>
            </Box>

            {process.env.NODE_ENV === 'development' && this.state.error && (
              <Box sx={{ mt: 4, p: 2, background: 'rgba(0, 0, 0, 0.1)', borderRadius: 1, maxWidth: '100%', overflow: 'auto' }}>
                <Typography variant="caption" sx={{ color: 'text.secondary', fontFamily: 'monospace' }}>
                  <strong>Error:</strong> {this.state.error.toString()}
                </Typography>
              </Box>
            )}
          </Box>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;