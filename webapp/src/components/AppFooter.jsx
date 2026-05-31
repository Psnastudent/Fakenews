import React from 'react';
import { NavLink } from 'react-router-dom';

export default function AppFooter() {
  return (
    <footer style={{ borderTop: '1px solid var(--border-light)', background: 'var(--bg-primary)', padding: '40px 0' }}>
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '24px' }}>
        
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '1.2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div className="nav-logo-mark" style={{ width: '16px', height: '16px' }} />
          FACTGUARD
        </div>

        <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', alignItems: 'center' }}>
          <NavLink to="/" className="nav-link" style={{ fontSize: '0.75rem' }}>Technology</NavLink>
          <NavLink to="/analyze" className="nav-link" style={{ fontSize: '0.75rem' }}>Analyze</NavLink>
          <NavLink to="/dashboard" className="nav-link" style={{ fontSize: '0.75rem' }}>Command Center</NavLink>
          <NavLink to="/history" className="nav-link" style={{ fontSize: '0.75rem' }}>History Logs</NavLink>
          <NavLink to="/about" className="nav-link" style={{ fontSize: '0.75rem' }}>About Us</NavLink>
        </div>

        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          © 2026 FactGuard Neural Systems. Built with FastAPI + React.
        </div>

      </div>
    </footer>
  );
}
