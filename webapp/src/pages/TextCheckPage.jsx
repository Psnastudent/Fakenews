import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API = '/api/v1/check';

const examples = [
  { text: 'Tamil Nadu recorded 84.69% voter turnout in the 2026 Assembly elections', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'Tamilaga Vettri Kazhagam (TVK) was allotted the "Whistle" symbol for the 2026 elections', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'The TVK party flag features maroon and yellow colors', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'Axis My India exit poll projects 120 seats for Vijay\'s TVK', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'The majority mark for the Tamil Nadu Assembly is 118 seats', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'The counting of votes for the 2026 TN elections is on May 4th', tag: '✅ Verified', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'The Pentagon signed AI agreements with OpenAI and SpaceX for classified networks', tag: '✅ Tech News', tagColor: 'var(--accent)', tagBg: 'var(--accent-bg)' },
  { text: 'Norway\'s 1X aims to build 100,000 humanoid robots by 2027', tag: '✅ Robotics', tagColor: 'var(--accent)', tagBg: 'var(--accent-bg)' },
  { text: 'AMA announced a policy to protect doctors from AI deepfakes', tag: '✅ Health', tagColor: 'var(--green)', tagBg: 'var(--green-bg)' },
  { text: 'NASA confirmed Earth will be dark for 6 days', tag: '❌ Known Fake', tagColor: 'var(--red)', tagBg: 'var(--red-bg)' },
];

export default function TextCheckPage() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/text`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: text.trim(), content_type: 'text' }),
      });
      if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || `Server error (${res.status})`); }
      const data = await res.json();
      // Save to history
      const history = JSON.parse(localStorage.getItem('factcheck_history') || '[]');
      history.unshift({ text: text.trim().slice(0, 200), verdict: data.verdict, score: data.truth_score, date: new Date().toISOString(), type: 'text' });
      localStorage.setItem('factcheck_history', JSON.stringify(history.slice(0, 50)));
      navigate('/result', { state: { result: data } });
    } catch (e) { setError(e.message || 'Failed to analyze. Is the backend running?'); }
    finally { setLoading(false); }
  };

  return (
    <div className="sub-page container page-enter">
      <button className="back-btn" onClick={() => navigate('/')}>← Back</button>

      <div className="info-banner">
        <div className="info-icon" style={{ background: 'var(--accent-bg)' }}>📝</div>
        <div>
          <h2>Text Fact Check</h2>
          <p>Enter a claim, news headline, or any text to verify its accuracy</p>
        </div>
      </div>

      <div className="input-card">
        <textarea
          id="text-input"
          placeholder='Paste or type a claim to fact-check...'
          value={text}
          onChange={e => setText(e.target.value)}
          maxLength={10000}
        />
        <div className="input-actions">
          <span className="char-count">{text.length.toLocaleString()} / 10,000</span>
          <button id="analyze-btn" className="analyze-btn" onClick={analyze} disabled={loading || !text.trim()}>
            {loading ? 'Analyzing...' : '🔍 Analyze'}
          </button>
        </div>
      </div>

      {error && <div className="error-card">⚠️ {error}</div>}
      {loading && <div className="loading-state"><div className="loader-ring" /><p>Running AI analysis pipeline...</p></div>}

      <div className="examples-label">EXAMPLE CLAIMS — TAP TO TRY</div>
      {examples.map((ex, i) => (
        <div key={i} className="example-card" onClick={() => setText(ex.text)}>
          <span className="ex-text">{ex.text}</span>
          <span className="ex-tag" style={{ color: ex.tagColor, background: ex.tagBg }}>{ex.tag}</span>
        </div>
      ))}
    </div>
  );
}
