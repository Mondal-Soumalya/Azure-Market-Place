import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Header from './components/Header';
import Footer from './components/Footer';
import ProfessionalHomePage from './pages/ProfessionalHomePage';
import AboutUsPage from './pages/AboutUsPage';
// import NewRequestPage from './pages/NewRequestPage';
import AnalysisEnginePage from './pages/AnalysisEnginePage';
// import ServiceDeskAnalysisPage from './pages/ServiceDeskAnalysisPage';
import PageNotFound from './pages/PageNotFound';
import ErrorBoundary from './components/ErrorBoundary';

// Create a dark theme
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#66FFE0', // Updated primary color
    },
    secondary: {
      main: '#6366f1',
    },
    background: {
      default: '#1e2a3a',
      paper: '#1a1a1a',
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b0b0',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
});




function App() {
  const [isDarkMode, setIsDarkMode] = React.useState(true);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <Router>
          <div className="App">
            <Header isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
            <main>
              <Routes>
                <Route path="/" element={<ProfessionalHomePage />} />
                <Route path="/about" element={<AboutUsPage />} />
                {/* <Route path="/newrequest" element={<NewRequestPage />} /> */}
                <Route path="/analysisenginepage" element={<AnalysisEnginePage />} />
                {/* <Route path="/servicedeskanalysis" element={<ServiceDeskAnalysisPage />} /> */}
                {/* <Route path="/demo3d" element={<Demo3DPage />} /> */}
                {/* Catch-all route for 404 - Page Not Found */}
                <Route path="*" element={<PageNotFound />} />
              </Routes>
            </main>
            <Footer />
              
              {/* Toast Notifications Container */}
              <ToastContainer
                position="top-right"
                autoClose={3000}
                newestOnTop={false}
                closeOnClick
                pauseOnHover
                draggable
                theme="colored"
              />
          </div>
        </Router>
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;
