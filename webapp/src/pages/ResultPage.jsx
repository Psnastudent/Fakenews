import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { generatePDFReport } from '../services/pdf';

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [downloading, setDownloading] = useState(false);
  
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="section-light" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <h2>No Data Found</h2>
          <br/>
          <button className="btn-amber" onClick={() => navigate('/analyze')}>Return</button>
        </div>
      </div>
    );
  }

  const v = result.verdict?.toLowerCase() || 'unverified';
  const isFake = v === 'fake' || v === 'misleading';
  const isReal = v === 'real' || v === 'partially_true';

  const handleDownload = async () => {
    setDownloading(true);
    await generatePDFReport(result);
    setDownloading(false);
  };

  return (
    <div className="section-gray" style={{ minHeight: '100vh', paddingTop: '160px' }}>
      <div className="container">
        
        <div style={{ marginBottom: '64px' }} className="fade-in">
          <span className="eyebrow">Detection Results</span>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '24px' }}>
            <h2>Analysis Complete</h2>
            <div style={{ display: 'flex', gap: '16px' }}>
              <button className="btn-amber" onClick={() => navigate('/analyze')}>Analyze Another</button>
              <button className="btn-black" onClick={handleDownload} disabled={downloading}>
                {downloading ? 'Generating...' : 'Download Report'}
              </button>
            </div>
          </div>
        </div>

        <div className="result-box slide-up" style={{ borderLeft: `8px solid ${isFake ? 'var(--red)' : isReal ? 'var(--green)' : 'var(--amber)'}` }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <div className={`status-badge ${isFake ? 'status-fake' : isReal ? 'status-real' : 'status-amber'}`}>
              <div className="status-dot" />
              {isFake ? 'Threat Detected' : isReal ? 'Verified Real' : 'Unverified'}
            </div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.5rem', fontWeight: 700 }}>
              {result.truth_score}% <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Truth Score</span>
            </div>
          </div>
          
          <h3 style={{ marginBottom: '16px', fontSize: '1.5rem' }}>Engine Explanation</h3>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>{result.explanation}</p>
        </div>

        <div className="feature-grid slide-up" style={{ alignItems: 'flex-start' }}>
          
          <div className="result-box">
            <h3 style={{ marginBottom: '24px', fontSize: '1.25rem' }}>Claim Breakdown</h3>
            {result.claims?.length > 0 ? result.claims.map((claim, idx) => (
              <div key={idx} style={{ marginBottom: '24px', paddingBottom: '24px', borderBottom: '1px solid var(--border-light)' }}>
                <div style={{ display: 'flex', gap: '16px' }}>
                  <div style={{ fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>0{idx + 1}</div>
                  <div>
                    <div style={{ marginBottom: '8px', fontWeight: 500 }}>"{claim.claim}"</div>
                    <div className="eyebrow" style={{ marginBottom: 0 }}>
                      Conf: {(claim.confidence * 100).toFixed(1)}% • Rating: {claim.verdict}
                    </div>
                  </div>
                </div>
              </div>
            )) : <p style={{ color: 'var(--text-muted)' }}>No specific claims extracted.</p>}
          </div>

          <div className="result-box">
            <h3 style={{ marginBottom: '24px', fontSize: '1.25rem' }}>Cross-Reference Data</h3>
            {result.sources?.length > 0 ? result.sources.map((src, idx) => (
              <div key={idx} style={{ marginBottom: '24px', paddingBottom: '24px', borderBottom: '1px solid var(--border-light)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <a href={src.url} target="_blank" rel="noreferrer" style={{ fontWeight: 500, color: 'var(--text-primary)' }}>
                    {src.name}
                  </a>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    {src.trust_score ? `${(src.trust_score * 100).toFixed(0)}% Trust` : src.rating || 'REF'}
                  </span>
                </div>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{src.snippet}</p>
              </div>
            )) : <p style={{ color: 'var(--text-muted)' }}>No external sources matched.</p>}
            
            {isFake && result.correct_info && (
              <div style={{ marginTop: '32px', padding: '24px', background: '#fff8f5', border: '1px solid var(--shinkei-amber)', borderRadius: '8px' }}>
                <h4 style={{ color: 'var(--shinkei-amber)', marginBottom: '12px', fontSize: '1rem' }}>Correct Information</h4>
                <p style={{ fontSize: '0.95rem' }}>{result.correct_info}</p>
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}
