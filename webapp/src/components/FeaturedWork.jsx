import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const projects = [
  { id: 1, title: 'WKNDHRS', tags: ['Agency Website', 'Portfolio', 'Animations'], img: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&q=80&w=1200' },
  { id: 2, title: 'BodyArmor', tags: ['Marketing Site', 'Sports'], img: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&q=80&w=1200' },
  { id: 3, title: 'Annnimate', tags: ['Web App', 'SaaS', 'Animations'], img: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1200' },
  { id: 4, title: 'Fitgreenmind', tags: ['Marketing Site', 'Animations'], img: 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?auto=format&fit=crop&q=80&w=1200' }
];

export default function FeaturedWork() {
  const sectionRef = useRef(null);

  useEffect(() => {
    // Parallax effect on images as you scroll down
    const ctx = gsap.context(() => {
      const cards = gsap.utils.toArray('.project-card');
      
      cards.forEach((card) => {
        const img = card.querySelector('img');
        
        gsap.fromTo(img, 
          { yPercent: -20, scale: 1.1 },
          {
            yPercent: 20,
            scale: 1,
            ease: "none",
            scrollTrigger: {
              trigger: card,
              start: "top bottom",
              end: "bottom top",
              scrub: true
            }
          }
        );
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      id="work"
      ref={sectionRef} 
      style={{
        padding: '120px 0',
        backgroundColor: '#fff', // Light theme for this section
        color: '#000'
      }}
      className="grid-container"
    >
      <div style={{ marginBottom: '80px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <h2 style={{ fontSize: 'clamp(2rem, 5vw, 4rem)', lineHeight: 1, letterSpacing: '-0.02em', fontWeight: 600 }}>
          Featured Work
        </h2>
        <p style={{ maxWidth: '400px', fontSize: '1.1rem', color: '#555', fontFamily: 'var(--font-mono)' }}>
          We build websites where every scroll, every transition, and every interaction feels intentional.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '40px' }}>
        {projects.map((project, index) => (
          <div 
            key={project.id} 
            className="project-card"
            style={{
              marginTop: index % 2 !== 0 ? '120px' : '0', // Stagger grid
              cursor: 'none'
            }}
          >
            <div style={{ 
              width: '100%', 
              paddingBottom: '120%', 
              position: 'relative', 
              overflow: 'hidden',
              backgroundColor: '#eee'
            }}
            onMouseEnter={(e) => {
              gsap.to(e.currentTarget.querySelector('.overlay'), { opacity: 0.2, duration: 0.3 });
              gsap.to(e.currentTarget.querySelector('img'), { scale: 1.05, filter: 'grayscale(0%)', duration: 0.5 });
            }}
            onMouseLeave={(e) => {
              gsap.to(e.currentTarget.querySelector('.overlay'), { opacity: 0, duration: 0.3 });
              gsap.to(e.currentTarget.querySelector('img'), { scale: 1, filter: 'grayscale(100%)', duration: 0.5 });
            }}
            >
              <img 
                src={project.img} 
                alt={project.title}
                style={{
                  position: 'absolute',
                  top: '-10%',
                  left: 0,
                  width: '100%',
                  height: '120%',
                  objectFit: 'cover',
                  filter: 'grayscale(100%)',
                  transition: 'filter 0.5s'
                }}
              />
              <div 
                className="overlay"
                style={{
                  position: 'absolute',
                  inset: 0,
                  backgroundColor: 'var(--brand)',
                  opacity: 0,
                  transition: 'opacity 0.3s'
                }}
              />
            </div>
            
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3 style={{ fontSize: '1.5rem', fontWeight: 600 }}>{project.title}</h3>
              <div style={{ display: 'flex', gap: '8px' }}>
                {project.tags.map(tag => (
                  <span key={tag} style={{ 
                    fontSize: '0.8rem', 
                    padding: '4px 12px', 
                    borderRadius: '20px', 
                    border: '1px solid #ddd',
                    fontFamily: 'var(--font-mono)'
                  }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
