import { useState } from 'react'

function ResultsPage({ loans }) {
  const [results, setResults] = useState(null)
  const [mcResults, setMcResults] = useState(null)

  const optimize = async () => {
    const response = await fetch("http://localhost:8000/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ loans, extra_payment: 100 })  // hardcoded $100/month extra for now
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
    </div>
  )
}

export default ResultsPage
