import React from 'react'
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Search from './Search/Search.js'
 


function App() {
  return (
    <div className="App">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Navigate to="/search" />}/>
            <Route path="/search" element={<Search />}/>

          </Routes>

        </BrowserRouter>
  
    </div>
  );
}

export default App;
