import { useState } from 'react'

function Manual({ setLoans, setDone, loans, setMode }) {
  // Local state for the form fields
  const [form, setForm] = useState({
    name: '',
    type: '',
    principal: '',
    interest_rate: '',
    minimum_payment: ''
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
        name: '',
        type: '',
        principal: '',
        interest_rate: '',
        minimum_payment: ''
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
        <label>Name (optional)
          <input name="name" value={form.name} onChange={handleChange} placeholder="e.g RBC Rewards Visa" />
        </label>
        <label>Type (optional)
          <input name="type" value={form.type} onChange={handleChange} placeholder="e.g Credit Card" />
        </label>
        <label>Principal ($)
          <input name="principal" value={form.principal} onChange={handleChange} placeholder="e.g. 20000" />
        </label>
        <label>Interest Rate/APR (%)
          <input name="interest_rate" value={form.interest_rate} onChange={handleChange} placeholder="e.g. 5.5" />
        </label>
        <label>Minimum Payment ($)
          <input name="minimum_payment" value={form.minimum_payment} onChange={handleChange} placeholder="e.g. 400" />
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
