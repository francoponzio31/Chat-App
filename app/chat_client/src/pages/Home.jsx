import Container from "react-bootstrap/Container"
import Tab from "react-bootstrap/Tab"
import Tabs from "react-bootstrap/Tabs"
import Navbar from "../components/Navbar.jsx"
import CreateElementBtn from "../components/CreateElementBtn.jsx"
import ChatCard from "../components/ChatCard.jsx"
import ContactCard from "../components/ContactCard.jsx"
import NewContactModal from "../components/NewContactModal.jsx"
import { useState } from "react"


export default function Home(){

    const [showContactModal, setShowContactModal] = useState(false)
    const handleShowContactModal = () => setShowContactModal(true)
  
    return (
        <>
            <Navbar/>

            <Container>
                <Tabs
                    defaultActiveKey="chats"
                    id="uncontrolled-tab-example"
                    className="my-3"
                >
                    <Tab eventKey="chats" title="Chats">
                        <Container>
                            <ChatCard/>
                            <CreateElementBtn tooltip={"Add new chat"}/>
                        </Container>
                    </Tab>
                    <Tab eventKey="contacts" title="Contacts">
                        <Container>
                            <ContactCard contactName={"Contact 1"} contactUserId={1}/>
                            <CreateElementBtn tooltip={"Add new contact"} onClickFunction={handleShowContactModal}/>
                        </Container>
                        <NewContactModal showContactModal={showContactModal} setShowContactModal={setShowContactModal}></NewContactModal>
                    </Tab>
                </Tabs>
            </Container>
        </>
    )
}