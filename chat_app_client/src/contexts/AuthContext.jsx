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

    const login = (userToken) => {
      setToken(userToken)
      localStorage.setItem("authToken", userToken)
    }

    const logout = () => {
      setToken(null)
      localStorage.removeItem("authToken")
    }
    
    return (
      <AuthContext.Provider value={{ token, login, logout }}>
        {children}
      </AuthContext.Provider>
    )
}