import { createContext, useContext, useState} from "react"


export const AuthContext = createContext(null)

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
      throw new Error("useAuth must be used within an AuthProvider")
    }
    return context
}

export function AuthProvider({ children }) {
    
    const [token, setToken] = useState(() => localStorage.getItem("authToken"))
    const [userId, setUserId] = useState(() => localStorage.getItem("userId"))

    const login = (userToken, user) => {
      setToken(userToken)
      setUserId(user.id)
      localStorage.setItem("authToken", userToken)
      localStorage.setItem("userId", user.id)
    }

    const logout = () => {
      setToken(null)
      localStorage.removeItem("authToken")
    }
    
    return (
      <AuthContext.Provider value={{ token, userId, login, logout }}>
        {children}
      </AuthContext.Provider>
    )
}