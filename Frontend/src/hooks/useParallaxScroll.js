import { useState, useEffect, useCallback } from 'react';

// Throttle function for performance
const throttle = (func, delay) => {
  let timeoutId;
  let lastExecTime = 0;
  return function (...args) {
    const currentTime = Date.now();
    
    if (currentTime - lastExecTime > delay) {
      func.apply(this, args);
      lastExecTime = currentTime;
    } else {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func.apply(this, args);
        lastExecTime = Date.now();
      }, delay - (currentTime - lastExecTime));
    }
  };
};

export const useParallaxScroll = () => {
  const [scrollY, setScrollY] = useState(0);
  const [scrollDirection, setScrollDirection] = useState('down');
  const [lastScrollY, setLastScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = throttle(() => {
      const currentScrollY = window.scrollY;
      
      // Determine scroll direction
      if (currentScrollY > lastScrollY) {
        setScrollDirection('down');
      } else if (currentScrollY < lastScrollY) {
        setScrollDirection('up');
      }
      
      setScrollY(currentScrollY);
      setLastScrollY(currentScrollY);
    }, 16); // 60fps throttling
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    return () => window.removeEventListener('scroll', handleScroll);
  }, [lastScrollY]);

  // Optimized mathematical parallax calculations
  const getParallaxOffset = useCallback((speed = 0.5, reverse = false) => {
    const offset = Math.round(scrollY * speed * 0.5); // Reduced multiplier and rounded
    return reverse ? -offset : offset;
  }, [scrollY]);

  const getParallaxOpacity = useCallback((triggerPoint = 0, fadeDistance = 200) => {
    const distance = Math.abs(scrollY - triggerPoint);
    return Math.max(0, Math.min(1, 1 - (distance / fadeDistance)));
  }, [scrollY]);

  const getParallaxScale = useCallback((baseScale = 1, maxScale = 1.05, triggerPoint = 0) => {
    const distance = Math.abs(scrollY - triggerPoint);
    const scaleMultiplier = Math.max(0, Math.min(1, 1 - (distance / 800))); // Increased distance for smoother scaling
    return baseScale + ((maxScale - baseScale) * scaleMultiplier);
  }, [scrollY]);

  return {
    scrollY,
    scrollDirection,
    getParallaxOffset,
    getParallaxOpacity,
    getParallaxScale
  };
};

export default useParallaxScroll;
