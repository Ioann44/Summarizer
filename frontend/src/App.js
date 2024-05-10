// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PollPage from './pages/PollPage';
import SearchPage from './pages/SearchPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/poll" element={<PollPage />} />
        <Route exact path="/search" element={<SearchPage />} />
      </Routes>
    </Router>
  );
}

export default App;
