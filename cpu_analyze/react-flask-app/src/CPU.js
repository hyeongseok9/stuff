import React, { Component } from 'react';
import styled from 'styled-components';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

const options =  {
  chart: {
      type: 'bar'
  },
  title: {
      text: 'Stacked bar chart'
  },
  yAxis: {
      min: 0,
      title: {
          text: 'CPU Percentage Analysis'
      }
  },
  legend: {
      reversed: true
  },
  plotOptions: {
      series: {
          stacking: 'normal'
      }
  }
}

const Wrapper = styled.div`
  margin-top: 1em;
  margin-left: 6em;
  margin-right: 6em;
`;

export class CPU extends React.Component {
  afterChartCreated = (chart) => {
    this.internalChart = chart;
  }

  componentDidMount(){

    fetch('http://localhost:3000/api/', {
      method: 'GET'
    })
    .then(response => response.json())
    .then(response => {
      this.internalChart.xAxis[0].setCategories(response.categories, true);
      
      Object.keys(response.series)
      .sort()
      .map((k) =>  ( 
        this.internalChart.addSeries({name: k, data:response.series[k]})
     ));

      // for (var k in response.series){
      //   this.internalChart.addSeries({name: k, data:response.series[k]})
      // }
    });
  }

  render() {
    return (
      <Wrapper>
    <h2>CPU Page</h2>
    <p>Chart</p>
    
    <HighchartsReact
    highcharts={Highcharts}
    options={options}
    callback={ this.afterChartCreated }
  />
    </Wrapper>
    );
  }
}

// export default CPU;


// export const CPU = () => (
//   <Wrapper>
//     <h2>CPU Page</h2>
//     <p>Chart</p>
    
//     <HighchartsReact
//     highcharts={Highcharts}
//     options={options}
//   />
//     </Wrapper>

// )