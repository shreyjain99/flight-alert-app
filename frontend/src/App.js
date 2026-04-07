import React, { useState } from "react";
import "./App.css";

function App() {
  // Form field state
  const [form, setForm] = useState({
    from: "",
    to: "",
    date: "",
    email: "",
    targetPrice: "",
  });

  // UI state
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [currentPrice, setCurrentPrice] = useState(null); // real price from backend

  // Update form fields as user types
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Basic validation before submit
  const validate = () => {
    if (!form.from || !form.to || !form.date || !form.email) {
      return "Please fill in all required fields.";
    }
    if (form.from.trim().toUpperCase() === form.to.trim().toUpperCase()) {
      return "Source and destination cannot be the same.";
    }
    if (!form.email.includes("@")) {
      return "Please enter a valid email address.";
    }
    return "";
  };

  // Handle form submission — calls real backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from_airport: form.from.toUpperCase(),
          to_airport:   form.to.toUpperCase(),
          travel_date:  form.date,
          email:        form.email,
          target_price: form.targetPrice ? parseFloat(form.targetPrice) : null,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Success — save the real price returned by backend
        setCurrentPrice(data.price);
        setSubmitted(true);
      } else {
        // Backend returned a 4xx/5xx with an error detail
        setError(data.detail || "Something went wrong. Please try again.");
      }
    } catch (err) {
      // Network error — backend not running or unreachable
      setError("Could not connect to server. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // Reset to track another flight
  const handleReset = () => {
    setSubmitted(false);
    setCurrentPrice(null);
    setForm({ from: "", to: "", date: "", email: "", targetPrice: "" });
  };

  // --- SUCCESS SCREEN ---
  if (submitted) {
    return (
      <div className="container">
        <div className="card success-card">
          <div className="success-icon">✓</div>
          <h2>Tracking Started!</h2>
          <p>
            We'll monitor <strong>{form.from.toUpperCase()}</strong> →{" "}
            <strong>{form.to.toUpperCase()}</strong> on{" "}
            <strong>{form.date}</strong>.
          </p>
          <p>
            Alerts will be sent to <strong>{form.email}</strong>.
          </p>
          {currentPrice && (
            <p>
              Current price: <strong>${currentPrice.toFixed(2)}</strong>
            </p>
          )}
          {form.targetPrice && (
            <p>
              You'll be notified when the price drops below{" "}
              <strong>${form.targetPrice}</strong>.
            </p>
          )}
          <button className="btn" onClick={handleReset}>
            Track Another Flight
          </button>
        </div>
      </div>
    );
  }

  // --- MAIN FORM ---
  return (
    <div className="container">
      <div className="card">

        {/* Header */}
        <div className="header">
          <h1>✈ Flight Price Tracker</h1>
          <p>Enter your flight details and we'll alert you when prices change.</p>
        </div>

        <form onSubmit={handleSubmit}>

          {/* From / To row */}
          <div className="row">
            <div className="field">
              <label>From <span className="required">*</span></label>
              <input
                type="text"
                name="from"
                placeholder="e.g. JFK"
                value={form.from}
                onChange={handleChange}
                maxLength={3}
              />
              <small>3-letter airport code</small>
            </div>

            <div className="arrow">→</div>

            <div className="field">
              <label>To <span className="required">*</span></label>
              <input
                type="text"
                name="to"
                placeholder="e.g. LAX"
                value={form.to}
                onChange={handleChange}
                maxLength={3}
              />
              <small>3-letter airport code</small>
            </div>
          </div>

          {/* Travel Date */}
          <div className="field">
            <label>Travel Date <span className="required">*</span></label>
            <input
              type="date"
              name="date"
              value={form.date}
              onChange={handleChange}
              min={new Date().toISOString().split("T")[0]}
            />
          </div>

          {/* Email */}
          <div className="field">
            <label>Email Address <span className="required">*</span></label>
            <input
              type="email"
              name="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={handleChange}
            />
            <small>We'll send price alerts here</small>
          </div>

          {/* Target Price (optional) */}
          <div className="field">
            <label>Target Price <span className="optional">(optional)</span></label>
            <div className="price-input">
              <span className="currency">$</span>
              <input
                type="number"
                name="targetPrice"
                placeholder="e.g. 300"
                value={form.targetPrice}
                onChange={handleChange}
                min={1}
              />
            </div>
            <small>Alert me when price drops below this</small>
          </div>

          {/* Validation error */}
          {error && <div className="error">{error}</div>}

          {/* Submit */}
          <button type="submit" className="btn" disabled={loading}>
            {loading ? "Starting tracker..." : "Start Tracking"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
