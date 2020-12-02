import './App.css';
import React, {useEffect, useState } from 'react';
import List from './components/List';
import Navigation from './components/Navbar';
import WithListLoading from './components/WithListLoading';
import Routes from "./Routes"
const axios = require('axios');
function App() {
  // const ListLoading = WithListLoading(List);
  // const [appState, setAppState] = useState({
  //   loading: true,
  //   repos: null,
  // });

  // useEffect(() => {
  //   setAppState({loading : true});
  //   let headers = new Headers();

  //   headers.append('Content-Type', 'application/json');
  //   headers.append('Accept', 'application/json');
  //   headers.append('Origin','http://localhost:5000');
  //   axios({
  //       url: "/search",
  //       baseURL: 'http://127.0.0.1:5000',
  //       method: 'POST',
  //       headers: headers,
  //       data: {
  //           tag: 'MkLeo'
  //       },
  //   })
  //       .then(function (response) {
  //           console.log(response);
  //           const allPlacings = response.data;
  //           setAppState({ loading : false, repos: allPlacings});
            
  //       })
  //       .catch(function (error) {
  //           console.log(error);
  //       })
  //       .then(function () {
  //           // always executed
  //           console.log("I always run");
  //       });
  // }, [setAppState]);
  return (
    <div className="App">
      <Navigation/>
      <Routes/>
      
    </div>
  );
}

export default App;
