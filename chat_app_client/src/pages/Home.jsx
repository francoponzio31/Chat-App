import Container from "react-bootstrap/Container"
import Tab from "react-bootstrap/Tab"
import Tabs from "react-bootstrap/Tabs"
import Navbar from "../components/Navbar.jsx"
import CreateElementBtn from "../components/CreateElementBtn.jsx"
import ChatCard from "../components/ChatCard.jsx"
import ContactCard from "../components/ContactCard.jsx"


export default function Home(){

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
                            <ContactCard/>
                            <CreateElementBtn tooltip={"Add new contact"}/>
                        </Container>
                    </Tab>
                </Tabs>
            </Container>


        </>
    )
}