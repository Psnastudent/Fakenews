import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div>
      {/* HERO SECTION */}
      <section className="hero">
        <div className="container">
          <h1 className="hero-title fade-in">
            Deterministic fact-checking at <em>industrial scale.</em>
          </h1>
          <p className="hero-desc fade-in" style={{ animationDelay: '0.1s' }}>
            FactGuard uses deep learning and cryptography to build a world where truth thrives, 
            information supply chains are transparent, and digital ecosystems restore societal vitality.
          </p>
          <div className="fade-in" style={{ animationDelay: '0.2s' }}>
            <button className="btn-amber" onClick={() => navigate('/analyze')}>
              <span>Initialize Engine</span>
            </button>
          </div>
        </div>
      </section>

      {/* FEATURE SECTION 1 */}
      <section className="section-light">
        <div className="container">
          <div className="feature-grid">
            <div className="slide-up">
              <span className="eyebrow">The State of Information</span>
              <h2>Most generated content operates unchecked.</h2>
              <p style={{ marginTop: '24px', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
                Digital platforms operate with legacy moderation tools largely unchanged for a decade. 
                While generative models reshape industries, systemic inefficiency means most deepfakes and 
                hallucinations slip through — waste that impacts enterprises, consumers, and the public square.
              </p>
              <br/>
              <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
                We see a vitalistic opportunity. With neural vision and transformers, we can scale artisanal 
                fact-checking practices that have proven quality outputs.
              </p>
            </div>
            <div className="slide-up">
              <img 
                src="https://images.unsplash.com/photo-1585829365295-ab7cd400c167?auto=format&fit=crop&w=1200&q=80" 
                alt="Breaking News digital display" 
                className="feature-img"
              />
            </div>
          </div>
        </div>
      </section>

      {/* FEATURE SECTION 2 (Gray) */}
      <section className="section-gray">
        <div className="container">
          <div className="feature-grid">
            <div className="slide-up" style={{ order: 2 }}>
              <span className="eyebrow">Engineering Meets Logic</span>
              <h2>Software that understands every footprint.</h2>
              <p style={{ marginTop: '24px', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>
                Our integrated computer vision system parses images in milliseconds, with real-time data streams 
                connected to 44k+ datasets. FactGuard extends the lifespan of verified content and eliminates 
                the noise that degrades 70% of digital quality.
              </p>
            </div>
            <div className="slide-up" style={{ order: 1 }}>
              <img 
                src="https://images.unsplash.com/photo-1504711434969-e33886168f5c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" 
                alt="Newspaper print macro" 
                className="feature-img"
              />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
