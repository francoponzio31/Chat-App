import "bootstrap/dist/css/bootstrap.min.css"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import { AuthProvider } from "./contexts/AuthContext.jsx"
import { SocketsProvider } from "./contexts/SocketsContext.jsx"
import Login from "./pages/Login"
import Signup from "./pages/Signup"
import EmailVerification from "./pages/EmailVerification"
import Home from "./pages/Home.jsx"
import Chat from "./pages/Chat.jsx"
import Profile from "./pages/Profile"
import LoggedInRequiredRoute from "./components/ProtectedRoute.jsx"


function App() {
  
  return (
    <Router>
      <AuthProvider>
        <SocketsProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/verify-email" element={<EmailVerification />} />
            <Route path="/" element={<LoggedInRequiredRoute element={<Home />}/>} />
            <Route path="/chat/:chatId" element={<Chat />} />
            <Route path="/profile" element={<LoggedInRequiredRoute element={<Profile />}/>} />
          </Routes>
        </SocketsProvider>
      </AuthProvider>
    </Router>
  )
}

export default App
