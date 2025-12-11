import React from 'react';
import { motion } from 'framer-motion';

const PageContainer = ({
  children,
  title,
  subtitle,
  className = '',
  containerClass = 'form-container',
  showHeader = true,
  ...props
}) => {
  const pageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  };

  return (
    <motion.div
      className={`form-page-content ${className}`}
      variants={pageVariants}
      initial="hidden"
      animate="visible"
      {...props}
    >
      <div className={`container ${containerClass}`}>
        {showHeader && (title || subtitle) && (
          <div className="page-header mb-6">
            {title && (
              <motion.h1 
                className="page-title"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                {title}
              </motion.h1>
            )}
            {subtitle && (
              <motion.p 
                className="page-subtitle text-text-secondary"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                {subtitle}
              </motion.p>
            )}
          </div>
        )}
        {children}
      </div>
    </motion.div>
  );
};

export default PageContainer; 
