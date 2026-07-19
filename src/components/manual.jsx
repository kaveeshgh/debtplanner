import { useState } from 'react'

function Manual({ setLoans, setDone, loans, setMode }) {
  // Local state for the form fields
  const [form, setForm] = useState({
    principal: '',
    interest_rate: '',
    monthly_payment: '',
    maturity_date: ''
  })

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  // Checkes if necessary fields are filled
  const addLoan = () => {

      setLoans(prevLoans => [
          ...prevLoans,
          form
      ])

      setForm({
          principal:'',
          interest_rate:'',
          monthly_payment:'',
          maturity_date:''
      })
  }


  // Clears all loans and resets mode to null
  const goBack = () => {
    setLoans([]);
    setMode(null);
  }

  
  return (
    <div style={{ padding: '40px' }}>
      <button onClick={goBack}>← Back</button>
      <h2>Enter Loan Details</h2>
    
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px' }}>
        <label>Principal ($)
          <input name="principal" value={form.principal} onChange={handleChange} placeholder="e.g. 20000" />
        </label>
        <label>Interest Rate (%)
          <input name="interest_rate" value={form.interest_rate} onChange={handleChange} placeholder="e.g. 5.5" />
        </label>
        <label>Monthly Payment ($)
          <input name="monthly_payment" value={form.monthly_payment} onChange={handleChange} placeholder="e.g. 400" />
        </label>
        <label>Maturity Date (optional)
          <input name="maturity_date" value={form.maturity_date} onChange={handleChange} placeholder="e.g. January 1, 2030" />
        </label>
        <button onClick={addLoan}>Add Loan</button>
      </div>

      <p>{loans.length} loan(s) added</p>

      {loans.length > 0 && (
        <div>
          {loans.map((loan, i) => (
            <p key={i}>Loan {i + 1}: ${loan.principal} at {loan.interest_rate}%</p>
          ))}
          <button onClick={() => setDone(true)}>Done — See Results</button>
        </div>
      )}
    </div>
  )
}

export default Manual
