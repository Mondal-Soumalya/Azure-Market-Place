import React, { useEffect, useRef, useState } from 'react';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import AstraCapabilitiesBar, { items, UNIFIED_BEIGE, UNIFIED_WHITE } from './AstraCapabilitiesBar';

/*
  HomeCapabilitiesFloating
  - Renders capabilities as text badges inline (centered) beneath hero on initial load
  - On scroll past threshold, badges animate into a fixed left vertical stack (text only)
  - Uses Framer Motion layout animations for position/axis transition
  - Accessible: role=list / listitem; honors prefers-reduced-motion
  - Mobile (< md): remains inline; floating disabled
*/

const SCROLL_THRESHOLD = 120; // px before icons dock left
const LEFT_OFFSET = 18; // px from left when fixed
const TOP_OFFSET = 150; // px from top when fixed
const GAP = 22; // vertical gap between stacked icons

// 3D floating icon only (no box) with beige/white palette (no glow)
const FloatingCapabilityItem = ({ item, index, pointer, scrollFactor, reducedMotion }) => {
  const transform = reducedMotion
    ? 'none'
    : `translate3d(${pointer.x * 6}px, ${pointer.y * 6 - scrollFactor * 3}px, 0) perspective(900px) rotateX(${pointer.y * 5}deg) rotateY(${pointer.x * 8}deg)`;

  return (
    <motion.li
      role="listitem"
      initial={{ opacity: 0, x: -50, scale: 0.6, rotateY: -25 }}
      animate={{ opacity: 1, x: 0, scale: 1, rotateY: 0 }}
      exit={{ opacity: 0, x: -50, scale: 0.6, rotateY: -25 }}
      transition={{ duration: 0.55, delay: index * 0.07, ease: [0.23, 1, 0.32, 1] }}
      style={{ listStyle: 'none' }}
    >
      <Box
        sx={{
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: 56,
          height: 56,
          transform,
          transformStyle: 'preserve-3d',
          cursor: 'pointer'
        }}
      >
        <item.icon
          sx={{
            fontSize: 32,
            color: UNIFIED_BEIGE,
            filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.45))',
            transition: 'transform .4s cubic-bezier(0.23,1,0.32,1), filter .4s',
            transform: 'translateZ(12px)',
            position: 'relative',
            zIndex: 2,
            '&:hover': { filter: 'drop-shadow(0 5px 12px rgba(0,0,0,0.6))' }
          }}
        />
        <span style={{ position: 'absolute', width: 1, height: 1, padding: 0, margin: -1, overflow: 'hidden', clip: 'rect(0 0 0 0)', whiteSpace: 'nowrap', border: 0 }}>
          {item.label}
        </span>
      </Box>
    </motion.li>
  );
};

const HomeCapabilitiesFloating = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [floating, setFloating] = useState(false);
  const [ready, setReady] = useState(false);
  const rootRef = useRef(null);
  const [pointer, setPointer] = useState({ x: 0, y: 0 }); // normalized -0.5..0.5
  const [scrollFactor, setScrollFactor] = useState(0); // 0..1 for progressive intensity
  const reducedMotion = useRef(false);
  const rafRef = useRef();
  const initialHeightRef = useRef(0);

  // debug logs removed for production polish

  // Capture initial inline height so when we switch to floating we keep a placeholder and avoid layout jump
  useEffect(() => {
    if (rootRef.current) {
      initialHeightRef.current = rootRef.current.offsetHeight;
    }
  }, []);

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    reducedMotion.current = mq.matches;

    const handleScroll = () => {
      if (isMobile || mq.matches) return;
      const y = window.scrollY || window.pageYOffset;
      const shouldFloat = y > SCROLL_THRESHOLD;
      if (shouldFloat !== floating) setFloating(shouldFloat);
      const base = shouldFloat ? Math.min(400, Math.max(0, y - SCROLL_THRESHOLD)) : 0;
      setScrollFactor(base / 400);
    };

    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
    setReady(true);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isMobile, floating]);

  // Global pointer tracker for parallax feeling "user is controlling" the system
  useEffect(() => {
    if (isMobile) return;
    const onMove = (e) => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const nx = (e.clientX / vw) - 0.5; // -0.5..0.5
      const ny = (e.clientY / vh) - 0.5;
      rafRef.current = requestAnimationFrame(() => {
        setPointer({ x: nx, y: ny });
      });
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => {
      window.removeEventListener('pointermove', onMove);
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [isMobile]);

  // Provide a11y announcement when state changes
  useEffect(() => {
    if (!ready) return;
    const el = document.getElementById('capabilities-announcer');
    if (el) {
      el.textContent = floating ? 'Capabilities sidebar engaged' : 'Capabilities inline';
    }
  }, [floating, ready]);

  return (
    <>
      <Box id="capabilities-announcer" sx={{ position: 'absolute', width: 1, height: 1, overflow: 'hidden', clip: 'rect(0 0 0 0)' }} aria-live="polite" />
  <Box ref={rootRef} sx={{ position: 'relative', zIndex: 2, minHeight: initialHeightRef.current || undefined }}>
        {/* Inline layout placeholder - Icons with text centered */}
        <AnimatePresence initial={false}>
          {(!floating || isMobile) && (
            <motion.div
              key="inline"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.4 }}
              style={{ 
                display: 'flex', 
                justifyContent: 'center',
                padding: '20px 20px 30px 20px', // Reduced padding for hero section
              }}
            >
              <AstraCapabilitiesBar />
            </motion.div>
          )}
        </AnimatePresence>

  {/* Floating stack - Icons with text and enhanced interactive 3D + parallax */}
        <AnimatePresence>
          {floating && !isMobile && (
            <motion.ul
              key="floating"
              role="list"
              aria-label="PRISM ANALYTICS capabilities"
              initial={{ opacity: 0, x: -80 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -80 }}
              transition={{ 
                duration: 0.5, 
                ease: [0.23, 1, 0.32, 1],
                staggerChildren: 0.1
              }}
              style={{
                listStyle: 'none',
                margin: 0,
                padding: 0,
                position: 'fixed',
                left: LEFT_OFFSET,
                top: TOP_OFFSET,
                zIndex: 9999,
                display: 'flex',
                flexDirection: 'column',
                gap: GAP,
                pointerEvents: 'auto',
              }}
            >
              {items.map((it, i) => (
                <FloatingCapabilityItem
                  key={it.label}
                  item={it}
                  index={i}
                  pointer={pointer}
                  scrollFactor={scrollFactor}
                  reducedMotion={reducedMotion.current}
                />
              ))}
            </motion.ul>
          )}
        </AnimatePresence>
      </Box>
    </>
  );
};

export default HomeCapabilitiesFloating;
