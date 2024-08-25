import Modal from "react-bootstrap/Modal"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import Container from "react-bootstrap/Container"
import Spinner from "react-bootstrap/Spinner"
import NewContactUserCard from "../components/NewContactUserCard.jsx"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons"
import { useState, useRef } from "react"
import { useAuth } from "../contexts/AuthContext.jsx"
import userService from "../services/users.js"


export default function NewContactModal({showContactModal, setShowContactModal}){

    const authContext = useAuth()
    const [loading, setLoading] = useState(false)
    const [usersSearchResult, setUsersSearchResult] = useState([])
    const userSearchInputRef = useRef(null)

    function handleCloseContactModal(){
        setShowContactModal(false)
    }

    async function handleSearch(){
        console.log("userSearchInputRef.current")
        setLoading(true)
        console.log(userSearchInputRef.current.value)
        const response = await userService.search(10, 0, userSearchInputRef.current.value, authContext.token)
        setUsersSearchResult(response.users)
        console.log(response.users)
        setLoading(false)
    }

    return(
        <Modal show={showContactModal} onHide={handleCloseContactModal} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>Add new contact</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                
                <Form>
                    <Form.Group className="input-group mb-3">
                        <Form.Control
                            type="text"
                            placeholder="Search for username"
                            ref={userSearchInputRef}
                            autoFocus
                        />
                        <Button className="btn-secondary" style={{"minWidth": "42px"}} id="search-input-btn" onClick={handleSearch}>
                            <FontAwesomeIcon icon={faMagnifyingGlass} />
                        </Button>
                    </Form.Group>
                </Form>

                <Container className="d-flex flex-column justify-content-center gap-2" style={{"minHeight": "22em"}}>
                    
                    {
                        loading ? (
                            <Spinner
                                as="span"
                                style={{"minWidth" : "3em", "minHeight" : "3em", "fontSize": "1.3em"}}
                            />
                        ) : (
                        usersSearchResult.length ? (
                            <div className="" style={{"alignSef" : "start"}}>
                                {usersSearchResult.map((user) => (
                                    <NewContactUserCard
                                        key={user.id}
                                        userId={user.id}
                                        username={user.username}
                                        email={user.email}
                                        pictureId={user.picture_id}
                                    />
                                ))}
                            </div>           
                        ) : (
                            <FontAwesomeIcon icon={faMagnifyingGlass} style={{color: "#686e78"}} size="5x"/>
                        ))
                    }
                
                </Container>

            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseContactModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>

    )

}