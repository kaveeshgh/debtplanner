import { useState } from 'react'

function File({ setLoans, setDone, loans }) {

  const getFile = async (event) => {
    const file = event.target.files[0];

    const formData = new FormData();
    formData.append("file",file);

    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const info = await response.json();

    
    setLoans(prevLoans => [...prevLoans, info.loan]);
    console.log(info.loans);
  }


  return (
    
    <div>
      <input type="file" onChange={getFile} />
      <p>{loans.length} loan(s) uploaded</p>
      <button onClick={() => setDone(true)}>Done</button>
    </div>
  )
}

export default File
