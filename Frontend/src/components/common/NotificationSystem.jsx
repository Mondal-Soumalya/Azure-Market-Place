import React from 'react';
import { toast } from 'react-hot-toast';
import { 
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  Close as CloseIcon
} from '@mui/icons-material';

// Transparent toast styles with clean design
const toastStyles = {
  style: {
    background: 'rgba(255, 255, 255, 0.5)',
    color: '#374151',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    padding: '16px',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    border: '1px solid rgba(229, 231, 235, 0.6)',
    backdropFilter: 'blur(16px)',
    maxWidth: '400px',
    minWidth: '320px',
  },
  success: {
    iconTheme: {
      primary: '#ffffff',
      secondary: '#10b981',
    },
    style: {
      background: 'rgba(255, 255, 255, 0.5)',
      color: '#374151',
      borderLeft: '4px solid #10b981',
      border: '1px solid rgba(229, 231, 235, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      backdropFilter: 'blur(16px)',
    },
  },
  error: {
    iconTheme: {
      primary: '#ffffff',
      secondary: '#ef4444',
    },
    style: {
      background: 'rgba(255, 255, 255, 0.5)',
      color: '#374151',
      borderLeft: '4px solid #ef4444',
      border: '1px solid rgba(229, 231, 235, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      backdropFilter: 'blur(16px)',
    },
  },
  warning: {
    iconTheme: {
      primary: '#ffffff',
      secondary: '#f59e0b',
    },
    style: {
      background: 'rgba(255, 255, 255, 0.5)',
      color: '#374151',
      borderLeft: '4px solid #f59e0b',
      border: '1px solid rgba(229, 231, 235, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      backdropFilter: 'blur(16px)',
    },
  },
  info: {
    iconTheme: {
      primary: '#ffffff',
      secondary: '#3b82f6',
    },
    style: {
      background: 'rgba(255, 255, 255, 0.5)',
      color: '#374151',
      borderLeft: '4px solid #3b82f6',
      border: '1px solid rgba(229, 231, 235, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      backdropFilter: 'blur(16px)',
    },
  },
};

// Dark mode styles with transparent dark backgrounds
const darkToastStyles = {
  style: {
    background: 'rgba(31, 41, 55, 0.5)',
    color: '#f9fafb',
    borderRadius: '12px',
    fontSize: '0.875rem',
    fontWeight: '500',
    padding: '14px 18px',
    border: '1px solid rgba(55, 65, 81, 0.6)',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
    backdropFilter: 'blur(16px)',
    maxWidth: '400px',
    minWidth: '300px',
  },
  success: {
    iconTheme: {
      primary: '#22c55e',
      secondary: 'rgba(31, 41, 55, 0.9)',
    },
    style: {
      background: 'rgba(31, 41, 55, 0.5)',
      color: '#f9fafb',
      borderLeft: '4px solid #22c55e',
      border: '1px solid rgba(55, 65, 81, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      backdropFilter: 'blur(16px)',
    },
  },
  error: {
    iconTheme: {
      primary: '#ef4444',
      secondary: 'rgba(31, 41, 55, 0.5)',
    },
    style: {
      background: 'rgba(31, 41, 55, 0.5)',
      color: '#f9fafb',
      borderLeft: '4px solid #ef4444',
      border: '1px solid rgba(55, 65, 81, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      backdropFilter: 'blur(16px)',
    },
  },
  warning: {
    iconTheme: {
      primary: '#f59e0b',
      secondary: 'rgba(31, 41, 55, 0.5)',
    },
    style: {
      background: 'rgba(31, 41, 55, 0.5)',
      color: '#f9fafb',
      borderLeft: '4px solid #f59e0b',
      border: '1px solid rgba(55, 65, 81, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      backdropFilter: 'blur(16px)',
    },
  },
  info: {
    iconTheme: {
      primary: '#3b82f6',
      secondary: 'rgba(31, 41, 55, 0.5)',
    },
    style: {
      background: 'rgba(31, 41, 55, 0.5)',
      color: '#f9fafb',
      borderLeft: '4px solid #3b82f6',
      border: '1px solid rgba(55, 65, 81, 0.6)',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)',
      backdropFilter: 'blur(16px)',
    },
  },
};

// Get current theme styles
const getToastStyles = (isDarkMode = false) => {
  return isDarkMode ? darkToastStyles : toastStyles;
};

// Ultra-simple duplicate prevention using global flags
let isShowingError = false;
let isShowingSuccess = false;
let isShowingWarning = false;
let isShowingInfo = false;
let isShowingLoading = false;

// Reset flags after delay
const resetFlag = (flagName, delay = 2000) => {
  setTimeout(() => {
    switch(flagName) {
      case 'error': isShowingError = false; break;
      case 'success': isShowingSuccess = false; break;
      case 'warning': isShowingWarning = false; break;
      case 'info': isShowingInfo = false; break;
      case 'loading': isShowingLoading = false; break;
    }
  }, delay);
};

// Notification functions with duplicate prevention
export const showSuccess = (message, isDarkMode = false, toastId = null) => {
  // Block duplicates with simple flag
  if (isShowingSuccess) return null;
  
  isShowingSuccess = true;
  resetFlag('success', 4000); // Reset after toast duration
  
  const styles = getToastStyles(isDarkMode);
  return toast.success(message, {
    toastId: toastId,
    duration: 4000,
    position: 'top-center',
    ...styles.success,
  });
};

