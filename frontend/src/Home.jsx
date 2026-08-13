import React, { useEffect, useState } from 'react';

const Home = () => {
  const [products, setProducts] = useState([]);
  const [user, setUser] = useState({ username: 'Guest' });

  // AWS Backend API se Products Fetch karne ke liye
  useEffect(() => {
    // Apne AWS EC2 / Backend ka URL yahan dein (e.g. http://13.xx.xx.xx/api/products/)
    fetch('http://16.16.110.33/api/products/')
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  return (
    <div>
      {/* Dynamic CSS Styling */}
      <style>{`
        .product-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 25px;
          padding: 40px;
          max-width: 1200px;
          margin: auto;
        }

        .product-card {
          background: #ffffff;
          border: 1px solid #eee;
          border-radius: 12px;
          padding: 15px;
          transition: all 0.3s ease;
          text-align: center;
          box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        }

        .product-card:hover {
          box-shadow: 0 10px 20px rgba(0,0,0,0.15);
          transform: translateY(-5px);
        }

        .product-card img {
          width: 100%;
          height: 300px;
          object-fit: cover;
          display: block;
          border-radius: 10px;
          margin: 0 auto 15px auto;
        }

        .product-card h3 {
          font-size: 18px;
          margin: 10px 0;
          color: #333;
        }

        .product-card p {
          font-size: 16px;
          font-weight: bold;
          color: #e67e22;
          margin-bottom: 15px;
        }

        .add-to-cart-btn {
          border: 2px solid #333;
          color: #333;
          padding: 10px 20px;
          border-radius: 5px;
          text-decoration: none;
          font-weight: bold;
          display: inline-block;
          transition: 0.3s;
          cursor: pointer;
        }

        .add-to-cart-btn:hover {
          background-color: #333;
          color: white;
        }

        .nav-container {
          display: flex;
          flex-wrap: wrap;
          justify-content: space-between;
          align-items: center;
          padding: 10px 20px;
          background: #f8f9fa;
          border-bottom: 2px solid #ddd;
          gap: 10px;
        }

        .nav-links {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          align-items: center;
        }

        .btn-upgrade {
          background: linear-gradient(45deg, #8e2de2, #4a00e0);
          color: white !important;
          padding: 8px 20px;
          border-radius: 50px;
          font-weight: 600;
          text-decoration: none;
        }

        .btn-cart {
          background-color: #0ea5e9;
          color: white;
          padding: 8px 16px;
          border-radius: 6px;
          text-decoration: none;
        }

        .btn-logout {
          background-color: #ef4444;
          color: white;
          padding: 8px 16px;
          border-radius: 6px;
          border: none;
          cursor: pointer;
        }
      `}</style>

      {/* Navbar */}
      <nav className="nav-container">
        <div>Welcome, <strong>{user.username}</strong></div>
        
        <div className="nav-links">
          <a className="btn-upgrade" href="/pricing.html">Upgrade Plan</a>
          <a className="btn-cart" href="/view_cart.html">View Cart</a>
          <button className="btn-logout" onClick={() => alert("Logged out")}>Logout</button>
        </div>
      </nav>

      <h2 style={{ textAlign: 'center', marginTop: '40px', color: '#0f172a' }}>
        Our Exclusive Collection
      </h2>

      {/* Products Display Grid */}
      <div className="product-grid">
        {products.length > 0 ? (
          products.map((product) => (
            <div className="product-card" key={product.id}>
              {product.image && (
                <img src={product.image} alt={product.name} />
              )}
              <h3>{product.name}</h3>
              <p>Price: {product.price} PKR</p>
              
              <button 
                className="add-to-cart-btn" 
                onClick={() => alert(`Added ${product.name} to cart`)}
              >
                🛒 Add to Cart
              </button>
            </div>
          ))
        ) : (
          <p style={{ gridColumn: '1/-1', textAlign: 'center' }}>
            Loading products or backend not connected...
          </p>
        )}
      </div>
    </div>
  );
};

export default Home;