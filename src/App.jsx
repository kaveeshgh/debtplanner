import { useState } from 'react'
import debtImg from './assets/debt.png'
import './App.css'
import LoanInput from './components/input'
import File from './components/file'

function App() {
  const [count, setCount] = useState(0)

   return (
    <div>
      <File />
      <LoanInput />
      <p>This is my app</p>
      <button onClick={() => alert('clicked')}>Click me</button>
    </div>
  )
}

export default App
