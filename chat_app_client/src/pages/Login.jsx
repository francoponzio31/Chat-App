import { useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import authService from "../services/auth"
import { useAuth } from "../contexts/AuthContext.jsx"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faRocketchat } from "@fortawesome/free-brands-svg-icons"

export default function Login(){

    const authContext = useAuth()
    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const emailInputRef = useRef(null)
    const passwordInputRef = useRef(null)
    const formRef = useRef(null)
    const [error, setError] = useState(null)

    function handleEmailInputChange(){
        setEmail(emailInputRef.current.value)
    }

    function handlePasswordInputChange(){
        setPassword(passwordInputRef.current.value)
    }

    async function handleLogin(event){
        if (!formRef.current.reportValidity()){
            return
        }
        event.preventDefault()
        
        try {
            const response = await authService.login(email, password)
            authContext.login(response.token)
            setError("")
            navigate("/")
        } catch (error) {
            if (error.status === 400){
                setError("Invalid data")
            }
            else if (error.status === 401){
                setError("Invalid username or password")
            }
            else {
                setError("Sorry, an error has occurred. Please try again")
            }
        }
    }

    return (
        <div className="container" style={{"marginTop": "6em"}}>

            <div className="d-flex align-items-center gap-3">
                <FontAwesomeIcon icon={faRocketchat} size="5x"/>
                <h2 style={{ fontSize: "3.5em" }}>Chat App</h2>
            </div>

            <h3 className="mt-5 mb-4 fs-1">Login</h3>
            <Form ref={formRef}>
                <Form.Group className="mb-3" controlId="LoginFormEmail">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" required value={email} onChange={handleEmailInputChange} ref={emailInputRef}/>
                </Form.Group>
                <Form.Group className="mb-3" controlId="LoginFormPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password" required value={password} onChange={handlePasswordInputChange} ref={passwordInputRef} />
                </Form.Group>
                {error && <p className="text-danger">{error}</p>}
                <Button variant="primary" type="submit" onClick={handleLogin} >
                    Submit
                </Button>
            </Form>
        </div>
    )
}