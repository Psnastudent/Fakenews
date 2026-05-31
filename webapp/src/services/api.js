const API_BASE = import.meta.env.VITE_API_URL ? `${import.meta.env.VITE_API_URL}/api/v1` : 'http://localhost:8000/api/v1';

export async function analyzeText(text) {
  const res = await fetch(`${API_BASE}/check/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: text, content_type: 'text' })
  });
  if (!res.ok) throw new Error('Failed to analyze text');
  return res.json();
}

export async function analyzeUrl(url) {
  const res = await fetch(`${API_BASE}/check/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url })
  });
  if (!res.ok) throw new Error('Failed to analyze URL');
  return res.json();
}

export async function analyzeMedia(file, type) {
  const formData = new FormData();
  formData.append('file', file);
  
  // Endpoint differs based on image vs video if that's how it's structured,
  // Assuming our API has /check/image and /check/video
  const endpoint = type === 'video' ? '/check/video' : '/check/image';
  
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Failed to analyze media');
  return res.json();
}

export async function getStats() {
  const res = await fetch(`${API_BASE}/check/stats`);
  if (!res.ok) throw new Error('Failed to get stats');
  return res.json();
}

export async function getHistory(limit = 50) {
  const res = await fetch(`${API_BASE}/check/history?limit=${limit}`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}
