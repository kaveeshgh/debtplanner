const loanBoxStyle = {
  border: '1px solid #444',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
  backgroundColor: '#1a1a1a',
  color: 'white'
}


function ScheduleTab({ loans, schedule, setSchedule }) {

  const runSchedule = async () => {
    const response = await fetch("http://localhost:8000/schedule", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })
    })
    const data = await response.json()
    setSchedule(data)
  }


  return (
    <div>
      <p style={{ color: '#aaa', marginBottom: '16px', maxWidth: '600px' }}>
        A full month-by-month breakdown of every payment — how much goes to interest vs principal each month, and your running total debt.
      </p>
      <button onClick={runSchedule}>Generate Schedule</button>

      {schedule && (
        <div style={{ marginTop: '20px' }}>
          <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold' }}>Total months</p>
              <p>{schedule.summary.total_months} months ({(schedule.summary.total_months / 12).toFixed(1)} years)</p>
            </div>
            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold' }}>Total interest paid</p>
              <p>${schedule.summary.total_interest_paid.toLocaleString()}</p>
            </div>
            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold' }}>Total principal paid</p>
              <p>${schedule.summary.total_principal_paid.toLocaleString()}</p>
            </div>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #444' }}>
                  <th style={{ padding: '8px', textAlign: 'left', color: '#aaa' }}>Month</th>
                  <th style={{ padding: '8px', textAlign: 'right', color: '#aaa' }}>Total Balance</th>
                  <th style={{ padding: '8px', textAlign: 'right', color: '#aaa' }}>Interest Paid</th>
                  <th style={{ padding: '8px', textAlign: 'right', color: '#aaa' }}>Principal Paid</th>
                  <th style={{ padding: '8px', textAlign: 'right', color: '#aaa' }}>Cumulative Interest</th>
                </tr>
              </thead>
              <tbody>
                {schedule.schedule.map((row, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid #222' }}>
                    <td style={{ padding: '8px', color: 'white' }}>{row.month}</td>
                    <td style={{ padding: '8px', textAlign: 'right', color: 'white' }}>${row.total_balance.toLocaleString()}</td>
                    <td style={{ padding: '8px', textAlign: 'right', color: '#ff6b6b' }}>${row.total_interest.toLocaleString()}</td>
                    <td style={{ padding: '8px', textAlign: 'right', color: '#82ca9d' }}>${row.total_principal.toLocaleString()}</td>
                    <td style={{ padding: '8px', textAlign: 'right', color: '#aaa' }}>${row.cumulative_interest.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default ScheduleTab
