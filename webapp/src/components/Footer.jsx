import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export default function Footer() {
  const footerRef = useRef(null);
  const textRef = useRef(null);
  const btnRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Parallax text
      gsap.fromTo(textRef.current,
        { y: -100 },
        {
          y: 0,
          ease: "none",
          scrollTrigger: {
            trigger: footerRef.current,
            start: "top bottom",
            end: "bottom bottom",
            scrub: true
          }
        }
      );
    }, footerRef);

    // Magnetic button
    const btn = btnRef.current;
    
    const onMouseMove = (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      
      gsap.to(btn, {
        x: x * 0.3,
        y: y * 0.3,
        duration: 0.6,
        ease: "power3.out"
      });
    };

    const onMouseLeave = () => {
      gsap.to(btn, {
        x: 0,
        y: 0,
        duration: 1,
        ease: "elastic.out(1, 0.3)"
      });
    };

    if (btn) {
      btn.addEventListener('mousemove', onMouseMove);
      btn.addEventListener('mouseleave', onMouseLeave);
    }

    return () => {
      ctx.revert();
      if (btn) {
        btn.removeEventListener('mousemove', onMouseMove);
        btn.removeEventListener('mouseleave', onMouseLeave);
      }
    };
  }, []);

  return (
    <footer 
      id="pricing"
      ref={footerRef}
      style={{
        backgroundColor: 'var(--background)',
        color: 'var(--foreground)',
        padding: '120px 5vw 40px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        minHeight: '80vh',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '2rem' }}>
        <div style={{ maxWidth: '400px' }}>
          <h3 style={{ fontSize: '2rem', marginBottom: '1rem', letterSpacing: '-0.02em' }}>Ready to start?</h3>
          <p style={{ color: 'var(--muted)', fontFamily: 'var(--font-mono)', lineHeight: 1.6 }}>
            Pick a plan that fits your workload and pay monthly, with no contracts and no minimum commitment.
          </p>
        </div>

        <div 
          style={{
            padding: '40px',
            backgroundColor: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '20px',
            minWidth: '350px'
          }}
        >
          <div style={{ fontFamily: 'var(--font-mono)', color: 'var(--brand)', marginBottom: '1rem' }}>Standard Plan</div>
          <div style={{ fontSize: '3rem', fontWeight: 700, letterSpacing: '-0.03em', marginBottom: '2rem' }}>$4,995 <span style={{fontSize: '1rem', color: 'var(--muted)', fontWeight: 400}}>/mo</span></div>
          
          <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 2rem', display: 'flex', flexDirection: 'column', gap: '1rem', fontFamily: 'var(--font-mono)' }}>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: 'var(--brand)' }}>✓</span> One request at a time
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: 'var(--brand)' }}>✓</span> 2-5 days turnaround
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: 'var(--brand)' }}>✓</span> Unlimited revisions
            </li>
            <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={{ color: 'var(--brand)' }}>✓</span> Cancel anytime
            </li>
          </ul>

          <div 
            ref={btnRef}
            style={{ 
              display: 'inline-block',
              padding: '20px 40px',
              backgroundColor: 'var(--foreground)',
              color: 'var(--background)',
              fontWeight: 700,
              fontSize: '1.1rem',
              borderRadius: '50px',
              textAlign: 'center',
              width: '100%',
              cursor: 'none'
            }}
          >
            Subscribe Now
          </div>
        </div>
      </div>

      <div style={{ marginTop: 'auto', paddingTop: '100px' }}>
        <div 
          ref={textRef}
          style={{ 
            fontSize: 'clamp(3rem, 11vw, 20rem)', 
            fontWeight: 700, 
            letterSpacing: '-0.04em',
            lineHeight: 0.8,
            color: 'var(--foreground)',
            textAlign: 'center',
            marginBottom: '40px',
            userSelect: 'none'
          }}
        >
          GOOD FELLA
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--muted)', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px' }}>
          <div>© {new Date().getFullYear()} Good Fella Studio. All rights reserved.</div>
          <div style={{ display: 'flex', gap: '2rem' }}>
            <a href="#" style={{ transition: 'color 0.2s' }} onMouseEnter={(e) => e.target.style.color='var(--brand)'} onMouseLeave={(e) => e.target.style.color='var(--muted)'}>Twitter</a>
            <a href="#" style={{ transition: 'color 0.2s' }} onMouseEnter={(e) => e.target.style.color='var(--brand)'} onMouseLeave={(e) => e.target.style.color='var(--muted)'}>Instagram</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
