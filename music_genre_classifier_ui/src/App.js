import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import AboutPage from './pages/AboutPage';
import TopNavbar from './components/Navbar';

function App() {
    const [videoUrl, setVideoUrl] = useState(null); // Provides URL to model for testing
    const [videoTitle, setVideoTitle] = useState(null);
  
    return (
        <div className="App">
        <Router>
            <TopNavbar/>
            <Routes>
            <Route path='/' exact element={<HomePage setVideoUrl={setVideoUrl} setVideoTitle={setVideoTitle}/>} />
            <Route path='/results' element={<ResultsPage videoUrl={videoUrl} videoTitle={videoTitle}/>} />
            <Route path='/about' element={<AboutPage />} />
            </Routes>
        </Router>
        </div>
    );
}

export default App;
