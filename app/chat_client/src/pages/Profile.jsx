import { useEffect, useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import authService from "../services/auth.js"
import userService from "../services/users.js"
import ProfileCard from "../components/ProfileCard.jsx"
import { toBase64, getUserPictureFilename } from "../utils/utils.js"
import { useAuth } from "../contexts/AuthContext.jsx"
import Navbar from "../components/Navbar.jsx"
import Container from "react-bootstrap/Container"
import Button from "react-bootstrap/Button"
import Form from "react-bootstrap/Form"
import Modal from "react-bootstrap/Modal"
import Spinner from "react-bootstrap/Spinner"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faChevronLeft } from "@fortawesome/free-solid-svg-icons"
import "../index.css"


export default function Profile() {

    const navigate = useNavigate()
    const authContext = useAuth()

    const [loadingUserData, setLoadingUserData] = useState(true)
    const [updatingUserData, setUpdatingUserData] = useState(false)
    const [reloadUserData, setReloadUserData] = useState(false)
    const [showModal, setShowModal] = useState(false)

    const [username, setUsername] = useState("")
    const [userEmail, setUserEmail] = useState("")
    const [userId, setUserId] = useState("")
    const [profilePicture, setProfilePicture] = useState("")

    const usernameInputRef = useRef(null)
    const pictureInputRef = useRef(null)
    
    const handleShowModal = () => {
        setShowModal(true)
        if (usernameInputRef.current){
            usernameInputRef.current.value = username
        }
    }

    const handleClose = () => setShowModal(false)

    const handleSaveChanges = async () => {
        setUpdatingUserData(true)
        const updatedUsername = usernameInputRef.current.value
        const selectedFile = pictureInputRef.current.files[0]
        let dataUpdated = false

        // Form validation
        if (!usernameInputRef.current.checkValidity() || (selectedFile && !pictureInputRef.current.checkValidity())) {
            usernameInputRef.current.reportValidity()
            pictureInputRef.current.reportValidity()
            return
        }

        if (updatedUsername != username){
            console.log("Updated username:", updatedUsername)
            await userService.updateUser(userId, authContext.token, {
                username: updatedUsername
            })
            dataUpdated = true
        }
        if (selectedFile) {
            console.log("Selected file:", selectedFile)
            const profilePictureBase64 = await toBase64(selectedFile)
            const profilePictureName = selectedFile.name
            await userService.updateProfilePicture(userId, authContext.token, profilePictureBase64, profilePictureName)
            dataUpdated = true
        }

        if (dataUpdated){
            setReloadUserData(!reloadUserData)
        }

        setUpdatingUserData(false)
        handleClose()
    }
    
    useEffect(() => {
        async function getCurrentUser(){
            setLoadingUserData(true)
            try {
                console.log("Fetching current user")
                const response = await authService.current(authContext.token)
                setUsername(response.user.username)
                setUserEmail(response.user.email)
                setUserId(response.user.id)
                const profilePictureFile = await getUserPictureFilename(response.user.picture_id)
                setProfilePicture(profilePictureFile)
                setLoadingUserData(false)
            } catch (error) {
                console.error("Error fetching current user:", error)
            }
        }
        getCurrentUser()
    }, [reloadUserData])

    const handleHomeRedirect = () => {
        navigate("/")
    }

    return <>
        <Navbar/>

        <FontAwesomeIcon icon={faChevronLeft} onClick={handleHomeRedirect} className="selectable mt-4 ms-5 mb-2" style={{ fontSize: "1.8em" }}/>
        
        <Container className="">
            <h2 className="mb-3">Profile</h2>

            <ProfileCard username={username} userEmail={userEmail} profilePicture={profilePicture} loading={loadingUserData}/>
            
            <Button className="mt-3" onClick={handleShowModal}>Edit profile</Button>

            {/* Edit profile form */}
            <Modal show={showModal} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Profile edit</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group className="mb-3">
                            <Form.Label>Username</Form.Label>
                            <Form.Control
                                type="text"
                                defaultValue={username}
                                ref={usernameInputRef}
                                required
                            />
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Profile Picture</Form.Label>
                            <Form.Control
                                type="file"
                                accept="image/jpeg, image/jpg, image/png"
                                ref={pictureInputRef}
                            />
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                    {
                        updatingUserData ? (
                            <Button variant="primary" onClick={handleSaveChanges} disabled>
                                <Spinner
                                    as="span"
                                    animation="border"
                                    size="sm"
                                    aria-hidden="true"
                                />
                                Loading...
                            </Button>
                        ) : (
                            <Button variant="primary" onClick={handleSaveChanges}>
                                Save Changes
                            </Button>
                        )
                    }
                </Modal.Footer>
            </Modal>

        </Container>
    </>
}
