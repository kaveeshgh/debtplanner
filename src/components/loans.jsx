
function LoanList({ loans, setLoans, editingIndex, setEditingIndex, editForm, setEditForm, setResults, setTimeline }) {

  // Sets which loan is being edited and copies its current values 
  const startEdit = (index) => {
    setEditingIndex(index)
    setEditForm({ ...loans[index] })
  }

  // For every loan, if its index matches editingIndex, replace it with the edited values
  const saveEdit = () => {
    const updated = loans.map((loan, i) => i === editingIndex ? editForm : loan)
    // Updates the global loans, exits edit mode, and clears old results 
    setLoans(updated)
    setEditingIndex(null)
    setResults(null)
    setTimeline(null)
  }

  // Stop editing, don't save values
  const cancelEdit = () => {
    setEditingIndex(null)
    setEditForm({})
  }

  const loanBoxStyle = {
    border: '1px solid #444',
    borderRadius: '8px',
    padding: '16px',
    marginBottom: '12px',
    backgroundColor: '#1a1a1a',
    color: 'white'
  }

  const inputStyle = {
    display: 'block',
    margin: '6px 0',
    padding: '6px',
    width: '100%',
    backgroundColor: '#333',
    color: 'white',
    border: '1px solid #555',
    borderRadius: '4px'
  }

  return (
    <div>
      <h2 style={{ marginTop: '20px' }}>Your Loans</h2>
      {loans.map((loan, index) => (
        <div key={index} style={loanBoxStyle}>
          {editingIndex === index ? (
            <div>
              <p style={{ fontWeight: 'bold', marginBottom: '10px' }}>Editing Loan {index + 1}</p>
              <label>Name
                <input style={inputStyle} value={editForm.name} onChange={e => setEditForm({ ...editForm, name: e.target.value })} />
              </label>
              <label>Type
                <input style={inputStyle} value={editForm.type} onChange={e => setEditForm({ ...editForm, type: e.target.value })} />
              </label>
              <label>Principal ($)
                <input style={inputStyle} value={editForm.principal} onChange={e => setEditForm({ ...editForm, principal: e.target.value })} />
              </label>
              <label>Interest Rate (%)
                <input style={inputStyle} value={editForm.interest_rate} onChange={e => setEditForm({ ...editForm, interest_rate: e.target.value })} />
              </label>
              <label>Minimum Payment ($)
                <input style={inputStyle} value={editForm.minimum_payment} onChange={e => setEditForm({ ...editForm, minimum_payment: e.target.value })} />
              </label>
              <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                <button onClick={saveEdit}>Save</button>
                <button onClick={cancelEdit}>Cancel</button>
              </div>
            </div>
          ) : (
            <div>
              <p style={{ fontWeight: 'bold', marginBottom: '8px' }}>Loan {index + 1}</p>
              <p>Name: {loan.name || 'N/A'}</p>
              <p>Type: {loan.type || 'N/A'}</p>
              <p>Principal: ${loan.principal}</p>
              <p>Interest Rate: {loan.interest_rate}%</p>
              <p>Minimum Payment: ${loan.minimum_payment}</p>
              <button onClick={() => startEdit(index)} style={{ marginTop: '10px' }}>Edit</button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default LoanList
