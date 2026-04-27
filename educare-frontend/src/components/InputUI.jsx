import React, { useState } from 'react';

export default function InputUI({ onSubmit, isLoading, userRole }) {
  const [query, setQuery] = useState('');
  
  // Role-specific example queries for quick input
  const examples = userRole === 'doctor' 
    ? [
        { label: "Differential", text: "Provide differential diagnosis for 45yo male with chest pain and elevated D-dimer." },
        { label: "Dosage", text: "Standard titration schedule for Gabapentin in post-herpetic neuralgia." },
        { label: "Guidelines", text: "Summarize 2024 AHA/ACC guidelines for Stage 2 Hypertension." }
      ]
    : [
        { label: "Explanation", text: "Explain what a 'High Cholesterol' result means in simple terms." },
        { label: "Preparation", text: "How should I prepare for my upcoming abdominal ultrasound?" },
        { label: "Symptoms", text: "Is a persistent dry cough a common side effect of Lisinopril?" }
      ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query, userRole); // Sends the role as the 'mode'
    }
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="query-input">
          {userRole === 'doctor' ? 'Clinical Query' : 'Ask a Question'}
        </label>
        <textarea 
          id="query-input"
          className="form-control"
          rows="5"
          placeholder={userRole === 'doctor' ? "Enter clinical data..." : "Ask about your health..."}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
          disabled={isLoading}
        />
      </div>

      <div className="example-chips">
        <small>Quick Queries:</small>
        <div className="chip-container">
          {examples.map((ex) => (
            <button
              key={ex.label}
              type="button"
              onClick={() => setQuery(ex.text)}
              disabled={isLoading}
            >
              {ex.label}
            </button>
          ))}
        </div>
      </div>

      <button type="submit" className={`submit-btn ${userRole}-btn`} disabled={isLoading}>
        {isLoading ? (
          <><div className="spinner"></div><span>Analyzing...</span></>
        ) : (
          userRole === 'doctor' ? 'Run Clinical Analysis' : 'Get Health Info'
        )}
      </button>
    </form>
  );
}