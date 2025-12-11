import React from 'react';
import { motion } from 'framer-motion';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Error caught by boundary:', error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="error-boundary min-h-screen flex items-center justify-center bg-bg-primary"
        >
          <div className="text-center p-8 max-w-md">
            <div className="mb-6">
              <i className="fas fa-exclamation-triangle text-red-500 text-6xl mb-4"></i>
              <h1 className="text-2xl font-bold text-text-primary mb-2">
                Oops! Something went wrong
              </h1>
              <p className="text-text-secondary mb-6">
                We're sorry, but something unexpected happened. Please try refreshing the page.
              </p>
            </div>
            
            <div className="space-y-4">
              <button
                onClick={() => window.location.reload()}
                className="bg-accent-primary text-bg-primary px-6 py-3 rounded-md font-medium hover:bg-accent-primary/90 transition-colors"
              >
                <i className="fas fa-redo mr-2"></i>
                Refresh Page
              </button>
              
              <button
                onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
                className="bg-bg-tertiary text-text-secondary px-6 py-3 rounded-md font-medium hover:bg-bg-secondary transition-colors ml-4"
              >
                <i className="fas fa-home mr-2"></i>
                Go Home
              </button>
            </div>
            
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <details className="mt-6 text-left">
                <summary className="cursor-pointer text-text-secondary hover:text-text-primary">
                  Error Details (Development)
                </summary>
                <div className="mt-2 p-4 bg-bg-secondary rounded-md text-sm font-mono text-text-secondary overflow-auto">
                  <div className="mb-2">
                    <strong>Error:</strong>
                    <pre className="whitespace-pre-wrap">{this.state.error.toString()}</pre>
                  </div>
                  <div>
                    <strong>Stack Trace:</strong>
                    <pre className="whitespace-pre-wrap">{this.state.errorInfo.componentStack}</pre>
                  </div>
                </div>
              </details>
            )}
          </div>
        </motion.div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
