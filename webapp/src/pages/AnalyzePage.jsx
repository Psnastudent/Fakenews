import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { analyzeText, analyzeUrl, analyzeMedia } from '../services/api';

export default function AnalyzePage() {
  const [activeTab, setActiveTab] = useState('text');
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) setFile(droppedFile);
  };

  const handleAnalyze = async () => {
    if (!input && !file) return;
    setLoading(true);
    try {
      let result;
      if (activeTab === 'text') {
        result = await analyzeText(input);
      } else if (activeTab === 'url') {
        result = await analyzeUrl(input);
      } else if (activeTab === 'media' && file) {
        const type = file.type.startsWith('video') ? 'video' : 'image';
        result = await analyzeMedia(file, type);
      }
      navigate('/result', { state: { result } });
    } catch (error) {
      console.error('Analysis failed', error);
      alert('Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section-light" style={{ minHeight: '100vh', paddingTop: '160px' }}>
      <div className="container">
        
        <div style={{ textAlign: 'center', marginBottom: '64px' }} className="fade-in">
          <span className="eyebrow">Detection Module</span>
          <h2>Analyze Source Content</h2>
          <p style={{ maxWidth: '600px', margin: '24px auto', color: 'var(--text-secondary)' }}>
            Submit text, links, or media. Our multi-modal engine will cross-reference 
            with known datasets and use deep learning to detect anomalies.
          </p>
        </div>

        <div className="analyze-panel slide-up">
          <div className="tab-nav">
            <button className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`} onClick={() => setActiveTab('text')}>Text</button>
            <button className={`tab-btn ${activeTab === 'url' ? 'active' : ''}`} onClick={() => setActiveTab('url')}>URL</button>
            <button className={`tab-btn ${activeTab === 'media' ? 'active' : ''}`} onClick={() => setActiveTab('media')}>Media</button>
          </div>

          <div style={{ minHeight: '250px' }}>
            {activeTab === 'text' && (
              <textarea 
                className="input-field" 
                placeholder="Paste article text, tweet, or claim here..."
                value={input}
                onChange={e => setInput(e.target.value)}
              />
            )}

            {activeTab === 'url' && (
              <input 
                type="url"
                className="input-field" 
                placeholder="https://example.com/news-article"
                value={input}
                onChange={e => setInput(e.target.value)}
              />
            )}

            {activeTab === 'media' && (
              <div>
                <div 
                  className="dropzone"
                  onDragOver={e => e.preventDefault()}
                  onDrop={handleFileDrop}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <h3 style={{ marginBottom: '8px' }}>Drag and drop media here</h3>
                  <p style={{ color: 'var(--text-muted)' }}>Supports JPG, PNG, MP4 (Max 50MB)</p>
                  <input 
                    type="file" 
                    hidden 
                    ref={fileInputRef}
                    accept="image/*,video/*"
                    onChange={e => setFile(e.target.files[0])}
                  />
                </div>
                {file && (
                  <div style={{ padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '8px', marginBottom: '24px', fontFamily: 'var(--font-mono)' }}>
                    File attached: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </div>
                )}
              </div>
            )}
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '24px' }}>
            <button 
              className="btn-black" 
              onClick={handleAnalyze}
              disabled={loading || (!input && !file)}
            >
              {loading ? <div className="spinner"/> : 'Initiate Scan'}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
