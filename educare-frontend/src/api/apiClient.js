export const fetchEduCareQuery = async (queryText, mode) => {
  // Simulate a 1.5-second delay to test the loading state (as per your SMART objectives)
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Mock response for Patient Mode
  if (mode === 'patient') {
    return {
      answer_text: "Based on the symptoms you described, rheumatoid arthritis is an autoimmune condition where your immune system accidentally attacks the lining of your joints. This causes inflammation, which leads to swelling, stiffness, and pain.\n\nTips for day-to-day management:\n- Rest when your joints feel inflamed.\n- Try gentle exercises like swimming.\n- Take prescribed medications regularly.",
      citations: [
        { title: "Rheumatoid Arthritis - Overview", url: "https://www.nhs.uk/conditions/rheumatoid-arthritis/", source: "NHS" },
        { title: "Living with Rheumatoid Arthritis", url: "#", source: "MedQuAD" }
      ]
    };
  }

  // Mock response for Professional Mode
  return {
    answer_text: "Rheumatoid arthritis (RA) is a chronic, systemic inflammatory disorder that primarily affects synovial joints. Pathophysiologically, it is characterized by synovial hyperplasia and the infiltration of inflammatory cells (macrophages, T cells, and B cells) into the synovial sublining.\n\nDiagnostic Criteria (ACR/EULAR 2010):\n- Joint involvement (swollen/tender joints)\n- Serology (RF and/or ACPA)\n- Acute-phase reactants (CRP and ESR)\n- Duration of symptoms (≥6 weeks)\n\nFirst-line pharmacological management typically involves conventional synthetic DMARDs (e.g., Methotrexate) often bridging with short-term glucocorticoids.",
    citations: [
      { title: "Pathophysiology of Rheumatoid Arthritis", url: "https://pubmed.ncbi.nlm.nih.gov/", source: "PubMed" },
      { title: "NICE Guidelines: Rheumatoid arthritis in adults", url: "https://www.nice.org.uk/guidance/ng100", source: "NICE" }
    ]
  };
};