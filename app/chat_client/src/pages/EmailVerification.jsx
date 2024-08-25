import Container from "react-bootstrap/Container"
import Spinner from "react-bootstrap/Spinner"
import authService from "../services/auth"
import { useLocation } from "react-router-dom"
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"


export default function EmailVerification(){

    const query = new URLSearchParams(useLocation().search)
    const userId = query.get("user")
    const token = query.get("token")

    const [verificationSuccess, setVerificationSuccess] = useState(false)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        async function verifyEmail(){
            setLoading(true)
            try {
                const response = await authService.verifyEmail(userId, token)
                console.log(response)
                setVerificationSuccess(true)
            } catch (error) {
                setVerificationSuccess(false)
                console.error("Error verifying email:", error)
            }
            finally {
                setLoading(false)
            }
        }
        verifyEmail()
    }, [])

    return (     
        <Container className="d-flex align-items-center justify-content-center fs-4" style={{"marginTop": "6em"}}>
            {
                loading ? (
                    <Spinner
                        as="span"
                        animation="border"
                        size="xl"
                        aria-hidden="true"
                    />
                ) : (
                verificationSuccess ? (
                    <p>
                        Email verified successfully, you can now <Link to="/login" className="text-decoration-none">login</Link>.
                    </p>
                )
                : (
                    <p>
                    Email verification error, please try again later.
                    </p>
                ))
            }
        </Container>
    )

}