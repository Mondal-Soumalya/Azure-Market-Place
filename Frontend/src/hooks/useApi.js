import { useState, useCallback } from 'react';
import toastLib from '../utils/toast';

export const useApi = () => {
  const [loading, setLoading] = useState(false);

  const apiCall = useCallback(async ({
    url,
    method = 'GET',
    data = null,
    headers = {},
    onSuccess = null,
    onError = null,
    successMessage = null,
    errorMessage = null,
    showToast = true
  }) => {
    setLoading(true);

    try {
      const config = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...headers
        }
      };

      if (data) {
        if (data instanceof FormData) {
          // Remove Content-Type for FormData to let browser set it
          delete config.headers['Content-Type'];
          config.body = data;
        } else {
          config.body = JSON.stringify(data);
        }
      }

      const response = await fetch(url, config);
      const result = await response.json();

      if (response.ok) {
        if (showToast && successMessage) {
          toastLib.success(successMessage);
        }
        if (onSuccess) {
          onSuccess(result);
        }
        return { success: true, data: result };
      } else {
        const errorMsg = errorMessage || result.error || 'Request failed';
        if (showToast) {
          toastLib.error(errorMsg);
        }
        if (onError) {
          onError(result);
        }
        return { success: false, error: result };
      }
    } catch (error) {
      console.error('API Error:', error);
      const errorMsg = errorMessage || 'An unexpected error occurred';
      if (showToast) {
        toastLib.error(errorMsg);
      }
      if (onError) {
        onError(error);
      }
      return { success: false, error };
    } finally {
      setLoading(false);
    }
  }, []);

  const get = useCallback((url, options = {}) => {
    return apiCall({ url, method: 'GET', ...options });
  }, [apiCall]);

  const post = useCallback((url, data, options = {}) => {
    return apiCall({ url, method: 'POST', data, ...options });
  }, [apiCall]);

  const put = useCallback((url, data, options = {}) => {
    return apiCall({ url, method: 'PUT', data, ...options });
  }, [apiCall]);

  const del = useCallback((url, options = {}) => {
    return apiCall({ url, method: 'DELETE', ...options });
  }, [apiCall]);

  return {
    loading,
    apiCall,
    get,
    post,
    put,
    delete: del
  };
};

// Predefined API endpoints
export const apiEndpoints = {
  // Authentication
  // login: '/api/userlogin',
  // register: '/api/registeruser',
  // registerAdmin: '/api/registeradmin',
  
  // Forms
  // newRequest: '/api/newrequest',
  // adminPage: '/api/adminpage',
  
  // Analysis
  incidentAnalysis: '/api/incidentanalysis',
  serviceAnalysis: '/api/servicedeskanalysis',
  
  // Dashboard
  superAdminDashboard: '/api/superadmindashboard',
  
  // Chat
  chatbot: '/api/chatbot',
  
  // Logs
  applicationsLog: '/api/applicationslog'
}; 
