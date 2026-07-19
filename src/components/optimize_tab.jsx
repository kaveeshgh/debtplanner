import { useState } from 'react'


const loanBoxStyle = {
  border: '1px solid #444',
  borderRadius: '8px',
  padding: '16px',
  marginBottom: '12px',
  backgroundColor: '#1a1a1a',
  color: 'white'
}



function OptimizeTab({ loans, results, setResults }) {

  const [chartImg, setChartImg] = useState(null)
  const [loading, setLoading] = useState(false)



  const optimize = async () => {

    setLoading(true)


    const res = await fetch(
      "http://localhost:8000/analyze/optimize",
      {
        method: "POST",

        headers:{
          "Content-Type":"application/json"
        },

        body: JSON.stringify({
          loans
        })
      }
    )


    const data = await res.json()


    setResults(data)

    setChartImg(data.chart)


    setLoading(false)
  }




  return (

    <div>


      <button
        onClick={optimize}
        disabled={loading}
      >
        {loading ? "Running..." : "Run Optimize"}
      </button>




      {results && (

        <div style={{
          display:"flex",
          gap:"40px",
          marginTop:"30px"
        }}>


          <div>


            <div style={loanBoxStyle}>

              <h3 style={{color:"#8884d8"}}>
                Avalanche
              </h3>


              <p>
                Months:
                <strong>
                  {" "}
                  {results.avalanche.months}
                </strong>
              </p>


              <p>
                Interest:
                <strong>
                  {" "}
                  ${results.avalanche.total_interest.toLocaleString()}
                </strong>
              </p>


            </div>





            <div style={loanBoxStyle}>

              <h3 style={{color:"#82ca9d"}}>
                Snowball
              </h3>


              <p>
                Months:
                <strong>
                  {" "}
                  {results.snowball.months}
                </strong>
              </p>


              <p>
                Interest:
                <strong>
                  {" "}
                  ${results.snowball.total_interest.toLocaleString()}
                </strong>
              </p>


            </div>





            <div style={loanBoxStyle}>


              <h3>
                Recommendation
              </h3>


              <p>
                {results.recommendation.strategy}
              </p>


              <p style={{color:"#aaa"}}>
                {results.recommendation.reason}
              </p>


            </div>


          </div>






          {chartImg && (

            <div style={{flex:1}}>

              <img
                src={chartImg}
                alt="Debt balance chart"
                style={{
                  width:"100%"
                }}
              />

            </div>
          )}
        </div>
      )}
    </div>

  )
}

export default OptimizeTab
