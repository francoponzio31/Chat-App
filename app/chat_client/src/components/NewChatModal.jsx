import Modal from "react-bootstrap/Modal"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import Container from "react-bootstrap/Container"
import Spinner from "react-bootstrap/Spinner"
import Pagination from "react-bootstrap/Pagination"
import NewChatUserCard from "./NewChatUserCard.jsx"
import { useState, useEffect } from "react"
import { useAuth } from "../contexts/AuthContext.jsx"
import userService from "../services/users.js"
import { useDebounce } from "use-debounce"


export default function NewChatModal({showChatModal, setShowChatModal}){

    const authContext = useAuth()
    const searchLimit = 5
    const [pageAmount, setPageAmount] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [loading, setLoading] = useState(false)
    const [usersSearchResult, setUsersSearchResult] = useState([])
    const [searchTerm, setSearchTerm] = useState("")
    const [debouncedSearchTerm] = useDebounce(searchTerm, 600)

    async function searchUsers(offset, search) {
        setLoading(true)
        const response = await userService.search(searchLimit, offset, search, authContext.token)
        setUsersSearchResult(response.users)
        setPageAmount(Math.ceil(response.totalCount / searchLimit))        
        setLoading(false)
    }

    function handleCloseChatModal(){
        setShowChatModal(false)
    }

    function handleSearchInputChange(event) {
        setSearchTerm(event.target.value)
    }

    async function handlePageChange(pageNumber){
        await searchUsers((pageNumber - 1)*searchLimit, debouncedSearchTerm)
        setCurrentPage(pageNumber)
    }

    useEffect(() => {
        searchUsers(0, debouncedSearchTerm)
        setCurrentPage(1)
    }, [debouncedSearchTerm])

    return(
        <Modal show={showChatModal} onHide={handleCloseChatModal} size="lg">
            <Modal.Header closeButton>
                <Modal.Title>Add new chat</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form.Control
                    className="mb-3"
                        type="text"
                        placeholder="Search for username"
                        value={searchTerm}
                        onChange={handleSearchInputChange}
                />
                <Container 
                    className={`d-flex flex-column align-items-center ${!usersSearchResult.length || loading ? "justify-content-center" : ""}`} 
                    style={{"minHeight": "35em"}}
                >
                    {
                        loading ? (
                            <Spinner
                                as="span"
                                style={{ minWidth: "3em", minHeight: "3em", fontSize: "1.3em" }}
                            />
                        ) : (
                            usersSearchResult.length ? (
                                <div className="d-flex flex-column w-100" style={{ flexGrow: 1 }}>
                                    <div className="d-flex flex-column gap-2" style={{ flexGrow: 1 }}>
                                        {usersSearchResult.map((user) => (
                                            <NewChatUserCard
                                                key={user.id}
                                                userId={user.id}
                                                username={user.username}
                                                email={user.email}
                                                pictureId={user.pictureId}
                                            />
                                        ))}
                                    </div>           
                                    <Pagination size="sm" className="align-self-center mt-3 mb-0" style={{ marginTop: "auto" }}>
                                        <Pagination.Prev disabled={currentPage === 1} onClick={() => handlePageChange(currentPage - 1)} />
                                        {
                                            Array.from({ length: pageAmount }, (_, i) => (
                                                <Pagination.Item 
                                                    key={i} 
                                                    active={i+1 === currentPage}
                                                    onClick={() => handlePageChange(i+1)}
                                                >
                                                    {i + 1}
                                                </Pagination.Item>
                                            ))
                                        }
                                        <Pagination.Next disabled={currentPage === pageAmount} onClick={() => handlePageChange(currentPage + 1)} />
                                    </Pagination>
                                </div>
                            ) : (
                                <span className="fs-3 fw-medium">No users found</span>
                            )
                        )
                    }
                
                </Container>

            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseChatModal}>
                    Close
                </Button>
            </Modal.Footer>
        </Modal>
    )
}
