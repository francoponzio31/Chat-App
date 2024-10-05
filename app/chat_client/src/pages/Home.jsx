import Container from "react-bootstrap/Container"
import Navbar from "../components/Navbar.jsx"
import CreateElementBtn from "../components/CreateElementBtn.jsx"
import ChatCard from "../components/ChatCard.jsx"
import NewChatModal from "../components/NewChatModal.jsx"
import { useState } from "react"


export default function Home(){

    const [showChatModal, setShowChatModal] = useState(false)
    const handleShowChatModal = () => setShowChatModal(true)
  
    return (
        <>
            <Navbar/>
            <Container>
                <h3 className="my-3">Chats</h3>
                <ChatCard contactName={"Chat 1"} contactUserId={1}/>
            </Container>
            <CreateElementBtn tooltip={"Create new chat"} onClickFunction={handleShowChatModal}/>
            <NewChatModal showChatModal={showChatModal} setShowChatModal={setShowChatModal}></NewChatModal>
        </>
    )
}