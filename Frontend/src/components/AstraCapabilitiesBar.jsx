import React from 'react';
import { 
  AutoAwesome, 
  Speed, 
  Security, 
  Analytics, 
  CloudQueue, 
  Psychology 
} from '@mui/icons-material';

// Color constants
export const UNIFIED_BEIGE = '#F5E6D3';
export const UNIFIED_WHITE = '#FFFFFF';

// Capabilities data
export const items = [
  {
    label: 'AI-Powered Solutions',
    icon: AutoAwesome,
    description: 'Advanced artificial intelligence capabilities'
  },
  {
    label: 'High Performance',
    icon: Speed,
    description: 'Optimized for speed and efficiency'
  },
  {
    label: 'Enterprise Security',
    icon: Security,
    description: 'Bank-level security standards'
  },
  {
    label: 'Advanced Analytics',
    icon: Analytics,
    description: 'Deep insights and reporting'
  },
  {
    label: 'Cloud Integration',
    icon: CloudQueue,
    description: 'Seamless cloud connectivity'
  },
  {
    label: 'Smart Automation',
    icon: Psychology,
    description: 'Intelligent process automation'
  }
];

// Default export (placeholder component)
const AstraCapabilitiesBar = () => {
  return null; // This component is used for exports only
};

export default AstraCapabilitiesBar;
