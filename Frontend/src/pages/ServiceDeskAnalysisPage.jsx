import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Box,
  Container,
  Typography,
  Paper,
  Button,
  LinearProgress,
  Chip,
  Card,
  Alert,
  Fade,
  Backdrop,
  CircularProgress
} from '@mui/material';
import {
  CloudUpload,
  Analytics,
  Description,
  CheckCircle,
  Info,
  Speed,
  TrendingUp,
  AccessTime,
  SupportAgent,
  Refresh
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import toastLib from '../utils/toast';
import ParticlesBackground from '../components/ParticlesBackground';

// Styled Components
const StyledPaper = styled(Paper)(({ theme }) => ({
  background: 'linear-gradient(135deg, rgba(0, 255, 220, 0.04) 0%, rgba(0, 230, 143, 0.02) 100%)',
  backdropFilter: 'blur(14px)',
  border: '1.5px solid rgba(0, 255, 220, 0.12)',
  borderRadius: '16px',
  padding: theme.spacing(4),
  boxShadow: '0 8px 32px rgba(0, 255, 220, 0.08)',
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 12px 28px rgba(0, 0, 0, 0.12)',
    borderColor: 'rgba(100, 255, 218, 0.2)',
  }
}));

const UploadArea = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'isDragOver' && prop !== 'hasFile',
})(({ theme, isDragOver, hasFile }) => ({
  border: `2px dashed ${hasFile ? '#00e68f' : isDragOver ? '#00ffdc' : 'rgba(255, 255, 255, 0.2)'}`,
  borderRadius: '12px',
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  background: hasFile 
    ? 'linear-gradient(135deg, rgba(0, 230, 143, 0.12) 0%, rgba(0, 230, 143, 0.06) 100%)'
    : isDragOver 
    ? 'linear-gradient(135deg, rgba(0, 255, 220, 0.12) 0%, rgba(0, 255, 220, 0.06) 100%)'
    : 'linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.01) 100%)',
  '&:hover': {
    borderColor: '#00ffdc',
    background: 'linear-gradient(135deg, rgba(0, 255, 220, 0.1) 0%, rgba(0, 255, 220, 0.05) 100%)',
  }
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%)',
  backdropFilter: 'blur(10px)',
  border: '1.5px solid rgba(0, 255, 220, 0.1)',
  borderRadius: '12px',
  height: '100%',
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'translateY(-6px)',
    borderColor: 'rgba(0, 255, 220, 0.4)',
    background: 'linear-gradient(135deg, rgba(0, 255, 220, 0.05) 0%, rgba(0, 230, 143, 0.02) 100%)',
  }
}));

const GradientButton = styled(Button)(({ theme }) => ({
  background: 'linear-gradient(135deg, #00ffdc 0%, #00e68f 100%)',
  color: '#000',
  fontWeight: 700,
  padding: '12px 32px',
  borderRadius: '8px',
  textTransform: 'none',
  fontSize: '1rem',
  boxShadow: '0 4px 16px rgba(0, 255, 220, 0.4)',
  transition: 'all 0.3s ease',
  '&:hover': {
    background: 'linear-gradient(135deg, #00e6d1 0%, #00d97e 100%)',
    transform: 'translateY(-2px)',
    boxShadow: '0 8px 24px rgba(0, 255, 220, 0.5), 0 0 12px rgba(0, 230, 143, 0.3)',
  },
  '&:disabled': {
    background: 'rgba(255, 255, 255, 0.1)',
    color: 'rgba(255, 255, 255, 0.5)',
    transform: 'none',
    boxShadow: 'none',
  }
}));

