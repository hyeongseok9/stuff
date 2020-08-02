import React, { Component } from 'react';
import styled from 'styled-components';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'

const options = {
  title: {
    text: 'My chart'
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
    this.internalChart.addSeries({'data': [1,2,3,4]})
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