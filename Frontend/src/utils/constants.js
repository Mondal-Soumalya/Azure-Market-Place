// Application Constants
export const APP_NAME = 'C.R.E.A.T.E';
export const APP_DESCRIPTION = 'Comprehensive Robotic Enterprise Automation Technology Engine';

// Routes
export const ROUTES = {
  HOME: '/',
  FEATURES: '/features',
  ABOUT_US: '/aboutus',
  NEW_REQUEST: '/newrequest',
  ANALYSIS_ENGINE: '/analysisenginepage',
  SERVICE_ANALYSIS: '/servicedeskanalysis',
  INCIDENT_ANALYSIS: '/incidentanalysis',
  CHATBOT: '/chatbot'
};

// Form Pages (for body class handling)
export const FORM_PAGES = [
  ROUTES.NEW_REQUEST
];

// API Base URL - Flask backend
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

// API Endpoints
export const API_ENDPOINTS = {
  // Forms
  NEW_REQUEST: '/api/newrequest',
  
  // Analysis
  INCIDENT_ANALYSIS: '/incidentanalysis',
  SERVICE_ANALYSIS: '/servicedeskanalysis',
  
  // Chat
  CHATBOT: '/api/chatbot',
  
  // Logs
  APPLICATIONS_LOG: '/api/applicationslog'
};

// File Types
export const FILE_TYPES = {
  EXCEL: '.xlsx,.xls',
  CSV: '.csv',
  DOCUMENT: '.doc,.docx',
  ALL_DOCUMENTS: '.doc,.docx,.pdf,.txt'
};

// Validation Patterns
export const VALIDATION_PATTERNS = {
  CAPGEMINI_EMAIL: /^[a-zA-Z0-9._%+-]+@capgemini\.com$/,
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  EMPLOYEE_ID: /^\d{8}$/
};

// Animation Durations
export const ANIMATION_DURATIONS = {
  FAST: 0.2,
  NORMAL: 0.3,
  SLOW: 0.5,
  VERY_SLOW: 0.8
};

// Toast Configuration
export const TOAST_CONFIG = {
  DURATION: 4000,
  POSITION: 'top-right'
};

// Theme Colors (legacy static palette deprecated - retained for fallback)
export const THEME_COLORS = {
  PRIMARY: '#5fffe0', // 97% cyan-green primary
  SECONDARY: '#8b5cf6', // was #8892b0 (mapped to secondary accent)
  BACKGROUND: '#1e2a3a', // updated to navy blue bg
  SURFACE: '#181832',
  BORDER: '#334155',
  ERROR: '#D14B55',
  SUCCESS: '#2FAF72', // was #64ffda
  WARNING: '#D88A1A'
};

// Loading States
export const LOADING_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  SUCCESS: 'success',
  ERROR: 'error'
};

// Log Levels
export const LOG_LEVELS = {
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info',
  DEBUG: 'debug'
};

// Chat Message Types
export const MESSAGE_TYPES = {
  USER: 'user',
  BOT: 'bot',
  SYSTEM: 'system'
};