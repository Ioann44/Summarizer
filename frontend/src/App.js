// App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import PollPage from './pages/PollPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/poll" element={<PollPage />} />
      </Routes>
    </Router>
  );
}

export default App;
