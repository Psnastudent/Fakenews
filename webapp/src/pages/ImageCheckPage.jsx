import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API = '/api/v1/check';
const steps = [
  'Extract image metadata & EXIF data',
  'Perform Reverse Image Search',
  'Run OCR to extract text from image',
  'Detect digital manipulation & AI generation',
  'Generate verdict & truth score'
];

export default function ImageCheckPage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const analyze = async () => {
    if (!url.trim()) return;
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/image`, {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: url.trim(), content_type: 'image' }),
      });
      if (!res.ok) { 
        const e = await res.json().catch(() => ({})); 
        throw new Error(e.detail || `Server error (${res.status})`); 
      }
      const data = await res.json();
      
      // Save to local history
      const history = JSON.parse(localStorage.getItem('factcheck_history') || '[]');
      history.unshift({ 
        text: `Image: ${url.trim().slice(0, 50)}...`, 
        verdict: data.verdict, 
        score: data.truth_score, 
        date: new Date().toISOString(), 
        type: 'image' 
      });
      localStorage.setItem('factcheck_history', JSON.stringify(history.slice(0, 50)));
      
      navigate('/result', { state: { result: data } });
    } catch (e) { 
      setError(e.message || 'Failed to analyze image.'); 
    } finally { 
      setLoading(false); 
    }
  };

  return (
    <div className="sub-page container page-enter">
      <button className="back-btn" onClick={() => navigate('/')}>← Back</button>
      
      <div className="info-banner">
        <div className="info-icon" style={{ background: 'var(--green-bg)' }}>🖼️</div>
        <div>
          <h2>Image / Meme Check</h2>
          <p>Paste an image URL — we'll perform reverse search and check for digital manipulation</p>
        </div>
      </div>

      <div className="input-card">
        <input 
          id="image-input" 
          type="url" 
          placeholder="https://example.com/image.jpg" 
          value={url} 
          onChange={e => setUrl(e.target.value)} 
        />
        <div className="input-actions">
          <span className="char-count" />
          <button 
            id="image-analyze-btn" 
            className="analyze-btn" 
            style={{ background: 'var(--green)' }}
            onClick={analyze} 
            disabled={loading || !url.trim()}
          >
            {loading ? 'Analyzing Image...' : '🖼️ Verify Image'}
          </button>
        </div>
      </div>

      <div className="examples-label">TEST IMAGES</div>
      <div className="example-card" onClick={() => setUrl('https://tvkparty.org/assets/flag_v2.jpg')}>
        <span className="ex-text">TVK Party Flag (Maroon & Yellow)</span>
        <span className="ex-tag" style={{ color: 'var(--green)', background: 'var(--green-bg)' }}>✅ Real</span>
      </div>
      <div className="example-card" onClick={() => setUrl('https://social.media/fake_vijay_speech.jpg')}>
        <span className="ex-text">AI Generated Campaign Image</span>
        <span className="ex-tag" style={{ color: 'var(--red)', background: 'var(--red-bg)' }}>❌ Deepfake</span>
      </div>

      {error && <div className="error-card">⚠️ {error}</div>}
      
      {loading && (
        <div className="loading-state">
          <div className="loader-ring" style={{ borderTopColor: 'var(--green)' }} />
          <p>Scanning image for manipulations & text...</p>
        </div>
      )}

      <div className="steps-section">
        <div className="section-label">HOW IT WORKS</div>
        {steps.map((s, i) => (
          <div key={i} className="step-item">
            <div className="step-num" style={{ background: 'var(--green-bg)', color: 'var(--green)' }}>{i + 1}</div>
            <span>{s}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
