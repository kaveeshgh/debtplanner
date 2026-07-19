import { useState } from 'react'
import File from './components/file'
import Manual from './components/manual'
import ResultsPage from './components/results'

function App() {
  // Creates a state variable loans starting as an empty array
  const [loans, setLoans] = useState([]);
  // Boolean - false means still in the upload/entry phase, true means show the results page
  const [done, setDone] = useState(false);
  // Controls which view shows on the landing page
  const [mode, setMode] = useState(null);


  // If done return the results page and pass it everything it needs
  if (done) {
    return <ResultsPage loans={loans} setLoans={setLoans} setDone={setDone} setMode={setMode} />
  }
  // If mode is pdf, show the file upload component
  if (mode === 'pdf') {
    return <File setLoans={setLoans} setDone={setDone} loans={loans} setMode={setMode} />
  }
  // If mode is manual, show the manual entry component
  if (mode === 'manual') {
    return <Manual setLoans={setLoans} setDone={setDone} loans={loans} setMode={setMode} />
  }


  // Landing page
  return (
    <div style={{ backgroundColor: 'black', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
      
      <h1 style={{ color: 'white', fontSize: '3rem', marginBottom: '10px' }}>Plan your debt now</h1>
      <p style={{ color: 'grey', marginBottom: '30px' }}>Choose how to add your loans</p>

      <button onClick={() => setMode('pdf')} style={{ padding: '15px 40px', fontSize: '1rem', cursor: 'pointer' }}>
        Upload PDF
      </button>
      <button onClick={() => setMode('manual')} style={{ padding: '15px 40px', fontSize: '1rem', cursor: 'pointer' }}>
        Enter Manually
      </button>
    </div>
  )
}

export default App
