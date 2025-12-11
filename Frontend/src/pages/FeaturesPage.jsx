import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowLeft, Network, CheckCircle, Sparkles, Zap, Shield } from 'lucide-react';

const FeaturesPage = () => {
  const { scrollY } = useScroll();
  const [activeSection, setActiveSection] = useState(0);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.1,
      },
    },
  };

  const cardVariants = {
    hidden: { 
      opacity: 0, 
      y: 30,
      scale: 0.95
    },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      transition: { 
        duration: 0.6, 
        ease: [0.25, 0.46, 0.45, 0.94],
        type: "spring",
        stiffness: 100
      }
    },
    hover: {
      y: -8,
      scale: 1.02,
      transition: {
        duration: 0.3,
        ease: "easeOut"
      }
    }
  };

  const features = [
    {
      id: 1,
      title: "Incident Dump Analysis",
      subtitle: "AI-Powered Document Intelligence",
      description: "Leverage advanced Natural Language Processing (NLP) and machine learning models to automatically scan, classify, and extract vital information from diverse document types.",
      icon: "fas fa-chart-pie",
      status: "coming-soon",
      benefits: [
        "Automated data extraction (entities, clauses, tables)",
        "Sentiment analysis and topic modeling",
        "Anomaly detection and risk identification",
        "Customizable extraction templates",
        "Integration with existing data lakes and warehouses"
      ],
      highlight: "Transform unstructured data into actionable business intelligence. Reduce manual review time significantly."
    },
    {
      id: 2,
      title: "Intelligent Chatbot",
      subtitle: "RAG-Powered Knowledge Assistant",
      description: "Combine the power of large language models (LLMs) with your organization's private knowledge base using Retrieval-Augmented Generation.",
      icon: "fas fa-brain",
      status: "coming-soon",
      benefits: [
        "Secure querying of internal documents and databases",
        "Source attribution for generated responses (traceability)",
        "Automated report generation and summarization",
        "Enhanced chatbot capabilities with factual grounding",
        "Fine-tuning options for specific industry terminology"
      ],
      highlight: "Empower your teams with instant access to verified information and generate reliable content faster."
    },
    {
      id: 3,
      title: "Automation Workflow Hub",
      subtitle: "Streamlined Request Management",
      description: "A centralized module to streamline the ideation, submission, approval, and tracking of automation enhancement requests within your enterprise.",
      icon: "fas fa-sitemap",
      status: "active",
      benefits: [
        "Standardized data capture form for consistent requests",
        "Secure document upload (SOPs, requirements)",
        "Backend integration via API for processing and workflow initiation",
        "Submission summary and confirmation",
        "(Future) Dashboard for tracking request status"
      ],
      highlight: "Accelerate your automation pipeline by standardizing the intake process and ensuring all necessary information is captured upfront."
    }
  ];

  return (
    <div className="features-page-wrapper">
      <style>{`
        .features-page-wrapper {
          min-height: 100vh;
          background: linear-gradient(120deg, var(--bg-primary) 60%, var(--accent-secondary-tint) 100%);
          position: relative;
          overflow-x: hidden;
          overflow-y: auto;
          scroll-behavior: smooth;
        }
        .features-page-wrapper::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: radial-gradient(circle at 80% 10%, var(--accent-primary-tint) 0%, transparent 60%), radial-gradient(circle at 10% 90%, var(--accent-secondary-tint) 0%, transparent 60%);
          pointer-events: none;
          z-index: 0;
        }
        .features-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2.5rem 1.5rem 4rem 1.5rem;
          position: relative;
          z-index: 1;
        }
        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
          gap: 2.5rem;
          margin-top: 3.2rem;
        }
        .feature-card {
          background: linear-gradient(120deg, var(--bg-secondary) 80%, var(--accent-primary-tint) 100%);
          border: 1.5px solid var(--border-color);
          border-radius: 2.2rem;
          padding: 2.7rem 1.7rem 1.7rem 1.7rem;
          position: relative;
          overflow: visible;
          cursor: pointer;
          transition: box-shadow 0.32s cubic-bezier(0.4,0,0.2,1), transform 0.32s cubic-bezier(0.4,0,0.2,1), background 0.32s;
          outline: none;
          z-index: 1;
          box-shadow: 0 8px 36px 0 rgba(100,255,218,0.13), 0 2px 12px 0 var(--shadow-md);
        }
        .feature-card:focus {
          box-shadow: 0 0 0 2px var(--accent-primary), 0 8px 40px 0 var(--accent-primary-tint);
        }
        .feature-card:hover {
          background: linear-gradient(120deg, var(--accent-primary-tint) 0%, var(--bg-tertiary) 100%);
          border-color: var(--accent-primary);
          transform: translateY(-12px) scale(1.035);
          box-shadow: 0 16px 48px 0 rgba(100,255,218,0.18), 0 4px 16px 0 var(--shadow-lg);
        }
        .status-badge {
          position: absolute;
          top: 0.7rem;
          right: 0.7rem;
          padding: 0.13rem 0.6rem;
          border-radius: 1em;
          font-size: 0.68rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          z-index: 3;
          box-shadow: 0 2px 8px var(--shadow-sm);
          background-clip: padding-box;
          border: none;
          opacity: 0.97;
          backdrop-filter: blur(2px);
        }
        .status-badge.active {
          background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
          color: var(--bg-primary);
          box-shadow: 0 2px 8px var(--accent-primary-tint);
        }
        .status-badge.coming-soon {
          background: linear-gradient(90deg, var(--info-bg), var(--accent-secondary-tint));
          color: var(--info-text);
          border: 1px solid var(--info-border);
          font-size: 0.62rem;
          padding: 0.13rem 0.45rem;
          font-weight: 700;
          opacity: 0.92;
        }
        .feature-header {
          display: flex;
          align-items: center;
          gap: 1.2rem;
          margin-bottom: 1.3rem;
        }
        .feature-icon {
          width: 62px;
          height: 62px;
          border-radius: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--accent-primary-tint) 60%, var(--accent-secondary-tint) 100%);
          border: 2px solid var(--accent-secondary);
          transition: all 0.32s cubic-bezier(0.4,0,0.2,1);
          z-index: 2;
          box-shadow: 0 2px 12px 0 var(--accent-secondary-tint);
        }
        .feature-card:hover .feature-icon {
          background: linear-gradient(135deg, var(--accent-primary-tint) 0%, var(--accent-secondary-tint) 100%);
          border-color: var(--accent-primary);
          transform: scale(1.13) rotate(-8deg);
        }
        .feature-icon i {
          font-size: 2.3rem;
          color: var(--accent-secondary);
          transition: color 0.32s cubic-bezier(0.4,0,0.2,1);
          filter: drop-shadow(0 2px 8px var(--accent-secondary-tint));
        }
        .feature-card:hover .feature-icon i {
          color: var(--accent-primary);
          filter: drop-shadow(0 2px 8px var(--accent-primary-tint));
        }
        .feature-title {
          font-size: 1.38rem;
          font-weight: 700;
          color: var(--text-primary);
          margin-bottom: 0.18rem;
          line-height: 1.3;
          letter-spacing: 0.01em;
        }
        .feature-subtitle {
          font-size: 1.04rem;
          color: var(--text-muted);
          font-weight: 500;
          letter-spacing: 0.01em;
        }
        .feature-description {
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 1.2rem;
          font-size: 1.01rem;
        }
        .feature-benefits {
          background: linear-gradient(90deg, var(--bg-primary) 80%, var(--accent-primary-tint) 100%);
          border-radius: 16px;
          padding: 1.2rem 1.3rem;
          margin-bottom: 1.2rem;
          border: 1px solid var(--border-color);
          box-shadow: 0 1px 6px 0 var(--shadow-sm);
        }
        .feature-benefits h4 {
          color: var(--accent-secondary);
          font-size: 1.01rem;
          font-weight: 600;
          margin-bottom: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .benefits-list {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        .benefits-list li {
          display: flex;
          align-items: flex-start;
          gap: 0.7rem;
          color: var(--text-primary);
          font-size: 1.01rem;
          line-height: 1.5;
          margin-bottom: 0.5rem;
          padding: 0.4rem 0.2rem;
          border-radius: 8px;
          transition: background 0.18s cubic-bezier(0.4,0,0.2,1);
        }
        .benefits-list li:hover {
          background: var(--accent-secondary-tint);
        }
        .benefits-list li:last-child {
          margin-bottom: 0;
        }
        .benefits-list li svg {
          color: var(--accent-primary);
          flex-shrink: 0;
          margin-top: 0.125rem;
          filter: drop-shadow(0 1px 4px var(--accent-primary-tint));
        }
        .feature-highlight {
          background: linear-gradient(90deg, var(--accent-primary-tint) 80%, var(--accent-secondary-tint) 100%);
          border: 1px solid var(--accent-primary);
          border-radius: 15px;
          padding: 1.1rem 1.2rem;
          font-style: italic;
          color: var(--accent-primary);
          font-size: 1.01rem;
          line-height: 1.5;
          box-shadow: 0 1px 6px 0 var(--shadow-sm);
        }
        /* Responsive design */
        @media (max-width: 768px) {
          .features-container {
            padding: 1rem 0.5rem 2rem 0.5rem;
          }
          .features-grid {
            grid-template-columns: 1fr;
            gap: 1.2rem;
          }
          .feature-card {
            padding: 1.1rem 0.7rem 0.7rem 0.7rem;
            padding-top: 2.2rem;
          }
        }
      `}</style>

      <div className="features-container">
        <motion.div 
          className="page-header"
          data-section="features-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        >
          <Link to="/" className="back-button">
            <ArrowLeft size={16} />
            Back to Platform Overview
          </Link>

          <motion.h1 
            className="page-title"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            C.R.E.A.T.E Core Capabilities
          </motion.h1>
          
          <motion.p 
            className="page-subtitle"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            Explore the powerful AI-driven modules that form the foundation of the DocuForge platform. 
            Each capability is designed to streamline your workflow and enhance productivity.
          </motion.p>
        </motion.div>

        <motion.div 
          className="features-grid"
          data-section="capabilities-grid"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.id}
              className="feature-card"
              variants={cardVariants}
              whileHover="hover"
              onClick={() => setActiveSection(index)}
            >
              <div className={`status-badge ${feature.status}`}>
                {feature.status === 'active' ? 'Active' : 'Coming Soon'}
              </div>

              <div className="feature-header">
                <div className="feature-icon">
                  <i className={feature.icon}></i>
                </div>
                <div>
                  <h3 className="feature-title">{feature.title}</h3>
                  <p className="feature-subtitle">{feature.subtitle}</p>
                </div>
              </div>

              <p className="feature-description">{feature.description}</p>

              <div className="feature-benefits">
                <h4>Key Benefits</h4>
                <ul className="benefits-list">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx}>
                      <CheckCircle size={16} />
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="feature-highlight">
                {feature.highlight}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};

export default FeaturesPage;
