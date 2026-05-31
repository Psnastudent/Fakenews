import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getStats } from '../services/api';

export default function DashboardPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getStats().then(setStats).catch(console.error);
  }, []);

  return (
    <div className="section-gray" style={{ minHeight: '100vh', paddingTop: '160px' }}>
      <div className="container">
        
        <div style={{ marginBottom: '64px' }} className="fade-in">
          <span className="eyebrow">Command Center</span>
          <h2>System Operations</h2>
          <p style={{ maxWidth: '600px', marginTop: '24px', color: 'var(--text-secondary)' }}>
            Real-time status of the FactGuard neural engine, deployed models, and verified detection logs.
          </p>
        </div>

        <div className="feature-grid slide-up">
          
          <div className="result-box" onClick={() => navigate('/analyze')} style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
            <h3 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>Live Detection</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Run text, images, or URLs through the neural engine.
            </p>
            <div style={{ color: 'var(--shinkei-amber)', fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>LAUNCH ENGINE →</div>
          </div>

          <div className="result-box" onClick={() => navigate('/history')} style={{ cursor: 'pointer', transition: 'transform 0.2s' }}>
            <h3 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>Analysis History</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
              Review cryptographically signed past detections.
            </p>
            <div style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-mono)', fontSize: '0.9rem' }}>VIEW LOGS →</div>
          </div>

          <div className="result-box">
            <h3 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>Model Weights</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '24px' }}>
              100k Image Model Active<br/>44k Text Model Active
            </p>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div className="status-dot" style={{ color: 'var(--green)' }}/>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--green)' }}>MODELS ONLINE</span>
            </div>
          </div>

          <div className="result-box">
            <h3 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>System Metrics</h3>
            {stats ? (
              <p style={{ color: 'var(--text-secondary)' }}>
                {stats.known_fake_claims} Known Fakes Blocked<br/>
                {stats.total_facts} Facts Verified across {stats.total_articles} Articles.
              </p>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>Loading metrics...</p>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
