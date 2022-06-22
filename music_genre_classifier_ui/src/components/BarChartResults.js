import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';

/**
 * Returns a component containing a barchart of the result probabilities.
 * This code was adapted from URL: https://codesandbox.io/s/jebqk?file=/App.tsx:27-216
 */
function BarChartResults({resultArr, sampleLocation, barChartColor}) {

    ChartJS.register(
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend
      );
      
    const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: `${sampleLocation} Sample`,
          },
        },
        scales: {
            y: {
                min: 0,
                max: 1,                    
            }
        }
      };
      
      const labels = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'];
      
      const data = {
        labels,
        datasets: [
          {
            label: 'Probability',
            data: resultArr,
            backgroundColor: barChartColor,
          },
        ],
      };

    return (
        <>
            <div className='barchartAndHeaderContainer'>
                <Bar
                    data={data}
                    height={400}
                    width={400}
                    options={options}
                />
            </div>
        </>
    );
}

export default BarChartResults;