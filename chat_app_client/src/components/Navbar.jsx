import Container from "react-bootstrap/Container"
import BSNavbar from "react-bootstrap/Navbar"
import Nav from "react-bootstrap/Nav"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faRocketchat } from "@fortawesome/free-brands-svg-icons"
import { faUser, faPowerOff } from "@fortawesome/free-solid-svg-icons"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext.jsx"
import authService from "../services/auth.js"
import { useState, useEffect } from "react"


export default function Navbar(){

    const authContext = useAuth()
    const navigate = useNavigate()
    const [username, setUsername] = useState("")

    useEffect(() => {
        async function getCurrentUser(){
            try {
                const response = await authService.current(authContext.token)
                setUsername(response.user.username)
            } catch (error) {   // TODO: pulir el manejo de errores, en especial ucando se vence el JWT
                console.error("Error fetching current user:", error)
                navigate("/login")
            }
        }
        getCurrentUser()
    }, [])

    const handleLogout = () => {
        authContext.logout()
        navigate("/login")
    }

    const handleHomeRedirect = () => {
        navigate("/")
    }

    return (
        <>
            <BSNavbar expand="lg" className="bg-body-tertiary">
                <Container>
                    <BSNavbar.Brand className="d-flex align-items-center gap-2" onClick={handleHomeRedirect} style={{cursor:"pointer"}}>
                        <FontAwesomeIcon icon={faRocketchat} size="lg"/>
                        Chat app
                    </BSNavbar.Brand>
                    <Nav className="d-flex align-items-center gap-3">
                        <Nav.Link href="/profile" className="d-flex align-items-center gap-2">
                            <FontAwesomeIcon icon={faUser} />
                            {username}
                        </Nav.Link>
                        <Nav.Link className="d-flex align-items-center gap-2" onClick={handleLogout}>
                            <FontAwesomeIcon icon={faPowerOff} />
                            Logout
                        </Nav.Link>
                    </Nav>
                </Container>
            </BSNavbar>
        </>
    )
}