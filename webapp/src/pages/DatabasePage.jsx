import React, { useEffect, useState } from 'react';

export default function DatabasePage() {
  const [facts, setFacts] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [totalFacts, setTotalFacts] = useState(0);
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    fetch('/api/v1/dataset/facts')
      .then(r => r.json())
      .then(data => {
        // API returns { total_facts: N, facts: [...] }
        const factsArr = Array.isArray(data) ? data : (data.facts || []);
        setFacts(factsArr);
        setTotalFacts(data.total_facts || factsArr.length);
        setLoading(false);
      })
      .catch(() => {
        setError('Could not load the fact database. Make sure the backend is running.');
        setLoading(false);
      });
  }, []);

  // Gather unique categories
  const categories = ['all', ...new Set(facts.map(f => f.category || 'general'))];

  const filtered = facts.filter(f => {
    const matchSearch = !search || 
      (f.statement || '').toLowerCase().includes(search.toLowerCase()) ||
      (f.article_source || '').toLowerCase().includes(search.toLowerCase());
    const matchCat = activeCategory === 'all' || (f.category || 'general') === activeCategory;
    return matchSearch && matchCat;
  });

  return (
    <div className="sub-page container page-enter">
      <div className="section-label">FACT DATABASE</div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, marginBottom: 20 }}>
        <h1>Verified Knowledge Base</h1>
        {totalFacts > 0 && (
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 500 }}>
            {totalFacts} facts indexed
          </span>
        )}
      </div>
      
      <input 
        type="text" 
        className="search-input" 
        placeholder="Search verified facts by keyword or source..." 
        value={search}
        onChange={e => setSearch(e.target.value)}
      />

      {categories.length > 1 && (
        <div className="category-pills" style={{ marginBottom: 16 }}>
          {categories.map(cat => (
            <button
              key={cat}
              className={`cat-pill ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>
      )}

      {error && <div className="error-card">⚠️ {error}</div>}

      {loading ? (
        <div className="loading-state"><div className="loader-ring" /><p>Loading facts...</p></div>
      ) : (
        <div className="facts-list">
          {filtered.length > 0 ? (
            <>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 10 }}>
                Showing {filtered.length} of {totalFacts} facts
              </div>
              {filtered.map((fact, i) => (
                <div key={i} className="fact-card">
                  <div className="fact-meta">
                    <span className="fact-badge">VERIFIED</span>
                    {fact.category && (
                      <span style={{ 
                        fontSize: '0.6rem', fontWeight: 700, padding: '2px 8px', borderRadius: 50,
                        background: 'var(--accent-bg)', color: 'var(--accent)'
                      }}>{fact.category.toUpperCase()}</span>
                    )}
                    <span>{fact.article_source}</span>
                    <span>{fact.article_date}</span>
                  </div>
                  <div className="fact-statement">{fact.statement}</div>
                  {fact.article_url && (
                    <a href={fact.article_url} target="_blank" rel="noreferrer" style={{ fontSize: '0.7rem', color: 'var(--accent)' }}>
                      Source: {fact.article_title || fact.article_url}
                    </a>
                  )}
                </div>
              ))}
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-icon">🔍</div>
              <p>{search ? `No facts found matching "${search}"` : 'No verified facts in the database yet.'}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
