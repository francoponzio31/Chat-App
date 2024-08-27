import Container from "react-bootstrap/Container"
import BSNavbar from "react-bootstrap/Navbar"
import Nav from "react-bootstrap/Nav"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faRocketchat } from "@fortawesome/free-brands-svg-icons"
import { faUser, faPowerOff, faComment } from "@fortawesome/free-solid-svg-icons"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext.jsx"


export default function Navbar(){

    const authContext = useAuth()
    const navigate = useNavigate()
 
    const handleLogout = () => {
        authContext.logout()
        navigate("/login")
    }

    const handleHomeRedirect = () => {
        navigate("/")
    }

    return (
        <BSNavbar collapseOnSelect expand="lg" className="bg-body-tertiary">
            <Container>
                <BSNavbar.Brand className="d-flex align-items-center gap-2" onClick={handleHomeRedirect} style={{cursor:"pointer"}}>
                    <FontAwesomeIcon icon={faRocketchat} size="lg"/>
                    Chat app
                </BSNavbar.Brand>
                <BSNavbar.Toggle aria-controls="navbarScroll" />
                <BSNavbar.Collapse>
                    <Nav className="ms-auto">
                        <Nav.Link href="/" className="d-flex align-items-center gap-2">
                            <FontAwesomeIcon icon={faComment} />
                            Chats
                        </Nav.Link>
                        <Nav.Link href="/profile" className="d-flex align-items-center gap-2">
                            <FontAwesomeIcon icon={faUser} />
                            Profile
                        </Nav.Link>
                        <Nav.Link className="d-flex align-items-center gap-2" onClick={handleLogout}>
                            <FontAwesomeIcon icon={faPowerOff} />
                            Logout
                        </Nav.Link>
                    </Nav>
                </BSNavbar.Collapse>
            </Container>
        </BSNavbar>
    )
}