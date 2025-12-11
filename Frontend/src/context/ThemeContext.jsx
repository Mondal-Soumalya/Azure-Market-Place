import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [isLightMode, setIsLightMode] = useState(false);

  // Initialize theme from localStorage or OS preference
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
    
    if (savedTheme) {
      setIsLightMode(savedTheme === 'light');
    } else {
      setIsLightMode(prefersLight);
    }
  }, []);

  // Apply theme to body
  useEffect(() => {
    const body = document.body;
    
    // Remove existing theme classes
    body.classList.remove('light-mode', 'blue-theme');
    
    if (isLightMode) {
      body.classList.add('light-mode');
    } else {
      body.classList.add('blue-theme');
    }
    
    localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
  }, [isLightMode]);

  // Initialize body classes on first load
  useEffect(() => {
    const body = document.body;
    if (!body.classList.contains('homepage')) {
      body.classList.add('homepage');
    }
    if (!body.classList.contains('blue-theme') && !body.classList.contains('light-mode')) {
      body.classList.add('blue-theme');
    }
  }, []);

  const toggleTheme = () => {
    setIsLightMode(!isLightMode);
  };

  const value = {
    isLightMode,
    toggleTheme,
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
