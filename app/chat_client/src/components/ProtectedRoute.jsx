import { useAuth } from "../contexts/AuthContext.jsx"
import { Navigate } from "react-router-dom"


export default function LoggedInRequiredRoute({ element }) {
    const { token } = useAuth()
    return token ? element : <Navigate to="/login" />
}
