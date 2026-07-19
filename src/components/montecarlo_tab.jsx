import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'


const loanBoxStyle = {
  border: '1px solid #444',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
  backgroundColor: '#1a1a1a',
  color: 'white'
}


function MonteCarloTab({ loans, mcResults, setMcResults }) {
  // Send loans, get results, save to state.
  const runMonteCarlo = async () => {
    const response = await fetch("http://localhost:8000/monte-carlo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })
    })
    
    const data = await response.json()
    setMcResults(data)
  }


  return (
    <div>
      <p style={{ color: '#aaa', marginBottom: '16px', maxWidth: '600px' }}>
        Monte Carlo runs your loans through <strong style={{ color: 'white' }}>1,000 simulated lives</strong> — each one
        slightly different. Some months your income is higher, some months a surprise expense hits.
        The result is a <strong style={{ color: 'white' }}>range of payoff times</strong> rather than one fixed number, showing
        how real-life unpredictability affects each strategy.
      </p>

      <button onClick={runMonteCarlo}>Run Monte Carlo</button>

      {mcResults && (
        <div style={{ marginTop: '24px' }}>
          <div style={{ display: 'flex', gap: '20px', marginBottom: '30px', flexWrap: 'wrap' }}>
            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold', marginBottom: '12px', color: '#8884d8' }}>Avalanche Strategy</p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '10px' }}>
                Paying highest interest first, your payoff time varies by <strong style={{ color: 'white' }}>{mcResults.avalanche.worst_case - mcResults.avalanche.best_case} months</strong> depending on life circumstances
              </p>
              <p>Best case: <strong>{mcResults.avalanche.best_case} months</strong> ({(mcResults.avalanche.best_case / 12).toFixed(1)} years)</p>
              <p>Median: <strong>{mcResults.avalanche.median} months</strong> ({(mcResults.avalanche.median / 12).toFixed(1)} years)</p>
              <p>Worst case: <strong>{mcResults.avalanche.worst_case} months</strong> ({(mcResults.avalanche.worst_case / 12).toFixed(1)} years)</p>
            </div>

            <div style={loanBoxStyle}>
              <p style={{ fontWeight: 'bold', marginBottom: '12px', color: '#82ca9d' }}>Snowball Strategy</p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '10px' }}>
                Paying smallest balance first, your payoff time varies by <strong style={{ color: 'white' }}>{mcResults.snowball.worst_case - mcResults.snowball.best_case} months</strong> depending on life circumstances
              </p>
              <p>Best case: <strong>{mcResults.snowball.best_case} months</strong> ({(mcResults.snowball.best_case / 12).toFixed(1)} years)</p>
              <p>Median: <strong>{mcResults.snowball.median} months</strong> ({(mcResults.snowball.median / 12).toFixed(1)} years)</p>
              <p>Worst case: <strong>{mcResults.snowball.worst_case} months</strong> ({(mcResults.snowball.worst_case / 12).toFixed(1)} years)</p>
            </div>

            <div style={{ ...loanBoxStyle, borderColor: '#666' }}>
              <p style={{ fontWeight: 'bold', marginBottom: '8px' }}>What does this mean?</p>
              <p style={{ color: '#aaa', fontSize: '0.85rem', lineHeight: '1.6' }}>
                The <strong style={{ color: 'white' }}>median</strong> is your most likely payoff time.<br /><br />
                The gap between best and worst case shows how <strong style={{ color: 'white' }}>sensitive</strong> your plan is to unexpected events — a smaller gap means your plan is more robust to real life.
              </p>
            </div>
          </div>

          <p style={{ fontWeight: 'bold', marginBottom: '4px' }}>Payoff Range Comparison</p>
          <p style={{ color: '#aaa', fontSize: '0.85rem', marginBottom: '16px' }}>
            Each group shows best case, median, and worst case payoff time in months. Shorter bars = better outcome.
          </p>
          <div style={{ height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={[
                { name: 'Best Case', avalanche: mcResults.avalanche.best_case, snowball: mcResults.snowball.best_case },
                { name: 'Median', avalanche: mcResults.avalanche.median, snowball: mcResults.snowball.median },
                { name: 'Worst Case', avalanche: mcResults.avalanche.worst_case, snowball: mcResults.snowball.worst_case },
              ]}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="name" stroke="#aaa" />
                <YAxis stroke="#aaa" label={{ value: 'Months', angle: -90, position: 'insideLeft', fill: '#aaa' }} />
                <Tooltip contentStyle={{ backgroundColor: '#222', border: '1px solid #444' }} formatter={(value) => [`${value} months (${(value / 12).toFixed(1)} yrs)`]} />
                <Legend />
                <Bar dataKey="avalanche" fill="#8884d8" name="Avalanche" />
                <Bar dataKey="snowball" fill="#82ca9d" name="Snowball" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  )
}

export default MonteCarloTab
