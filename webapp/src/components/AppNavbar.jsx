import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

const links = [
  { to: '/', label: 'Technology', end: true },
  { to: '/analyze', label: 'Analyze' },
  { to: '/dashboard', label: 'Command Center' },
];

export default function AppNavbar() {
  const [scrolled, setScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <nav className="navbar" style={{ borderBottomColor: scrolled ? 'var(--border-light)' : 'transparent' }}>
      <div className="container">
        <div className="nav-inner">
          {/* Logo */}
          <NavLink to="/" className="nav-logo">
            <div className="nav-logo-mark" />
            FACTGUARD
          </NavLink>

          {/* Desktop Links (Pill shape like Shinkei) */}
          <div className="nav-links">
            {links.map(l => (
              <NavLink
                key={l.to}
                to={l.to}
                end={l.end}
                className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
              >
                {l.label}
              </NavLink>
            ))}
          </div>

          {/* Desktop CTA */}
          <button className="btn-amber" onClick={() => navigate('/analyze')}>
            <span>Launch Engine</span>
            <svg width="11" height="8" viewBox="0 0 11 8" fill="none"><path d="M0.5 3.18188C0.223858 3.18188 0 3.40574 0 3.68188C0 3.95803 0.223858 4.18188 0.5 4.18188V3.68188V3.18188ZM10.8536 4.03544C11.0488 3.84018 11.0488 3.52359 10.8536 3.32833L7.67157 0.146351C7.47631 -0.0489113 7.15973 -0.0489113 6.96447 0.146351C6.7692 0.341613 6.7692 0.658195 6.96447 0.853458L9.79289 3.68188L6.96447 6.51031C6.7692 6.70557 6.7692 7.02216 6.96447 7.21742C7.15973 7.41268 7.47631 7.41268 7.67157 7.21742L10.8536 4.03544ZM0.5 3.68188V4.18188H10.5V3.68188V3.18188H0.5V3.68188Z" fill="currentColor"/></svg>
          </button>
        </div>
      </div>
    </nav>
  );
}
