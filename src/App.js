// App.js

import React, { useState } from 'react';
import './App.css';
import AuthPage from './AuthPage';
import DataSelection from './DataSelection';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loggedInUsername, setLoggedInUsername] = useState("");
  const [result, setResult] = useState(''); 
  const [histogramImage, setHistogramImage] = useState('');
  const [imageKey, setImageKey] = useState(0);

  const handleAuthSuccess = (username) => {
    setIsAuthenticated(true);
    setLoggedInUsername(username);
  };

  const fetchHistogram = async (selectedOption) => {
    let attribute, values;
  
    switch (selectedOption) {
      case "option1": // Smoke Histogram
        attribute = "Smoking";
        values = ["Yes", "No"];
        break;
      case "option2": // Blood Histogram
        attribute = "BloodType";
        values = ["A", "B", "AB", "O"];
        break;
      case "option3": // Diabetes Histogram
        attribute = "Diabetes";
        values = ["Yes", "No"];
        break;
      default:
        return;
    }
  
    const response = await fetch('http://localhost:5000/api/histogram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        attribute,
        values,
        username: loggedInUsername,
        personal_epsilon: 10
        
      }),
    });
  
    const data = await response.json();
    if (data.image) {
      setHistogramImage(`data:image/png;base64,${data.image}`);
      setImageKey(prevKey => prevKey + 1);
    }
  };


  //fetching for max min avg function from .py
  const fetchData = async (operation, attribute) => {
    const operationsMap = {
      'option4': 'max',
      'option5': 'min',
      'option6': 'avg',
    };

    const attributesMap = {
      'option7': 'Age',
      'option8': 'Height',
      'option9': 'Weight',
      'option10': 'BMI',
      'option11': 'Temperature',
      'option12': 'HeartRate',
      'option13': 'BloodPressure',
      'option14': 'Cholesterol',
      
    };

    const operationValue = operationsMap[operation];
    const attributeValue = attributesMap[attribute];

    if (operationValue && attributeValue) {
      const response = await fetch(`http://localhost:5000/api/${operationValue}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attribute: attributeValue,
          personal_epsilon: 10,
          username: loggedInUsername
        }),
      });

      const data = await response.json();
      setResult(formatResult(data.result));
    }
  };

  const fetchTotalNum = async (attributeType, smoke, diabetes, bloodType) => {
    const attributeTypeMap = {
      'option15': 'Smoke',
      'option16': 'Blood',
      'option17': 'Diabetes',
    };
  
    const attributeTypeValue = attributeTypeMap[attributeType];
  
    if (attributeTypeValue) {
      const response = await fetch('http://localhost:5000/api/totalnum', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              attribute_type: attributeTypeValue,
              smoke,
              diabetes, 
              bloodType, 
              personal_epsilon: 10,
              username: loggedInUsername
          }),
      });
  
      const data = await response.json();
      setResult(formatResult(data.result));
    }
  };

  const formatResult = (value) => {
    if (!isNaN(value)) {
      return parseFloat(value).toFixed(4);
    }
    return value;
  };

  
  return (
    <div className="App">
      {isAuthenticated ? (
        <>
          <header className="App-header">
            <h1 className="app-title">MediKUest</h1>
          </header>
          <DataSelection
           fetchHistogram={fetchHistogram}
           onExecute={fetchData}
           onTotalNum={fetchTotalNum}
            />
          <div className="result-container">
          <div className="result-title">Result:</div>
          <div className="result-value">{result}</div>
        </div>
          {histogramImage && (
            <img
              key={imageKey}
              src={histogramImage}
              alt="Histogram"
              style={{ marginTop: '20px' }}
            />
          )}
        </>
      ) : (
        <AuthPage onAuthSuccess={handleAuthSuccess} />
      )}
    </div>
  );
}

export default App;
