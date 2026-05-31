import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export default function Hero() {
  const container = useRef(null);
  const title1 = useRef(null);
  const title2 = useRef(null);
  const subtext = useRef(null);
  const ctaBtn = useRef(null);
  const ctaLink = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Entrance animation
      const tl = gsap.timeline();
      
      tl.fromTo(
        [title1.current, title2.current], 
        { y: 100, opacity: 0, rotateX: -20 },
        { y: 0, opacity: 1, rotateX: 0, duration: 1, stagger: 0.1, ease: 'power4.out', delay: 0.2 }
      )
      .fromTo(
        subtext.current,
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' },
        '-=0.6'
      )
      .fromTo(
        [ctaBtn.current, ctaLink.current],
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: 'power3.out' },
        '-=0.6'
      );
    }, container);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      ref={container}
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        position: 'relative',
        overflow: 'hidden',
        paddingTop: '80px' // adjust for navbar
      }}
      className="grid-container"
    >
      {/* Background Grid Lines (decorative) */}
      <div style={{
        position: 'absolute',
        top: 0, left: 0, right: 0, bottom: 0,
        pointerEvents: 'none',
        backgroundImage: `
          linear-gradient(to right, var(--grid-color) 1px, transparent 1px),
          linear-gradient(to bottom, var(--grid-color) 1px, transparent 1px)
        `,
        backgroundSize: '4vw 4vw',
        zIndex: 0
      }} />

      <div className="grid-layout" style={{ zIndex: 10, width: '100%' }}>
        <div className="grid-span-7" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <h1 style={{ 
            fontSize: 'clamp(3rem, 7vw, 7rem)', 
            lineHeight: 0.95,
            letterSpacing: '-0.03em',
            perspective: '1000px'
          }}>
            <div style={{ overflow: 'hidden' }}>
              <div ref={title1} style={{ transformOrigin: 'bottom' }}>YOUR FRONTEND TEAM.</div>
            </div>
            <div style={{ overflow: 'hidden', color: 'var(--brand)' }}>
              <div ref={title2} style={{ transformOrigin: 'bottom' }}>ONE MONTHLY FEE.</div>
            </div>
          </h1>

          <p ref={subtext} style={{ 
            fontSize: '1.2rem', 
            maxWidth: '500px',
            lineHeight: 1.5,
            color: 'var(--muted)',
            fontFamily: 'var(--font-mono)'
          }}>
            Good Fella is a frontend development studio that works as your dedicated team. 
            One monthly fee, no contracts, and no hourly tracking.
          </p>

          <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center', marginTop: '1rem' }}>
            <button 
              ref={ctaBtn}
              style={{
                backgroundColor: 'var(--brand)',
                color: '#fff',
                border: 'none',
                padding: '16px 32px',
                fontSize: '1rem',
                fontWeight: 600,
                cursor: 'none',
                transition: 'transform 0.2s',
                fontFamily: 'var(--font-sans)',
              }}
              onMouseEnter={(e) => e.target.style.transform = 'scale(1.05)'}
              onMouseLeave={(e) => e.target.style.transform = 'scale(1)'}
            >
              See our pricing
            </button>
            <a 
              ref={ctaLink}
              href="#work" 
              style={{
                color: 'var(--foreground)',
                fontWeight: 600,
                cursor: 'none',
                textDecoration: 'underline',
                textUnderlineOffset: '4px',
                transition: 'color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.color = 'var(--brand)'}
              onMouseLeave={(e) => e.target.style.color = 'var(--foreground)'}
            >
              View our work
            </a>
          </div>
        </div>

        <div className="grid-span-5" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
          {/* Abstract interactive sphere element */}
          <div style={{
            width: '100%',
            paddingBottom: '100%',
            position: 'relative',
          }}>
             <div 
               ref={(el) => {
                 if (el) {
                   gsap.to(el, {
                     rotate: 360,
                     duration: 40,
                     repeat: -1,
                     ease: 'linear'
                   });
                   gsap.to(el, {
                     scale: 1.05,
                     duration: 4,
                     repeat: -1,
                     yoyo: true,
                     ease: 'sine.inOut'
                   });
                 }
               }}
               style={{
                 position: 'absolute',
                 inset: '10%',
                 borderRadius: '50%',
                 background: 'radial-gradient(circle at 30% 30%, rgba(255,107,74,0.8), rgba(26,10,46,0.9), transparent)',
                 boxShadow: '0 0 80px rgba(255,107,74,0.3)',
                 filter: 'blur(8px)',
               }}
             />
             <div style={{
                 position: 'absolute',
                 inset: '20%',
                 borderRadius: '50%',
                 border: '1px solid rgba(255,107,74,0.4)',
             }}/>
             <div style={{
                 position: 'absolute',
                 inset: '30%',
                 borderRadius: '50%',
                 border: '1px dashed rgba(255,107,74,0.2)',
             }}/>
          </div>
        </div>
      </div>
    </section>
  );
}
