import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toastLib from '../utils/toast';
import ParticlesBackground from '../components/ParticlesBackground';
import './NewRequestPage.css';

const NewRequestPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    account_name: '',
    use_case_name: '',
    region: '',
    sub_region: '',
    brief_description: '',
    tower: '',
    itsm_tool: '',
    cloud_onprem: '',
    cloud_onprem_env: '',
    scripting_language: '',
    eaf_dop: '',
    existing_automation: '',
    manual_approval: '',
    trigger_automation: '',
    auth_mechanism: '',
    regional_sme_email: '',
    customer_approval: '',
    sdm_approval: '',
    uat_env_availability: '',
    bot_test_service_account: '',
    jump_server_available: '',
    multidomain_credentials: '',
    sop_file: null
  });

  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState('No file selected');

  // Calculate form progress
  useEffect(() => {
    const requiredFields = [
      'account_name', 'use_case_name', 'region', 'brief_description',
      'tower', 'itsm_tool', 'cloud_onprem_env', 'scripting_language',
      'existing_automation', 'manual_approval', 'regional_sme_email',
      'customer_approval', 'sdm_approval', 'uat_env_availability',
      'jump_server_available', 'sop_file'
    ];

    const filledFields = requiredFields.filter(field => {
      if (field === 'sop_file') {
        return formData[field] !== null;
      }
      return formData[field] && formData[field].toString().trim() !== '';
    }).length;

    const progressPercent = Math.round((filledFields / requiredFields.length) * 100);
    setProgress(progressPercent);
  }, [formData]);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;
    
    if (type === 'file') {
      if (files && files.length > 0) {
        const file = files[0];
        if (file.name.toLowerCase().endsWith('.docx')) {
          setFormData(prev => ({ ...prev, [name]: file }));
          setFileName(file.name);
        } else {
          toastLib.error('Please upload a .docx file.');
          e.target.value = '';
          setFileName('No file selected');
        }
      }
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    
    // Remove error styling on focus
    e.target.classList.remove('input-error');
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);

    try {
      const formDataObj = new FormData();
      
      // Append all form data
      Object.keys(formData).forEach(key => {
        if (formData[key] !== null) {
          formDataObj.append(key, formData[key]);
        }
      });

      const response = await fetch('/api/newrequest', {
        method: 'POST',
        body: formDataObj
      });

      const result = await response.json();

      if (response.ok) {
        toastLib.success(result.message || 'Enhancement request submitted successfully!');
        navigate('/');
      } else {
        toastLib.error(result.error || 'Failed to submit enhancement request.');
      }
    } catch (error) {
      console.error('Submission error:', error);
      toastLib.error('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const pageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.6, ease: "easeOut" }
    }
  };

  return (
    <>
      <ParticlesBackground />
      <motion.div
        className="form-page-content"
        variants={pageVariants}
        initial="hidden"
        animate="visible"
      >
      <div className="container form-container">
        {/* Progress Tracker */}
        <div className="progress-tracker" data-section="form-header">
          <h3>📊 Enhancement Request Progress</h3>
          <div className="progress-bar-container">
            <div 
              className="progress-bar-fill" 
              id="form-progress-bar" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className="progress-bar-text" id="form-progress-text">
            {progress}% Complete
          </span>
        </div>

        {/* Form */}
        <form id="enhancement-form" onSubmit={handleSubmit}>
          {/* Basic Information */}
          <fieldset data-section="basic-info">
            <legend>
              <i className="fas fa-info-circle"></i> Basic Information
            </legend>
            <p style={{ color: '#a0aec0', fontSize: '13px', marginBottom: '20px', marginTop: '-5px' }}>
              ℹ️ Provide essential details about your enhancement request
            </p>
            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="account-name">ACCOUNT NAME:</label>
                <input
                  type="text"
                  id="account-name"
                  name="account_name"
                  value={formData.account_name}
                  onChange={handleInputChange}
                  placeholder="Enter customer account name"
                  required
                />
              </div>
              <div className="form-group half-width">
                <label htmlFor="use-case-name">USE CASE NAME:</label>
                <input
                  type="text"
                  id="use-case-name"
                  name="use_case_name"
                  value={formData.use_case_name}
                  onChange={handleInputChange}
                  placeholder="e.g., AIX CPU Memory Utilization"
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="region">REGION:</label>
                <input
                  type="text"
                  id="region"
                  name="region"
                  value={formData.region}
                  onChange={handleInputChange}
                  placeholder="e.g., NA, EU, APAC"
                  required
                />
              </div>
              <div className="form-group third-width">
                <label htmlFor="sub-region">SUB-REGION:</label>
                <input
                  type="text"
                  id="sub-region"
                  name="sub_region"
                  value={formData.sub_region}
                  onChange={handleInputChange}
                  placeholder="e.g., US, UK, India"
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="brief-description">SHORT DESCRIPTION:</label>
              <textarea
                id="brief-description"
                name="brief_description"
                rows="3"
                value={formData.brief_description}
                onChange={handleInputChange}
                placeholder="Briefly describe the automation requirement and business value"
                required
              ></textarea>
            </div>
          </fieldset>

          {/* Technical Details */}
          <fieldset data-section="technical-details">
            <legend>
              <i className="fas fa-cogs"></i> Technical Details
            </legend>
            <p style={{ color: '#a0aec0', fontSize: '13px', marginBottom: '20px', marginTop: '-5px' }}>
              🔧 Specify the technology stack and environment configuration
            </p>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="tower">TECHNOLOGY:</label>
                <input
                  type="text"
                  id="tower"
                  name="tower"
                  value={formData.tower}
                  onChange={handleInputChange}
                  placeholder="e.g., Wintel, Unix, Linux"
                  required
                />
              </div>
              <div className="form-group third-width">
                <label htmlFor="itsm-tool">SNOW INTEGRATION:</label>
                <select
                  id="itsm-tool"
                  name="itsm_tool"
                  value={formData.itsm_tool}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="cloud-on-prem">SNOW INSTANCE:</label>
                <select
                  id="cloud-on-prem"
                  name="cloud_onprem"
                  value={formData.cloud_onprem}
                  onChange={handleInputChange}
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="cg">Capgemini</option>
                  <option value="client">Client</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="cloud-on-prem-env">CLOUD/ON-PREM:</label>
                <select
                  id="cloud-on-prem-env"
                  name="cloud_onprem_env"
                  value={formData.cloud_onprem_env}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Cloud">Cloud</option>
                  <option value="On-Premises">On-Premises</option>
                  <option value="Hybrid">Hybrid</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="scripting-language">SCRIPTING LANGUAGE:</label>
                <select
                  id="scripting-language"
                  name="scripting_language"
                  value={formData.scripting_language}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="PowerShell">PowerShell</option>
                  <option value="Python">Python</option>
                  <option value="Bash">BASH</option>
                  <option value="Ansible">Ansible</option>
                </select>
              </div>
              <div className="form-group half-width">
                <label htmlFor="eaf-non-eaf">EAF/non EAF (DOP /Non DOP):</label>
                <select
                  id="eaf-non-eaf"
                  name="eaf_dop"
                  value={formData.eaf_dop}
                  onChange={handleInputChange}
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="EAF - DOP">EAF - DOP</option>
                  <option value="Non EAF - Non DOP">Non EAF - Non DOP</option>
                  <option value="Partial EAF">Partial EAF</option>
                </select>
              </div>
            </div>
          </fieldset>

          {/* Automation Specifics */}
          <fieldset>
            <legend>
              <i className="fas fa-robot"></i> Automation Specifics
            </legend>
            <p style={{ color: '#a0aec0', fontSize: '13px', marginBottom: '20px', marginTop: '-5px' }}>
              🤖 Define automation requirements and approval workflow
            </p>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="existing-automation">EXISTING AUTOMATION:</label>
                <select
                  id="existing-automation"
                  name="existing_automation"
                  value={formData.existing_automation}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                  <option value="Partial">Partial</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="manual-approval">MANUAL/EXTERNAL APPROVAL/COMMUNICATION REQUIRED:</label>
                <select
                  id="manual-approval"
                  name="manual_approval"
                  value={formData.manual_approval}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="trigger-for-automation">TRIGGER FOR AUTOMATION:</label>
              <select
                id="trigger-for-automation"
                name="trigger_automation"
                value={formData.trigger_automation}
                onChange={handleInputChange}
              >
                <option value="" disabled>-- Select --</option>
                <option value="Manual">Manual</option>
                <option value="Schedule">Schedule</option>
              </select>
            </div>
            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="auth-mechanism">AUTHENTICATION MECHANISM FOR BOTS:</label>
                <input
                  type="text"
                  id="auth-mechanism"
                  name="auth_mechanism"
                  value={formData.auth_mechanism}
                  onChange={handleInputChange}
                  placeholder="e.g., OAuth 2.0, Basic Auth, API Key"
                  required
                />
              </div>
            </div>
          </fieldset>

          {/* Prerequisites & Environment */}
          <fieldset>
            <legend>
              <i className="fas fa-check-double"></i> Prerequisites & Environment
            </legend>
            <p style={{ color: '#a0aec0', fontSize: '13px', marginBottom: '20px', marginTop: '-5px' }}>
              ✅ Confirm environmental readiness and approval status
            </p>
            <div className="form-row">
              <div className="form-group half-width">
                <label htmlFor="sme-name-email">REGIONAL SME NAME & EMAIL:</label>
                <input
                  type="email"
                  id="sme-name-email"
                  name="regional_sme_email"
                  value={formData.regional_sme_email}
                  onChange={handleInputChange}
                  placeholder="e.g., john.smith@capgemini.com"
                  required
                />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="customer-approval">CUSTOMER APPROVAL:</label>
                <select
                  id="customer-approval"
                  name="customer_approval"
                  value={formData.customer_approval}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="sdm-approval">SDM APPROVAL:</label>
                <select
                  id="sdm-approval"
                  name="sdm_approval"
                  value={formData.sdm_approval}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Approved">Approved</option>
                  <option value="Pending">Pending</option>
                  <option value="Rejected">Rejected</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="env-availability">DEV/TEST Env AVAILABLE:</label>
                <select
                  id="env-availability"
                  name="uat_env_availability"
                  value={formData.uat_env_availability}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group third-width">
                <label htmlFor="service-account">SERVICE ACCOUNT:</label>
                <select
                  id="service-account"
                  name="bot_test_service_account"
                  value={formData.bot_test_service_account}
                  onChange={handleInputChange}
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Available">Available</option>
                  <option value="Not Available">Not Available</option>
                  <option value="Pending Request">Pending Request</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="jump-server">Jump/RAS SERVER AVAILABLE:</label>
                <select
                  id="jump-server"
                  name="jump_server_available"
                  value={formData.jump_server_available}
                  onChange={handleInputChange}
                  required
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
              <div className="form-group third-width">
                <label htmlFor="multidomain">MULTIDOMAIN LOGIN:</label>
                <select
                  id="multidomain"
                  name="multidomain_credentials"
                  value={formData.multidomain_credentials}
                  onChange={handleInputChange}
                >
                  <option value="" disabled>-- Select --</option>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                  <option value="N/A">N/A</option>
                </select>
              </div>
            </div>
          </fieldset>

          {/* SOP Document Upload */}
          <fieldset className="upload-section">
            <legend>
              <i className="fas fa-file-upload"></i> SOP Document Upload
            </legend>
            <p style={{ color: '#a0aec0', fontSize: '13px', marginBottom: '20px', marginTop: '-5px' }}>
              📄 Upload your Standard Operating Procedure (.docx format only)
            </p>
            <div className="form-group file-upload-group">
              <label htmlFor="sop-file" className="file-upload-label">
                <i className="fas fa-cloud-upload-alt"></i>
                <span>Drag & drop or click to select SOP Document</span>
              </label>
              <input
                type="file"
                id="sop-file"
                name="sop_file"
                accept=".docx"
                onChange={handleInputChange}
                required
              />
              <span id="file-name-display">{fileName}</span>
            </div>
          </fieldset>

          {/* Submit Button */}
          <button
            type="submit"
            id="submit-button"
            className="submit-button large-button"
            disabled={loading}
          >
            <span>
              {loading ? (
                <i className="fas fa-sync-alt fa-spin"></i>
              ) : (
                <i className="fas fa-paper-plane"></i>
              )}
              Submit Enhancement Request
            </span>
            <div className="button-loader"></div>
          </button>
        </form>
      </div>
    </motion.div>
    </>
  );
};

export default NewRequestPage;
