import React from 'react';
import SafetyBanner from './SafetyBanner';
import Disclaimer from './Disclaimer';

export default function DisplayOutput({ result }) {
  if (!result) return null;

  const { answer_text, citations } = result;

  return (
    <section className="output-section">
      <SafetyBanner />
      
      <div className="response-content">
        <h3>Response</h3>
        <p style={{ whiteSpace: 'pre-wrap' }}>{answer_text}</p>
      </div>

      {citations && citations.length > 0 && (
        <div className="citations-box">
          <h4>Sources & Citations</h4>
          <ul>
            {citations.map((cite, index) => (
              <li key={index}>
                <a href={cite.url} target="_blank" rel="noopener noreferrer">
                  {cite.title}
                </a> 
                <span> — {cite.source}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Disclaimer />
    </section>
  );
}