import React from 'react';
import BarChart from 'react-easy-bar-chart';
import 'bootstrap/dist/css/bootstrap.min.css';


function BarChartResults({ resultArr, sampleLocation }) {
    const data = [
        {
            title:  "Rock",
            value: resultArr[0],
            color: "#196f3d",
        },
        {
            title:  "Blues",
            value: resultArr[1],
            color: "#a93226",
        },
        {
            title:  "Classical",
            value: resultArr[2],
            color: " #1f618d",
        },
        {
            title:  "Country",
            value: resultArr[3],
            color: "#839192",
        },
        {
            title:  "Disco",
            value: resultArr[4],
            color: "#d35400",
        },
        {
            title:  "Hiphop",
            value: resultArr[5],
            color: " #a9cce3",
        },
        {
            title:  "Jazz",
            value: resultArr[6],
            color: "#2e4053",
        },
        {
            title:  "Metal",
            value: resultArr[7],
            color: "#186a3b",
        },
        {
            title:  "Pop",
            value: resultArr[8],
            color: "#fc03f4",
        },
        {
            title:  "Reggae",
            value: resultArr[9],
            color: "#ebfc03",
        },
        ];

    return (
        <>
            <div className='barchartAndHeaderContainer'>
            <h4>Results - {sampleLocation} Sample</h4>
            <BarChart 
                xAxis='Genres'
                yAxis="Probablities"
                height={400}
                width={800}
                data={data}
            />
            </div>
        </>
    );
}

export default BarChartResults;
