import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API = '/api/v1/check';
const steps = [
  'Extract video metadata & description',
  'Retrieve / Generate transcript using AI',
  'Analyze visual elements & face consistency',
  'Cross-check claims with trusted sources',
  'Generate verdict & truth score'
];

export default function VideoCheckPage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const analyze = async () => {
    if (!url.trim()) return;
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/video`, {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: url.trim(), content_type: 'video' }),
      });
      if (!res.ok) { 
        const e = await res.json().catch(() => ({})); 
        throw new Error(e.detail || `Server error (${res.status})`); 
      }
      const data = await res.json();
      
      // Save to local history
      const history = JSON.parse(localStorage.getItem('factcheck_history') || '[]');
      history.unshift({ 
        text: `Video: ${url.trim().slice(0, 50)}...`, 
        verdict: data.verdict, 
        score: data.truth_score, 
        date: new Date().toISOString(), 
        type: 'video' 
      });
      localStorage.setItem('factcheck_history', JSON.stringify(history.slice(0, 50)));
      
      navigate('/result', { state: { result: data } });
    } catch (e) { 
      setError(e.message || 'Failed to analyze video.'); 
    } finally { 
      setLoading(false); 
    }
  };

  return (
    <div className="sub-page container page-enter">
      <button className="back-btn" onClick={() => navigate('/')}>← Back</button>
      
      <div className="info-banner">
        <div className="info-icon" style={{ background: 'var(--red-bg)' }}>🎬</div>
        <div>
          <h2>YouTube / Video Check</h2>
          <p>Paste a YouTube or video URL — we'll analyze the content, transcript, and visual consistency</p>
        </div>
      </div>

      <div className="input-card">
        <input 
          id="video-input" 
          type="url" 
          placeholder="https://www.youtube.com/watch?v=..." 
          value={url} 
          onChange={e => setUrl(e.target.value)} 
        />
        <div className="input-actions">
          <span className="char-count" />
          <button 
            id="video-analyze-btn" 
            className="analyze-btn" 
            style={{ background: 'var(--red)' }}
            onClick={analyze} 
            disabled={loading || !url.trim()}
          >
            {loading ? 'Processing Video...' : '🎬 Verify Video'}
          </button>
        </div>
      </div>

      <div className="examples-label">TEST VIDEOS</div>
      <div className="example-card" onClick={() => setUrl('https://www.youtube.com/watch?v=tvk_official_anthem')}>
        <span className="ex-text">TVK Official Party Anthem</span>
        <span className="ex-tag" style={{ color: 'var(--green)', background: 'var(--green-bg)' }}>✅ Official</span>
      </div>
      <div className="example-card" onClick={() => setUrl('https://www.youtube.com/watch?v=vijay_deepfake_speech')}>
        <span className="ex-text">Deepfake: Vijay Speech at Rally</span>
        <span className="ex-tag" style={{ color: 'var(--red)', background: 'var(--red-bg)' }}>❌ Deepfake</span>
      </div>

      {error && <div className="error-card">⚠️ {error}</div>}
      
      {loading && (
        <div className="loading-state">
          <div className="loader-ring" style={{ borderTopColor: 'var(--red)' }} />
          <p>Transcribing & analyzing video frames...</p>
        </div>
      )}

      <div className="steps-section">
        <div className="section-label">HOW IT WORKS</div>
        {steps.map((s, i) => (
          <div key={i} className="step-item">
            <div className="step-num" style={{ background: 'var(--red-bg)', color: 'var(--red)' }}>{i + 1}</div>
            <span>{s}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
