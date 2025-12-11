import { useState, useCallback } from 'react';
import toastLib from '../utils/toast';

export const useForm = (initialState = {}, validationRules = {}) => {
  const [formData, setFormData] = useState(initialState);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleInputChange = useCallback((e) => {
    const { name, value, type, files } = e.target;
    
    if (type === 'file') {
      if (files && files.length > 0) {
        const file = files[0];
        setFormData(prev => ({ ...prev, [name]: file }));
      }
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  }, [errors]);

  const validateField = useCallback((name, value) => {
    const rule = validationRules[name];
    if (!rule) return null;

    if (rule.required && !value) {
      return rule.required;
    }

    if (rule.pattern && !rule.pattern.test(value)) {
      return rule.pattern.message;
    }

    if (rule.minLength && value.length < rule.minLength) {
      return rule.minLength.message;
    }

    if (rule.custom) {
      return rule.custom(value);
    }

    return null;
  }, [validationRules]);

  const validateForm = useCallback(() => {
    const newErrors = {};
    let isValid = true;

    Object.keys(validationRules).forEach(fieldName => {
      const error = validateField(fieldName, formData[fieldName]);
      if (error) {
        newErrors[fieldName] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, [formData, validateField, validationRules]);

  const setFieldError = useCallback((fieldName, error) => {
    setErrors(prev => ({ ...prev, [fieldName]: error }));
  }, []);

  const clearErrors = useCallback(() => {
    setErrors({});
  }, []);

  const resetForm = useCallback(() => {
    setFormData(initialState);
    setErrors({});
    setLoading(false);
  }, [initialState]);

  const setLoadingState = useCallback((isLoading) => {
    setLoading(isLoading);
  }, []);

  return {
    formData,
    errors,
    loading,
    handleInputChange,
    validateForm,
    setFieldError,
    clearErrors,
    resetForm,
    setLoadingState,
    setFormData
  };
};

// Common validation rules
export const validationRules = {
  email: {
    required: 'Email is required',
    pattern: {
      test: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
      message: 'Please enter a valid email address'
    }
  },
  capgeminiEmail: {
    required: 'Email is required',
    pattern: {
      test: (value) => /^[a-zA-Z0-9._%+-]+@capgemini\.com$/.test(value),
      message: 'Please enter a valid Capgemini email address'
    }
  },
  password: {
    required: 'Password is required',
    minLength: {
      value: 8,
      message: 'Password must be at least 8 characters long'
    }
  },
  employeeId: {
    required: 'Employee ID is required',
    pattern: {
      test: (value) => /^\d{8}$/.test(value),
      message: 'Employee ID must be exactly 8 digits'
    }
  },
  file: {
    required: 'File is required',
    custom: (value) => {
      if (!value) return 'Please select a file';
      if (value.size > 10 * 1024 * 1024) return 'File size must be less than 10MB';
      return null;
    }
  }
}; 
