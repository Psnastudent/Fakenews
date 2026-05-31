import React, { useEffect, useState } from 'react';
import { getHistory } from '../services/api';

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then(data => {
        setHistory(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="section-light" style={{ minHeight: '100vh', paddingTop: '160px' }}>
      <div className="container">
        
        <div style={{ marginBottom: '64px' }} className="fade-in">
          <span className="eyebrow">Data Logs</span>
          <h2>Analysis History</h2>
          <p style={{ marginTop: '24px', color: 'var(--text-secondary)' }}>
            Immutable ledger of recent neural detections.
          </p>
        </div>

        <div className="result-box slide-up">
          <div style={{ width: '100%', overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-light)', fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '16px' }}>Date</th>
                  <th style={{ padding: '16px' }}>Type</th>
                  <th style={{ padding: '16px' }}>Content</th>
                  <th style={{ padding: '16px' }}>Verdict</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan="4" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      <div className="spinner" style={{ borderTopColor: 'var(--shinkei-amber)', width: '24px', height: '24px', borderWidth: '3px' }} />
                    </td>
                  </tr>
                ) : history.length === 0 ? (
                  <tr>
                    <td colSpan="4" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      No analysis logs found. Run a scan to generate history.
                    </td>
                  </tr>
                ) : (
                  history.map((item) => (
                    <tr key={item.id} style={{ borderBottom: '1px solid var(--border-light)' }}>
                      <td style={{ padding: '16px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{item.date}</td>
                      <td style={{ padding: '16px' }}>
                        <span className="eyebrow" style={{ margin: 0, fontSize: '0.7rem' }}>{item.type}</span>
                      </td>
                      <td style={{ padding: '16px', color: 'var(--text-primary)', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {item.content}
                      </td>
                      <td style={{ padding: '16px' }}>
                        <div className={`status-badge ${item.verdict === 'FAKE' ? 'status-fake' : 'status-real'}`}>
                          <div className="status-dot" />
                          {item.verdict}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}
