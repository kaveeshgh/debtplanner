import { useState } from 'react'
import LoanList from './loans'
import OptimizeTab from './optimize_tab'
import MonteCarloTab from './montecarlo_tab'
import ScheduleTab from './schedule_tab'

function ResultsPage({ loans, setLoans, setDone, setMode }) {
  const [tab, setTab] = useState('optimize')
  const [results, setResults] = useState(null)
  const [mcResults, setMcResults] = useState(null)
  const [schedule, setSchedule] = useState(null)
  const [editingIndex, setEditingIndex] = useState(null)
  const [editForm, setEditForm] = useState({})

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
        setTimeline={() => {}}
      />

      <div style={{ display: 'flex', gap: '10px', margin: '30px 0 20px' }}>
        <button onClick={() => setTab('optimize')}   style={{ fontWeight: tab === 'optimize'   ? 'bold' : 'normal' }}>Optimize</button>
        <button onClick={() => setTab('montecarlo')} style={{ fontWeight: tab === 'montecarlo' ? 'bold' : 'normal' }}>Monte Carlo</button>
        <button onClick={() => setTab('schedule')}   style={{ fontWeight: tab === 'schedule'   ? 'bold' : 'normal' }}>Schedule</button>
      </div>

      {tab === 'optimize'   && <OptimizeTab   loans={loans} results={results}   setResults={setResults} />}
      {tab === 'montecarlo' && <MonteCarloTab loans={loans} mcResults={mcResults} setMcResults={setMcResults} />}
      {tab === 'schedule'   && <ScheduleTab   loans={loans} schedule={schedule}  setSchedule={setSchedule} />}

    </div>
  )
}

export default ResultsPage
