import Modal from "react-bootstrap/Modal"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import Container from "react-bootstrap/Container"
import Spinner from "react-bootstrap/Spinner"
import Table from "react-bootstrap/Table"
import Pagination from "react-bootstrap/Pagination"
import NewGroupChatUserCard from "./NewGroupChatUserCard.jsx"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../contexts/AuthContext.jsx"
import userService from "../services/users.js"
import { useDebounce } from "use-debounce"
import chatsService from "../services/chats.js"
import { useSocket } from "../contexts/SocketsContext.jsx"


export default function NewGroupChatModal({showChatModal, setShowChatModal}){

    const navigate = useNavigate()    
    const socketContext = useSocket()

    const [showUserSearchModal, setShowUserSearchModal] = useState(false)
    const authContext = useAuth()
    const searchLimit = 5
    const [pageAmount, setPageAmount] = useState(0)
    const [currentPage, setCurrentPage] = useState(1)
    const [loading, setLoading] = useState(false)
    const [usersSearchResult, setUsersSearchResult] = useState([])
    const [searchTerm, setSearchTerm] = useState("")
    const [debouncedSearchTerm] = useDebounce(searchTerm, 600)
    const [chatMembers, setChatMembers] = useState([])
    const [groupName, setGroupName] = useState("")
    const [formError, setFormError] = useState("")

    async function searchUsers(offset, search) {
        setLoading(true)
        const response = await userService.search(searchLimit, offset, search, authContext.token, [authContext.userId])
        setUsersSearchResult(response.users)
        setPageAmount(Math.ceil(response.totalCount / searchLimit))        
        setLoading(false)
    }

    function handleCloseGroupCreationModal(){
        setShowChatModal(false)
        setChatMembers([])
        setGroupName("")
        setFormError("")
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

    const handleToggleUserSearchModal = () => {
        setShowChatModal(false)
        setShowUserSearchModal(true)
    }

    const handleToggleGroupCreationModal = () => {
        setShowChatModal(true)
        setShowUserSearchModal(false)
    }

    async function handleCreateChat(){

        // Clear any previous error
        setFormError("")

        if (!groupName) {
            setFormError("Group name is required")
            return
        }

        if (!chatMembers.length) {
            setFormError("At least one member is required")
            return
        }

        const chatMembersIds = chatMembers.map(member => member.id)
        chatMembersIds.push(authContext.userId) // Include the creator in the chat

        if (chatMembersIds.length === 0) {
            return
        }

        const response = await chatsService.createChat({
            isGroup: true,
            groupName: groupName.trim(),
            membersIds: chatMembersIds,
            token: authContext.token
        })
        const chatId = await response.chat.id

        socketContext.socket.emit("create_chat", {
            token: authContext.token,
            detail: {
                chatId: chatId,
                chatMembers: chatMembersIds
            }
        })

        navigate(`/chat/${chatId}`)
    }

    function handleAddUserToChatMembers(user) {
        if (chatMembers.includes(user)) {
            handleToggleGroupCreationModal()
            return
        }

        setChatMembers([...chatMembers, user])
        handleToggleGroupCreationModal()
    }

    return(
        <>

            {/* Group creation modal */}
            <Modal show={showChatModal} onHide={handleCloseGroupCreationModal} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>Add new group chat</Modal.Title>
                </Modal.Header>
                <Modal.Body>

                    {/* Chat members table */}
                    <Form.Label>Group Name *</Form.Label>
                    <Form.Control
                        type="text"
                        value={groupName}
                        onChange={(e) => setGroupName(e.target.value)}
                    />

                    <h5 className="mt-3">Add other members</h5>

                    <Table striped bordered hover size="sm">
                        <thead>
                            <tr>
                            <th className="ps-3">Username</th>
                            <th className="ps-3">Email</th>
                            <th className="ps-3">Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {chatMembers.length === 0 ? (
                                <tr>
                                    <td colSpan={3} className="text-center">No other members added</td>
                                </tr>
                            ) : (
                                chatMembers.map((member) => (
                                    <tr key={member.id}>
                                        <td className="ps-3">{member.username}</td>
                                        <td className="ps-3">{member.email}</td>
                                    <td className="ps-3">
                                        <Button 
                                            variant="link" 
                                            size="sm"
                                            style={{ textDecoration: "none", color: "#dc4545" }}
                                            onClick={() => setChatMembers(chatMembers.filter(m => m.id !== member.id))}
                                        >
                                            Remove
                                        </Button>
                                    </td>
                                </tr>
                            )))
                        }
                        </tbody>
                    </Table>

                    <Button variant="primary" onClick={handleToggleUserSearchModal}>
                        Add member
                    </Button>

                    {formError && (
                        <div className="text-danger mt-3" style={{ fontSize: "0.95rem" }}>
                            {formError}
                        </div>
                    )}

                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={handleCloseGroupCreationModal}>
                        Close
                    </Button>
                    <Button variant="primary" onClick={handleCreateChat}>
                        Save
                    </Button>
                </Modal.Footer>
            </Modal>


            {/* User search modal */}

            <Modal show={showUserSearchModal} onHide={handleToggleGroupCreationModal} size="lg">
                <Modal.Header closeButton>
                    <Modal.Title>Search user</Modal.Title>
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
                                                <NewGroupChatUserCard
                                                    key={user.id}
                                                    userId={user.id}
                                                    username={user.username}
                                                    email={user.email}
                                                    pictureId={user.pictureId}
                                                    onClick={() => handleAddUserToChatMembers(user)}
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
                    <Button variant="secondary" onClick={handleToggleGroupCreationModal}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    )
}
