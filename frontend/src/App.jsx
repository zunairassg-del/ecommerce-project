import Home from './Home';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        {/* Main Home Page */}
        <Route path="/" element={<Home />} />

        {/* Cart Page Example */}
        <Route path="/cart" element={
          <div style={{ padding: '20px', textAlign: 'center' }}>
            <h1>Shopping Cart</h1>
            <p>Yahan aapka cart items show honge.</p>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;