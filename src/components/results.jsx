// Imports the four sub-components 
import { useState } from 'react'
import LoanList from './loans'
import OptimizeTab from './optimize_tab'
import MonteCarloTab from './montecarlo_tab'
import ScheduleTab from './schedule_tab'


function ResultsPage({ loans, setLoans, setDone, setMode }) {
  // Controls which tab is active
  const [tab, setTab] = useState('optimize')
  // Variables for each endpoint's response (mc = monte carlo)
  const [results, setResults] = useState(null)
  const [mcResults, setMcResults] = useState(null)
  const [timeline, setTimeline] = useState(null)
  const [schedule, setSchedule] = useState(null)
  // Tracks which loan is being edited (null = none) and holds the in-progress edit values
  const [editingIndex, setEditingIndex] = useState(null)
  const [editForm, setEditForm] = useState({})

  // Resets both flags, returning to the landing page
  const goBack = () => {
    setDone(false)
    setMode(null)
  }


  return (
    <div style={{ padding: '40px', backgroundColor: '#111', minHeight: '100vh', color: 'white' }}>

      <button onClick={goBack}>← Back</button>

      <LoanList
        loans={loans}
        setLoans={setLoans}
        editingIndex={editingIndex}
        setEditingIndex={setEditingIndex}
        editForm={editForm}
        setEditForm={setEditForm}
        setResults={setResults}
        setTimeline={setTimeline}
      />

      <div style={{ display: 'flex', gap: '10px', margin: '30px 0 20px' }}>
        <button onClick={() => setTab('optimize')} style={{ fontWeight: tab === 'optimize' ? 'bold' : 'normal' }}>Optimize</button>
        <button onClick={() => setTab('montecarlo')} style={{ fontWeight: tab === 'montecarlo' ? 'bold' : 'normal' }}>Monte Carlo</button>
        <button onClick={() => setTab('schedule')} style={{ fontWeight: tab === 'schedule' ? 'bold' : 'normal' }}>Schedule</button>
      </div>

      {tab === 'optimize' && <OptimizeTab loans={loans} results={results} setResults={setResults} timeline={timeline} setTimeline={setTimeline} />}
      {tab === 'montecarlo' && <MonteCarloTab loans={loans} mcResults={mcResults} setMcResults={setMcResults} />}
      {tab === 'schedule' && <ScheduleTab loans={loans} schedule={schedule} setSchedule={setSchedule} />}

    </div>
  )
}

export default ResultsPage
