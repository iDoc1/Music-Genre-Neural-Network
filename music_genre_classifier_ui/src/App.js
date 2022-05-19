import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import TopNavbar from './components/Navbar';

function App() {
  
  return (
    <div className="App">
      <Router>
        <TopNavbar/>
        <Routes>
          <Route path='/' exact element={<HomePage />} />
          <Route path='/about' element={<AboutPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
