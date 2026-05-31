import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export default function Navbar() {
  const navRef = useRef(null);
  let lastScrollY = window.scrollY;

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > lastScrollY && window.scrollY > 100) {
        // Scrolling down
        gsap.to(navRef.current, { yPercent: -100, duration: 0.5, ease: 'power3.out' });
      } else {
        // Scrolling up
        gsap.to(navRef.current, { yPercent: 0, duration: 0.5, ease: 'power3.out' });
      }
      lastScrollY = window.scrollY;
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav 
      ref={navRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '80px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 5vw',
        zIndex: 100,
        backdropFilter: 'blur(10px)',
        backgroundColor: 'rgba(15, 10, 21, 0.7)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.05)'
      }}
    >
      <div style={{ fontSize: '1.2rem', fontWeight: 700, letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <div style={{ width: '12px', height: '12px', backgroundColor: 'var(--brand)' }}></div>
        GOOD FELLA
      </div>
      
      <div style={{ display: 'flex', gap: '2rem', fontSize: '0.9rem', fontFamily: 'var(--font-mono)' }}>
        <a href="#work" style={{ color: 'var(--foreground)', opacity: 0.7, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = 1} onMouseLeave={(e) => e.target.style.opacity = 0.7}>Work</a>
        <a href="#pricing" style={{ color: 'var(--foreground)', opacity: 0.7, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = 1} onMouseLeave={(e) => e.target.style.opacity = 0.7}>Pricing</a>
        <a href="#about" style={{ color: 'var(--foreground)', opacity: 0.7, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = 1} onMouseLeave={(e) => e.target.style.opacity = 0.7}>About</a>
      </div>

      <button style={{
        backgroundColor: 'var(--brand)',
        color: '#fff',
        border: 'none',
        padding: '12px 24px',
        fontSize: '0.9rem',
        fontWeight: 600,
        cursor: 'none',
        fontFamily: 'var(--font-sans)',
        transition: 'transform 0.2s'
      }}
      onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
      onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
      >
        Let's work together
      </button>
    </nav>
  );
}
