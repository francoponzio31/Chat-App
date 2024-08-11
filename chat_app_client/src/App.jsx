import "bootstrap/dist/css/bootstrap.min.css"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import { AuthProvider } from "./contexts/AuthContext.jsx"
import Login from "./pages/Login"
import Home from "./pages/Home"
import Profile from "./pages/Profile"
import LoggedInRequiredRoute from "./components/ProtectedRoute.jsx"


function App() {
  
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<LoggedInRequiredRoute element={<Home />}/>} />
          <Route path="/profile" element={<LoggedInRequiredRoute element={<Profile />}/>} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App
