import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'


const loanBoxStyle = {
  border: '1px solid #444',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
  backgroundColor: '#1a1a1a',
  color: 'white'
}


// Receives loans to send to the backend, current results/timeline to display, and setters to update them
function OptimizeTab({ loans, results, setResults, timeline, setTimeline }) {

  const optimize = async () => {

    const [optRes, tlRes] = await Promise.all([
      fetch("http://localhost:8000/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ loans, extra_payment: 100 })
      }),
      fetch("http://localhost:8000/timeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ loans, extra_payment: 100 })
      })
    ])

    // Parse both responses
    const optData = await optRes.json()
    const tlData = await tlRes.json()

    // Merges two separate arrays (avalanche timeline and snowball timeline) into one combined array for Recharts
    const merged = tlData.avalanche.map((point, i) => ({
      month: point.month,
      avalanche: point.balance,
      snowball: tlData.snowball[i] ? tlData.snowball[i].balance : null
    }))

    // Saves both to parent state
    setResults(optData)
    setTimeline(merged)
  }

  
  return (
    <div>
      <button onClick={optimize}>Run Optimize</button>

      {results && timeline && (
        <div style={{ display: 'flex', gap: '40px', marginTop: '30px', alignItems: 'flex-start' }}>
          <div style={{ minWidth: '250px' }}>
            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold', marginBottom: '8px', color: '#8884d8' }}>Avalanche</p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '8px' }}>Highest interest rate first</p>
              <p>Months to payoff: <strong>{results.avalanche.months}</strong> ({(results.avalanche.months / 12).toFixed(1)} years)</p>
              <p>Total interest: <strong>${results.avalanche.total_interest.toLocaleString()}</strong></p>
            </div>

            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold', marginBottom: '8px', color: '#82ca9d' }}>Snowball</p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '8px' }}>Smallest balance first</p>
              <p>Months to payoff: <strong>{results.snowball.months}</strong> ({(results.snowball.months / 12).toFixed(1)} years)</p>
              <p>Total interest: <strong>${results.snowball.total_interest.toLocaleString()}</strong></p>
            </div>

            <div style={{ ...loanBoxStyle, borderColor: '#666' }}>
              <p style={{ fontWeight: 'bold', marginBottom: '4px' }}>Recommendation</p>
              <p style={{ color: '#aaa', fontSize: '0.9rem' }}>
                {results.avalanche.total_interest <= results.snowball.total_interest
                  ? 'Avalanche saves you more money in total interest'
                  : 'Snowball gets you debt-free faster'}
              </p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', marginTop: '8px' }}>
                Interest difference: ${Math.abs(results.avalanche.total_interest - results.snowball.total_interest).toLocaleString()}
              </p>
            </div>
          </div>

          <div style={{ flex: 1, height: 400 }}>
            <p style={{ fontWeight: 'bold', marginBottom: '4px' }}>Balance Over Time</p>
            <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '10px' }}>How your total debt decreases month by month for each strategy</p>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={timeline}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="month" stroke="#aaa" label={{ value: 'Month', position: 'insideBottom', offset: -5, fill: '#aaa' }} />
                <YAxis stroke="#aaa" label={{ value: 'Balance ($)', angle: -90, position: 'insideLeft', fill: '#aaa' }} />
                <Tooltip contentStyle={{ backgroundColor: '#222', border: '1px solid #444' }} formatter={(value) => [`$${value.toLocaleString()}`]} />
                <Legend />
                <Line type="monotone" dataKey="avalanche" stroke="#8884d8" dot={false} name="Avalanche" />
                <Line type="monotone" dataKey="snowball" stroke="#82ca9d" dot={false} name="Snowball" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

export default OptimizeTab
