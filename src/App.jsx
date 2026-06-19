import { useState } from 'react'
import debtImg from './assets/debt.png'
import './App.css'
import LoanInput from './components/input'
import File from './components/file'
import ResultsPage from './components/results'

function App() {
  const [loans, setLoans] = useState([]);
  const [done, setDone] = useState(false);

   return (
    <div>
      {done ? <ResultsPage loans={loans} /> : <File setLoans={setLoans} setDone={setDone} loans={loans} />}
    </div>
  )
}

export default App
