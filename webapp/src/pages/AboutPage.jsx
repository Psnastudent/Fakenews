import React from 'react';

export default function AboutPage() {
  return (
    <div className="section-light" style={{ minHeight: '100vh', paddingTop: '160px' }}>
      <div className="container" style={{ maxWidth: '800px' }}>
        
        <div className="fade-in">
          <span className="eyebrow">Our Mission</span>
          <h2>Deterministic truth in the generative era.</h2>
        </div>

        <div className="slide-up" style={{ marginTop: '48px', color: 'var(--text-secondary)', fontSize: '1.1rem', lineHeight: '1.8' }}>
          <p style={{ marginBottom: '24px' }}>
            FactGuard was built to solve the defining problem of the next decade: the collapse of digital trust.
            As generative models make it trivial to produce infinite synthetic media, traditional moderation 
            fails to scale.
          </p>
          <p style={{ marginBottom: '24px' }}>
            By combining deep convolutional neural networks (CNNs) for visual forensic analysis, and 
            transformer-based Natural Language Processing (NLP) cross-referencing against 44,000+ known 
            dataset facts, FactGuard restores the information supply chain.
          </p>
          <p>
            Our architecture is built on FastAPI, PyTorch, and React, creating an industrial-grade pipeline 
            capable of processing content in milliseconds.
          </p>
        </div>

      </div>
    </div>
  );
}
