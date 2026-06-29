import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function ResultsPage({ loans }) {
  const [results, setResults] = useState(null)
  const [mcResults, setMcResults] = useState(null)
  const [timeline, setTimeline] = useState(null)

  const optimize = async () => {
    const response = await fetch("http://localhost:8000/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })
    })
    const data = await response.json()
    setResults(data)
  }

  const runMonteCarlo = async () => {
    const response = await fetch("http://localhost:8000/monte-carlo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })
    })
    const data = await response.json()
    setMcResults(data)
  }

  const runTimeline = async () => {
    const response = await fetch("http://localhost:8000/timeline", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })
    })
    const data = await response.json()

    // merge avalanche + snowball into one array recharts can read
    const merged = data.avalanche.map((point, i) => ({
      month: point.month,
      avalanche: point.balance,
      snowball: data.snowball[i] ? data.snowball[i].balance : null
    }))

    setTimeline(merged)
  }

  return (
    <div>
      {loans.map((loan, index) => (
        <div key={index}>
          <p><br />Principal: {loan.principal}</p>
          <p>Interest Rate: {loan.interest_rate}</p>
          <p>Monthly Payment: {loan.monthly_payment}</p>
          <p>Maturity Date: {loan.maturity_date}</p>
        </div>
      ))}

      <button onClick={optimize}>Optimize</button>
      <button onClick={runMonteCarlo}>Run Monte Carlo</button>
      <button onClick={runTimeline}>Show Graph</button>

      {results && (
        <div>
          <h2>Avalanche</h2>
          <p>Months to payoff: {results.avalanche.months}</p>
          <p>Total interest paid: ${results.avalanche.total_interest}</p>

          <h2>Snowball</h2>
          <p>Months to payoff: {results.snowball.months}</p>
          <p>Total interest paid: ${results.snowball.total_interest}</p>
        </div>
      )}

      {mcResults && (
        <div>
          <h2>Monte Carlo — Avalanche</h2>
          <p>Best case: {mcResults.avalanche.best_case} months</p>
          <p>Median: {mcResults.avalanche.median} months</p>
          <p>Worst case: {mcResults.avalanche.worst_case} months</p>

          <h2>Monte Carlo — Snowball</h2>
          <p>Best case: {mcResults.snowball.best_case} months</p>
          <p>Median: {mcResults.snowball.median} months</p>
          <p>Worst case: {mcResults.snowball.worst_case} months</p>
        </div>
      )}

      {timeline && (
        <div style={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
            <LineChart data={timeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" label={{ value: 'Month', position: 'insideBottom', offset: -5 }} />
              <YAxis label={{ value: 'Balance ($)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="avalanche" stroke="#8884d8" dot={false} />
              <Line type="monotone" dataKey="snowball" stroke="#82ca9d" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

export default ResultsPage