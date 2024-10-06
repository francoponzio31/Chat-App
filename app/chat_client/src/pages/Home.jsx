import Container from "react-bootstrap/Container"
import Tab from "react-bootstrap/Tab"
import Tabs from "react-bootstrap/Tabs"
import Navbar from "../components/Navbar.jsx"
import Spinner from "react-bootstrap/Spinner"
import CreateElementBtn from "../components/CreateElementBtn.jsx"
import { DirectChatCard, GroupChatCard} from "../components/ChatCard.jsx"
import NewChatModal from "../components/NewChatModal.jsx"
import chatsService from "../services/chats.js"
import { useAuth } from "../contexts/AuthContext.jsx"
import { useState, useEffect } from "react"


function ChatsSection({chatType}){

    const authContext = useAuth()
    const [directChats, setDirectChats] = useState([])
    const [loadingChats, setLoadingChats] = useState(true)
    const [showChatModal, setShowChatModal] = useState(false)
    const handleShowChatModal = () => setShowChatModal(true)

    async function getUserChats(){
        setLoadingChats(true)
        try {
            console.log("Fetching chats")
            const response = await chatsService.getUserChats({
                limit: 10,
                offset: 0,
                type: chatType,
                token: authContext.token
            })
            setDirectChats(response.chats)
            setLoadingChats(false)
        } catch (error) {
            console.error("Error fetching data:", error)
        }
    }

    useEffect(() => {
        getUserChats()
    }, [])

    return <>

        <div 
            className={`d-flex flex-column align-items-center ${!directChats.length || loadingChats ? "justify-content-center" : ""}`} 
            style={{"minHeight": "35em"}}
        >
            {
                loadingChats ? (
                    <div className="d-flex align-items-center justify-content-center" style={{ width: "4.5em", height: "4.5em"}}>
                        <Spinner
                            as="span"
                            style={{ minWidth: "3em", minHeight: "3em", fontSize: "1.3em" }}
                        />
                    </div>
                ) : (
                    directChats.length ? (
                        <div className="d-flex flex-column w-100" style={{ flexGrow: 1 }}>
                            <div className="d-flex flex-column gap-3" style={{ flexGrow: 1 }}>
                                {                    
                                    directChats.map((chat) => (
                                        chat.isGroup ? (
                                            <GroupChatCard 
                                                    key={chat.id}
                                                    chatMembers={chat.chatMembers}
                                                    groupName={chat.groupName}
                                                    unreadMessages={chat.unreadMessages}
                                            />
                                        ) : (
                                            <DirectChatCard 
                                                key={chat.id}
                                                chatMembers={chat.chatMembers}
                                                unreadMessages={chat.unreadMessages}
                                            />
                                        )
                                    ))
                                }
                            </div>           
                        </div>
                    ) : (
                        <span className="mt-5 fs-3 fw-medium">No chats yet...</span>
                    )
                )
            }
        </div>

        {
            chatType === "direct" ? (
                <>
                    <CreateElementBtn tooltip={"Create new chat"} onClickFunction={handleShowChatModal}/>
                    <NewChatModal showChatModal={showChatModal} setShowChatModal={setShowChatModal}></NewChatModal>  
                </>
            ) : null    // TODO: creacion de chats grupales
        }
    </>
}


export default function Home(){
    return (
        <>
        <Navbar/>

        <Container>
            <Tabs
                defaultActiveKey="direct-chats"
                className="mt-4 mb-4"
            >
                <Tab eventKey="direct-chats" title="Direct Chats">
                    <ChatsSection chatType={"direct"}/>
                </Tab>
                <Tab eventKey="group-chats" title="Group Chats">
                    <ChatsSection chatType={"group"}/>
                </Tab>

            </Tabs>
            </Container>
        </>
    )
}