const ServiceDeskAnalysisPage = () => {
  const [formData, setFormData] = useState({
    servicedesk_file: null
  });
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [analysisResults, setAnalysisResults] = useState(null);
  const fileInputRef = useRef(null);

  const features = [
    {
      icon: <AccessTime sx={{ fontSize: 40, color: '#00ffdc' }} />,
      title: 'Resolution Time Tracking',
      description: 'Monitor and analyze ticket resolution times to identify bottlenecks'
    },
    {
      icon: <TrendingUp sx={{ fontSize: 40, color: '#00e68f' }} />,
      title: 'Trend Analysis',
      description: 'Identify patterns and trends in service desk operations'
    },
    {
      icon: <SupportAgent sx={{ fontSize: 40, color: '#5f7fff' }} />,
      title: 'User Experience Insights',
      description: 'Understand customer satisfaction and pain points'
    },
    {
      icon: <Speed sx={{ fontSize: 40, color: '#ffa800' }} />,
      title: 'Team Performance',
      description: 'Evaluate team efficiency and workload distribution'
    }
  ];

  // Handle file selection
  const handleFileSelect = (file) => {
    if (file && (file.name.toLowerCase().endsWith('.xlsx') || file.name.toLowerCase().endsWith('.csv'))) {
      setFormData(prev => ({ ...prev, servicedesk_file: file }));
      setFileName(file.name);
      toastLib.success(`File selected: ${file.name}`);
    } else {
      toastLib.error('Please upload a .xlsx or .csv file.');
      setFileName('');
    }
  };

  // Handle file input change
  const handleInputChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.servicedesk_file) {
      toastLib.error('Please select a file to upload.');
      return;
    }

    setLoading(true);
    setUploadProgress(0);

    try {
      const formDataObj = new FormData();
      formDataObj.append('servicedesk_file', formData.servicedesk_file);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.random() * 10;
        });
      }, 200);

      const response = await fetch('/api/servicedeskanalysis', {
        method: 'POST',
        body: formDataObj
      });

      const result = await response.json();
      clearInterval(progressInterval);
      setUploadProgress(100);

      if (response.ok) {
        setAnalysisResults(result);
        toastLib.success(result.message || 'Analysis completed successfully!');
      } else {
        toastLib.error(result.error || 'Failed to analyze file.');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      toastLib.error('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
      setTimeout(() => setUploadProgress(0), 2000);
    }
  };

  const pageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: (index) => ({
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        delay: index * 0.1,
        ease: "easeOut"
      }
    })
  };

  return (
    <>
      <ParticlesBackground />
      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress color="primary" size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Analyzing your service desk data...
          </Typography>
          {uploadProgress > 0 && (
            <Box sx={{ width: 300, mt: 2 }}>
              <LinearProgress 
                variant="determinate" 
                value={uploadProgress} 
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: '#00ffdc',
                  }
                }}
              />
              <Typography variant="body2" sx={{ mt: 1 }}>
                {Math.round(uploadProgress)}% Complete
              </Typography>
            </Box>
          )}
        </Box>
      </Backdrop>

      <Container maxWidth="lg" sx={{ py: 8, position: 'relative', zIndex: 2 }}>
        <motion.div
          variants={pageVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Header Section */}
          <Box sx={{ textAlign: 'center', mb: 6 }}>
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Typography
                variant="h2"
                component="h1"
                sx={{
                  fontWeight: 700,
                  background: 'linear-gradient(135deg, #00ffdc 0%, #00e68f 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  color: 'transparent',
                  mb: 2
                }}
              >
                Service Desk Ticket Analysis
              </Typography>
              <Typography
                variant="h6"
                sx={{ color: 'rgba(255, 255, 255, 0.7)', maxWidth: 700, mx: 'auto' }}
              >
                Upload your service desk ticket data to gain insightful analysis for tracking resolution trends, improving response times, and enhancing user experience through actionable insights.
              </Typography>
            </motion.div>
          </Box>

         
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <StyledPaper>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <SupportAgent sx={{ fontSize: 28, color: '#00ffdc', mr: 2 }} />
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  Service Desk Analysis
                </Typography>
              </Box>

              <form onSubmit={handleSubmit}>
                <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 3, mb: 3 }}>
                  {/* Left: Upload Area - Compact */}
                  <Box>
                    <UploadArea
                      isDragOver={isDragOver}
                      hasFile={!!fileName}
                      onDragOver={handleDragOver}
                      onDragLeave={handleDragLeave}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      sx={{ p: 3, minHeight: '200px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept=".xlsx,.csv"
                        onChange={handleInputChange}
                        style={{ display: 'none' }}
                      />
                      
                      {fileName ? (
                        <Fade in={true}>
                          <Box sx={{ textAlign: 'center', width: '100%' }}>
                            <CheckCircle sx={{ fontSize: 36, color: '#00e68f', mb: 1 }} />
                            <Typography variant="body1" sx={{ mb: 1, fontWeight: 600 }}>
                              File Selected
                            </Typography>
                            <Chip
                              icon={<Description />}
                              label={fileName}
                              color="success"
                              variant="outlined"
                              size="small"
                              sx={{ mb: 1 }}
                            />
                            <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block' }}>
                              Click to change
                            </Typography>
                          </Box>
                        </Fade>
                      ) : (
                        <Box sx={{ textAlign: 'center', width: '100%' }}>
                          <CloudUpload sx={{ fontSize: 36, color: '#00ffdc', mb: 1 }} />
                          <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                            Drop your file here
                          </Typography>
                          <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)', display: 'block', mb: 1 }}>
                            or click to browse
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center', flexWrap: 'wrap' }}>
                            <Chip label="Excel" size="small" variant="outlined" sx={{ height: 24 }} />
                            <Chip label="CSV" size="small" variant="outlined" sx={{ height: 24 }} />
                          </Box>
                        </Box>
                      )}
                    </UploadArea>
                  </Box>

                  {/* Right: Analysis Info & Guidelines */}
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <Box sx={{ 
                      background: 'linear-gradient(135deg, rgba(0, 255, 220, 0.1) 0%, rgba(0, 230, 143, 0.06) 100%)',
                      border: '1.5px solid rgba(0, 255, 220, 0.25)',
                      borderRadius: '8px',
                      p: 2
                    }}>
                      <Box sx={{ display: 'flex', gap: 1, mb: 1, alignItems: 'center' }}>
                        <Info sx={{ fontSize: 20, color: '#00ffdc' }} />
                        <Typography sx={{ fontWeight: 600, color: '#fff', fontSize: '0.95rem' }}>
                          Analysis Capabilities
                        </Typography>
                      </Box>
                      <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.7)', lineHeight: 1.6 }}>
                        ✓ Resolution time tracking<br/>
                        ✓ Trend analysis and patterns<br/>
                        ✓ User experience insights<br/>
                        ✓ Team performance metrics
                      </Typography>
                    </Box>

                    <Box sx={{ 
                      background: 'linear-gradient(135deg, rgba(95, 127, 255, 0.1) 0%, rgba(95, 127, 255, 0.06) 100%)',
                      border: '1.5px solid rgba(95, 127, 255, 0.25)',
                      borderRadius: '8px',
                      p: 2
                    }}>
                      <Typography sx={{ fontWeight: 600, color: '#fff', fontSize: '0.9rem', mb: 1 }}>
                        📊 Supported Formats
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.7)', lineHeight: 1.6 }}>
                        <strong>.XLSX</strong> - Excel spreadsheets<br/>
                        <strong>.CSV</strong> - Comma-separated values<br/>
                        <strong>File Size:</strong> No limit
                      </Typography>
                    </Box>

                    {fileName && (
                      <Box sx={{ 
                        background: 'linear-gradient(135deg, rgba(0, 230, 143, 0.12) 0%, rgba(0, 230, 143, 0.06) 100%)',
                        border: '1.5px solid rgba(0, 230, 143, 0.35)',
                        borderRadius: '8px',
                        p: 2
                      }}>
                        <Typography sx={{ fontWeight: 600, color: '#00e68f', fontSize: '0.9rem', mb: 0.5 }}>
                          ✓ Ready to Analyze
                        </Typography>
                        <Typography variant="caption" sx={{ color: 'rgba(0, 230, 143, 0.95)' }}>
                          Click the button below to start analysis
                        </Typography>
                      </Box>
                    )}
                  </Box>
                </Box>

                <Box sx={{ textAlign: 'center', mt: 3 }}>
                  <GradientButton
                    type="submit"
                    size="large"
                    disabled={!fileName || loading}
                    startIcon={loading ? <CircularProgress size={20} /> : <Analytics />}
                  >
                    {loading ? 'Analyzing...' : 'Start Analysis'}
                  </GradientButton>
                </Box>
              </form>
            </StyledPaper>
          </motion.div>

          {/* Results Section */}
          {analysisResults && (
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <StyledPaper sx={{ mt: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <Box sx={{
                    background: 'linear-gradient(135deg, #66FFE0 0%, #10b981 100%)',
                    borderRadius: '8px',
                    p: 1.25,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                  }}>
                    <SupportAgent sx={{ fontSize: 22, color: '#0f172a' }} />
                  </Box>
                  <Typography variant="h6" sx={{ fontWeight: 700, color: '#fff' }}>
                    Analysis Result
                  </Typography>
                </Box>

                <Box sx={{ textAlign: 'center', py: 4 }}>
                  {analysisResults.error ? (
                    <Box>
                      <Typography sx={{ color: '#ff6b6b', fontWeight: 700, fontSize: '1rem' }}>Analysis Failed</Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1 }}> {analysisResults.error || 'An error occurred during analysis.'} </Typography>
                    </Box>
                  ) : (
                    <Box>
                      <Typography sx={{ color: '#10b981', fontWeight: 700, fontSize: '1rem' }}>Analysis completed successfully</Typography>
                      {analysisResults.message && (
                        <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1 }}>{analysisResults.message}</Typography>
                      )}
                    </Box>
                  )}
                </Box>

              </StyledPaper>
            </motion.div>
          )}
        </motion.div>
      </Container>
    </>
  );
};

export default ServiceDeskAnalysisPage;
