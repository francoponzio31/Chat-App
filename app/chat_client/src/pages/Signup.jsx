import { useState, useRef } from "react"
import { Link } from "react-router-dom"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import Alert from "react-bootstrap/Alert"
import authService from "../services/auth.js"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faRocketchat } from "@fortawesome/free-brands-svg-icons"

export default function Signup(){

    const usernameInputRef = useRef(null)
    const emailInputRef = useRef(null)
    const passwordInputRef = useRef(null)
    const confirmPasswordInputRef = useRef(null)
    const formRef = useRef(null)
    const [error, setError] = useState(null)
    const [showSuccessModal, setShowSuccessModal] = useState(false)



    async function handleSignup(event){
        setError("")

        if (!formRef.current.reportValidity()){
            return
        }
        event.preventDefault()
        
        if (passwordInputRef.current.value !== confirmPasswordInputRef.current.value){
            setError("Passwords entered do not match")
            return
        }
        
        try {
            await authService.signup(
                usernameInputRef.current.value,
                emailInputRef.current.value,
                passwordInputRef.current.value
            )

            setShowSuccessModal(true)
            usernameInputRef.current.value = ""
            emailInputRef.current.value = ""
            passwordInputRef.current.value = ""
            confirmPasswordInputRef.current.value = ""

        } catch (error) {
            if (error.response.status === 400){
                setError("Invalid data")
            }
            else if (error.response.status === 409){
                setError("The email is already registered")
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

            {showSuccessModal && (
                <Alert style={{ marginTop: "4em" }} variant="primary" onClose={() => setShowSuccessModal(false)} dismissible>
                    <Alert.Heading>Successful Sign Up!</Alert.Heading>
                    <p>Check your email to verify your account.</p>
                </Alert>
            )}

            <h3 className="mt-5 mb-4 fs-1">Sign Up</h3>
            <Form ref={formRef}>
                <Form.Group className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" placeholder="Enter username" required ref={usernameInputRef}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" required ref={emailInputRef}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password" required ref={passwordInputRef} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Confirm password</Form.Label>
                    <Form.Control type="password" placeholder="Confirm password" required ref={confirmPasswordInputRef} />
                </Form.Group>
                {error && <p className="text-danger">{error}</p>}
                <Button variant="primary" type="submit" onClick={handleSignup} >
                    Submit
                </Button>
            </Form>

            <div className="mt-3">
                <Link to="/login" className="text-decoration-none">Login with your account</Link>
            </div>
        </div>
            
    )
}