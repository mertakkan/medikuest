// DataSelection.js

import React, { useState } from 'react';

const DataSelection = ({ fetchHistogram, onExecute, onTotalNum }) => {

    const [selectedOption1, setSelectedOption1] = useState('option1');
    const [selectedOperation, setSelectedOperation] = useState('option4');
    const [selectedAttribute, setSelectedAttribute] = useState('option7');
    const [selectedOption4, setSelectedOption4] = useState('option15');

    const [smokeSelection, setSmokeSelection] = useState('No');
    const [diabetesSelection, setDiabetesSelection] = useState('No');
    const [bloodTypeSelection, setBloodTypeSelection] = useState('A');

  const handleExecute1 = () => {
    fetchHistogram(selectedOption1);
  };

  const handleExecute2 = () => {
    onExecute(selectedOperation, selectedAttribute);
  };


  const handleExecute4 = () => {
    onTotalNum(selectedOption4, smokeSelection, diabetesSelection, bloodTypeSelection);
  };

  return (
    <div className="data-selection">
      <div className="dropdown-container">
        <select value={selectedOption1} onChange={(e) => setSelectedOption1(e.target.value)} className="dropdown">
          <option value="option1">Smoke Histogram</option>
          <option value="option2">Blood Histogram</option>
          <option value="option3">Diabetes Histogram</option>
        </select>
        <button onClick={handleExecute1} className="execute-button">Execute</button>
      </div>


      <div className="dropdown-container">
      <select value={selectedOperation} onChange={(e) => setSelectedOperation(e.target.value)} className="dropdown">
          <option value="option4">Max</option>
          <option value="option5">Min</option>
          <option value="option6">Avg</option>
        </select>
        <select value={selectedAttribute} onChange={(e) => setSelectedAttribute(e.target.value)} className="dropdown">
          <option value="option7">Age</option>
          <option value="option8">Height</option>
          <option value="option9">Weight</option>
          <option value="option10">BMI</option>
          <option value="option11">Temperature</option>
          <option value="option12">Heart Rate</option>
          <option value="option13">Blood Pressure</option>
          <option value="option14">Cholesterol</option>
        </select>
        <button onClick={handleExecute2} className="execute-button">Execute</button>
      </div>

      <div className="dropdown-container">
      <select value={smokeSelection} onChange={(e) => setSmokeSelection(e.target.value)} className="dropdown">
                    <option value="Yes">Smoke - Yes</option>
                    <option value="No">Smoke - No</option>
                </select>
                <select value={diabetesSelection} onChange={(e) => setDiabetesSelection(e.target.value)} className="dropdown">
                    <option value="Yes">Diabetes - Yes</option>
                    <option value="No">Diabetes - No</option>
                </select>
                <select value={bloodTypeSelection} onChange={(e) => setBloodTypeSelection(e.target.value)} className="dropdown">
                    <option value="A">Type A</option>
                    <option value="B">Type B</option>
                    <option value="AB">Type AB</option>
                    <option value="O">Type O</option>
                </select>
        <select value={selectedOption4} onChange={(e) => setSelectedOption4(e.target.value)} className="dropdown">
          <option value="option15">Smoke Number</option>
          <option value="option16">Blood Number</option>
          <option value="option17">Diabetes Number</option>
        </select>
        <button onClick={handleExecute4} className="execute-button">Execute</button>
      </div>
    </div>
  );
};

export default DataSelection;
