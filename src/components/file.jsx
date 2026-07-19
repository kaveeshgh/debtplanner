import { useState } from 'react'

function File({ setLoans, setDone, loans, setMode }) {
  const getFile = async (event) => {
    // Get file
    const file = event.target.files[0];

    const formData = new FormData();
    formData.append("file", file);

    // Send file to python backend
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const info = await response.json();
    // Updates loans array
    setLoans(prevLoans => [...prevLoans, info.loan]);
  }

  // Clears all loans and resets mode to null
  const goBack = () => {
    setLoans([]);
    setMode(null);
  }

  return (
    <div style={{ padding: '40px' }}>
      <button onClick={goBack}>← Back</button>
      <h2>Upload Loan PDFs</h2>
      <input type="file" onChange={getFile} />

      <p>{loans.length} loan(s) uploaded</p>

      {loans.length > 0 && (
        <button onClick={() => setDone(true)}>Done — See Results</button>
      )}
    </div>
  )
}

export default File