export const showError = (message, isDarkMode = false, toastId = null) => {
  // Block duplicates with simple flag
  if (isShowingError) return null;
  
  isShowingError = true;
  resetFlag('error', 5000); // Reset after toast duration
  
  const styles = getToastStyles(isDarkMode);
  return toast.error(message, {
    toastId: toastId,
    duration: 5000,
    position: 'top-center',
    ...styles.error,
  });
};

export const showWarning = (message, isDarkMode = false, toastId = null) => {
  // Block duplicates with simple flag
  if (isShowingWarning) return null;
  
  isShowingWarning = true;
  resetFlag('warning', 4000); // Reset after toast duration
  
  const styles = getToastStyles(isDarkMode);
  return toast(message, {
    toastId: toastId,
    duration: 4000,
    position: 'top-center',
    icon: <WarningIcon />,
    ...styles.warning,
  });
};

export const showInfo = (message, isDarkMode = false, toastId = null) => {
  // Block duplicates with simple flag
  if (isShowingInfo) return null;
  
  isShowingInfo = true;
  resetFlag('info', 4000); // Reset after toast duration
  
  const styles = getToastStyles(isDarkMode);
  return toast(message, {
    toastId: toastId,
    duration: 4000,
    position: 'top-center',
    icon: <InfoIcon />,
    ...styles.info,
  });
};

export const showLoading = (message, isDarkMode = false, toastId = null) => {
  // Block duplicates with simple flag
  if (isShowingLoading) return null;
  
  isShowingLoading = true;
  resetFlag('loading', 10000); // Reset after longer duration for loading
  
  const styles = getToastStyles(isDarkMode);
  return toast.loading(message, {
    toastId: toastId,
    position: 'top-center',
    style: {
      ...styles.style,
      background: isDarkMode ? 'rgba(31, 41, 55, 0.5)' : 'rgba(255, 255, 255, 0.5)',
      color: isDarkMode ? '#f9fafb' : '#374151',
      border: isDarkMode ? '1px solid rgba(55, 65, 81, 0.6)' : '1px solid rgba(229, 231, 235, 0.6)',
      backdropFilter: 'blur(16px)',
    },
  });
};

export const dismissToast = (toastId) => {
  toast.dismiss(toastId);
};

// Custom toast component for complex notifications with transparent background
export const showCustomToast = (content, options = {}) => {
  return toast.custom(
    (t) => (
      <div
        style={{
          background: options.background || 'rgba(255, 255, 255, 0.1)',
          color: options.color || '#1e293b',
          padding: '14px 18px',
          borderRadius: '12px',
          fontSize: '0.875rem',
          boxShadow: '0 8px 25px rgba(0, 0, 0, 0.1), 0 4px 10px rgba(0, 0, 0, 0.05)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          backdropFilter: 'blur(16px)',
          maxWidth: '400px',
          minWidth: '300px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
          {content.icon && <span>{content.icon}</span>}
          <span>{content.message}</span>
        </div>
        <button
          onClick={() => toast.dismiss(t.id)}
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '4px',
            borderRadius: '4px',
            color: 'inherit',
            opacity: 0.7,
            transition: 'opacity 0.2s',
          }}
          onMouseEnter={(e) => (e.target.style.opacity = '1')}
          onMouseLeave={(e) => (e.target.style.opacity = '0.7')}
        >
          <CloseIcon sx={{ fontSize: 16 }} />
        </button>
      </div>
    ),
    {
      duration: options.duration || 4000,
      position: options.position || 'top-right',
    }
  );
};

// Common notification helpers with predefined IDs
export const notifyFormError = (message = "Please correct highlighted fields", isDarkMode = false) => {
  return showError(message, isDarkMode, "form-error");
};

export const notifyLoginError = (message = "Invalid credentials", isDarkMode = false) => {
  return showError(message, isDarkMode, "login-error");
};

export const notifyNetworkError = (message = "Network connection failed", isDarkMode = false) => {
  return showError(message, isDarkMode, "network-error");
};

export const notifySuccess = (message = "Operation completed successfully", isDarkMode = false) => {
  return showSuccess(message, isDarkMode, "general-success");
};

export const notifyLoading = (message = "Processing...", isDarkMode = false) => {
  return showLoading(message, isDarkMode, "general-loading");
};

// Check if a specific toast type is currently being shown
export const isToastActive = (type) => {
  switch(type) {
    case 'error': return isShowingError;
    case 'success': return isShowingSuccess;
    case 'warning': return isShowingWarning;
    case 'info': return isShowingInfo;
    case 'loading': return isShowingLoading;
    default: return false;
  }
};

// Dismiss specific toast by ID
export const dismissSpecificToast = (toastId) => {
  toast.dismiss(toastId);
};

// Force reset flags (useful for debugging)
export const resetAllFlags = () => {
  isShowingError = false;
  isShowingSuccess = false;
  isShowingWarning = false;
  isShowingInfo = false;
  isShowingLoading = false;
};

// Dismiss all toasts and reset flags
export const dismissAllToasts = () => {
  resetAllFlags();
  toast.dismiss();
};

// Export default for convenience
const NotificationSystem = {
  success: showSuccess,
  error: showError,
  warning: showWarning,
  info: showInfo,
  loading: showLoading,
  dismiss: dismissAllToasts,
  custom: showCustomToast,
  // Helper functions
  formError: notifyFormError,
  loginError: notifyLoginError,
  networkError: notifyNetworkError,
  generalSuccess: notifySuccess,
  generalLoading: notifyLoading,
  isActive: isToastActive,
  dismissSpecific: dismissSpecificToast,
  dismissByMessage: dismissToastByMessage,
  dismissAll: dismissAllToasts,
};

export default NotificationSystem; 