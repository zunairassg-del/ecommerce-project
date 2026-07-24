import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Home() {
  const [products, setProducts] = useState([]);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Django backend se products aur user data fetch karna
    axios.get('http://10.171.170.208:8000/api/products/')
      .then(response => {
        setProducts(response.data);
      })
      .catch(error => {
        console.error("Error fetching products:", error);
      });

    // User authentication ki API call
    axios.get('http://10.171.170.208:8000/api/user/')
      .then(response => {
        setUser(response.data);
      })
      .catch(error => {
        console.log("User not logged in or guest mode");
      });
  }, []);

  const handleAddToCart = (productId) => {
    alert(`Product ${productId} added to cart!`);
  };

  return (
    <div>
      {/* Navbar */}
      <nav style={{
        display: 'flex', 
        flexWrap: 'wrap', 
        justifyContent: 'space-between',
        alignItems: 'center', 
        padding: '15px 20px', 
        background: '#f8f9fa',
        borderBottom: '2px solid #ddd', 
        gap: '10px'
      }}>
        <div>Welcome, <strong>{user ? user.username : "Guest"}</strong></div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <Link to="/pricing" style={{ 
            padding: '8px 16px', 
            border: 'none', 
            borderRadius: '6px', 
            cursor: 'pointer', 
            fontWeight: '600', 
            textDecoration: 'none', 
            backgroundColor: '#6366f1', 
            color: 'white' 
          }}>
            Upgrade
          </Link>
          <Link to="/cart" style={{ 
            padding: '8px 16px', 
            border: 'none', 
            borderRadius: '6px', 
            cursor: 'pointer', 
            fontWeight: '600', 
            textDecoration: 'none', 
            backgroundColor: '#0ea5e9', 
            color: 'white' 
          }}>
            Cart
          </Link>
          <button onClick={() => alert('Logout clicked')} style={{ 
            padding: '8px 16px', 
            border: 'none', 
            borderRadius: '6px', 
            cursor: 'pointer', 
            fontWeight: '600', 
            backgroundColor: '#ef4444', 
            color: 'white' 
          }}>
            Logout
          </button>
        </div>
      </nav>

      <h2 style={{ textAlign: 'center', marginTop: '40px', color: '#0f172a' }}>Our Exclusive Collection</h2>

      {/* Product Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '20px', 
        padding: '20px', 
        maxWidth: '1200px', 
        margin: 'auto'
      }}>
        {products && products.length > 0 ? (
          products.map((product) => (
            <div key={product.id} style={{
              background: '#fff', 
              border: '1px solid #eee', 
              borderRadius: '12px',
              padding: '15px', 
              textAlign: 'center', 
              boxShadow: '0 4px 10px rgba(0,0,0,0.08)'
            }}>
              {product.image && (
                <img 
                  src={`http://10.171.170.208:8000${product.image}`} 
                  alt={product.name} 
                  style={{ width: '100%', height: '250px', objectFit: 'cover', borderRadius: '10px', marginBottom: '10px' }} 
                />
              )}
              <h3 style={{ fontSize: '18px', margin: '10px 0' }}>{product.name}</h3>
              <p style={{ fontSize: '16px', fontWeight: 'bold', color: '#e67e22', marginBottom: '15px' }}>
                Price: {product.price} PKR
              </p>
              
              <button onClick={() => handleAddToCart(product.id)} style={{
                display: 'block', 
                width: '100%', 
                border: '2px solid #333', 
                background: 'transparent', 
                color: '#333',
                padding: '10px', 
                borderRadius: '5px', 
                fontWeight: 'bold', 
                cursor: 'pointer'
              }}>
                🛒 Add to Cart
              </button>
            </div>
          ))
        ) : (
          <p style={{ textAlign: 'center', gridColumn: '1 / -1', color: '#666' }}>No products available yet or loading...</p>
        )}
      </div>
    </div>
  );
}

export default Home;