import React from 'react';
import { Routes, Route } from 'react-router-dom';
import './index.css';
import AppNavbar from './components/AppNavbar.jsx';
import AppFooter from './components/AppFooter.jsx';
import HomePage from './pages/HomePage.jsx';
import AnalyzePage from './pages/AnalyzePage.jsx';
import DashboardPage from './pages/DashboardPage.jsx';
import ResultPage from './pages/ResultPage.jsx';
import HistoryPage from './pages/HistoryPage.jsx';
import AboutPage from './pages/AboutPage.jsx';

export default function App() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppNavbar />
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/"          element={<HomePage />} />
          <Route path="/analyze"   element={<AnalyzePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/result"    element={<ResultPage />} />
          <Route path="/history"   element={<HistoryPage />} />
          <Route path="/about"     element={<AboutPage />} />
        </Routes>
      </main>
      <AppFooter />
    </div>
  );
}
