import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API = '/api/v1/check';
const steps = ['Scrape article content from URL', 'Extract factual claims using NLP', 'Classify claims using AI model', 'Cross-check with trusted sources', 'Generate verdict & truth score'];

export default function UrlCheckPage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const analyze = async () => {
    if (!url.trim()) return;
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/url`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: url.trim(), content_type: 'url' }),
      });
      if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || `Server error (${res.status})`); }
      const data = await res.json();
      const history = JSON.parse(localStorage.getItem('factcheck_history') || '[]');
      history.unshift({ text: url.trim().slice(0, 200), verdict: data.verdict, score: data.truth_score, date: new Date().toISOString(), type: 'url' });
      localStorage.setItem('factcheck_history', JSON.stringify(history.slice(0, 50)));
      navigate('/result', { state: { result: data } });
    } catch (e) { setError(e.message || 'Failed to analyze.'); }
    finally { setLoading(false); }
  };

  return (
    <div className="sub-page container page-enter">
      <button className="back-btn" onClick={() => navigate('/')}>← Back</button>
      <div className="info-banner">
        <div className="info-icon" style={{ background: 'var(--cyan-bg)' }}>🔗</div>
        <div><h2>URL / Article Check</h2><p>Paste a news article URL — we'll scrape and verify the content</p></div>
      </div>
      <div className="input-card">
        <input id="url-input" type="url" placeholder="https://example.com/news-article" value={url} onChange={e => setUrl(e.target.value)} />
        <div className="input-actions">
          <span className="char-count" />
          <button id="url-analyze-btn" className="analyze-btn cyan" onClick={analyze} disabled={loading || !url.trim()}>
            {loading ? 'Scraping & Analyzing...' : '✓ Verify Article'}
          </button>
        </div>
      </div>
      {error && <div className="error-card">⚠️ {error}</div>}
      {loading && <div className="loading-state"><div className="loader-ring" /><p>Scraping article & running AI analysis...</p></div>}
      <div className="steps-section">
        <div className="section-label">HOW IT WORKS</div>
        {steps.map((s, i) => (
          <div key={i} className="step-item">
            <div className="step-num" style={{ background: 'var(--cyan-bg)', color: 'var(--cyan)' }}>{i + 1}</div>
            <span>{s}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
