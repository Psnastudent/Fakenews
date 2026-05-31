import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const steps = [
  { id: '01', title: 'Subscribe', desc: 'Pick a plan that fits your workload and pay monthly, with no contracts and no minimum commitment. Pause or cancel to the next month whenever you need to.' },
  { id: '02', title: 'Request', desc: 'Send your work through Slack, email, or wherever your team already communicates. We tackle one request at a time in the order you set.' },
  { id: '03', title: 'Ship', desc: 'You\'ll receive deliverables every 2-5 business days with unlimited revisions until you\'re happy.' },
  { id: '04', title: 'Repeat', desc: 'Submit your next request and we keep going the same way. Your backlog shrinks and your product gets better, month after month.' }
];

export default function Process() {
  const containerRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const items = gsap.utils.toArray('.process-step');
      
      items.forEach((item) => {
        gsap.fromTo(item, 
          { opacity: 0, y: 50 },
          {
            opacity: 1, 
            y: 0,
            duration: 0.8,
            ease: "power3.out",
            scrollTrigger: {
              trigger: item,
              start: "top 80%",
            }
          }
        );
      });
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      id="about"
      ref={containerRef}
      style={{ padding: '120px 5vw', backgroundColor: '#f0f0f0', color: '#111' }}
    >
      <div style={{ marginBottom: '80px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '1rem', color: 'var(--brand)' }}>// Process</span>
        <h2 style={{ fontSize: 'clamp(3rem, 6vw, 5rem)', fontWeight: 600, letterSpacing: '-0.02em', lineHeight: 1 }}>How it works</h2>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
        {steps.map((step, i) => (
          <div 
            key={step.id} 
            className="process-step"
            style={{ 
              display: 'flex', 
              borderTop: '1px solid #ccc',
              borderBottom: i === steps.length - 1 ? '1px solid #ccc' : 'none',
              padding: '60px 0',
              alignItems: 'flex-start'
            }}
          >
            <div style={{ flex: '0 0 100px', fontSize: '1.2rem', fontFamily: 'var(--font-mono)', fontWeight: 500 }}>
              {step.id}
            </div>
            
            <div style={{ flex: '1', display: 'grid', gridTemplateColumns: 'minmax(200px, 1fr) 2fr', gap: '2rem' }}>
              <h3 style={{ fontSize: '2.5rem', fontWeight: 600, letterSpacing: '-0.02em', margin: 0 }}>
                {step.title}
              </h3>
              <p style={{ fontSize: '1.2rem', lineHeight: 1.6, color: '#555', maxWidth: '600px', margin: 0, fontFamily: 'var(--font-mono)' }}>
                {step.desc}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
