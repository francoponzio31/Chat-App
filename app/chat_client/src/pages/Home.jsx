import Container from "react-bootstrap/Container"
import Tab from "react-bootstrap/Tab"
import Tabs from "react-bootstrap/Tabs"
import Navbar from "../components/Navbar.jsx"
import Spinner from "react-bootstrap/Spinner"
import CreateElementBtn from "../components/CreateElementBtn.jsx"
import { DirectChatCard, GroupChatCard} from "../components/ChatCard.jsx"
import NewDirectChatModal from "../components/NewDirectChatModal.jsx"
import NewGroupDirectChatModal from "../components/NewGroupChatModal.jsx"
import chatsService from "../services/chats.js"
import { useAuth } from "../contexts/AuthContext.jsx"
import { useSocket } from "../contexts/SocketsContext.jsx"
import { useState, useEffect } from "react"


function ChatsSection({chatType}){

    const authContext = useAuth()
    const socketContext = useSocket()
    const [userChats, setUserChats] = useState([])
    const [loadingChats, setLoadingChats] = useState(true)
    const [showChatModal, setShowChatModal] = useState(false)
    const handleShowChatModal = () => setShowChatModal(true)
    const getUserChats = async () => {
        try {
            const response = await chatsService.getUserChats({
                limit: 10,
                offset: 0,
                type: chatType,
                token: authContext.token
            })
            const chats = response.chats
            setUserChats(chats)
        } catch (error) {
            console.error("Error fetching data:", error)
        }
    } 

    // useEffect to fetch user chats for first render
    useEffect(() => {
        setLoadingChats(true)
        getUserChats()
        setLoadingChats(false)
    }, [])

    // useEffect to listen for new messages and update chats
    useEffect(() => {
        if (!socketContext.socket || !socketContext.isConnected) {
            console.log("Socket not ready - socket:", !!socketContext.socket, "connected:", socketContext.isConnected)
            return
        }

        const handleNewMessage = (data) => {
            console.log("New message received:", data)
            const newMessage = data

            // If the new message is not in the current chats, update the chats
            if (!userChats.find(chat => chat.id === newMessage.chatId)) {
                getUserChats()
                return
            }

            // Update the state to add a unread message to the chat and move it to the top
            setUserChats(prevChats => {
                let updatedChat = null
                const otherChats = []

                // Find the chat that received the message and separate it from others
                prevChats.forEach(chat => {
                    if (chat.id === newMessage.chatId) {
                        updatedChat = {
                            ...chat,
                            unreadMessages: chat.unreadMessages + 1,
                            lastMessage: newMessage
                        }
                    } else {
                        otherChats.push(chat)
                    }
                })

                // Return array with updated chat first, then other chats
                return updatedChat ? [updatedChat, ...otherChats] : prevChats
            })
        }

        // Add event listeners
        socketContext.socket.on("new_message", handleNewMessage)

        return () => {
            if (socketContext.socket) {
                socketContext.socket.off("new_message", handleNewMessage)
            }
        }
    }, [socketContext.socket, socketContext.isConnected, userChats])

    return <>
        <div 
            className={`d-flex flex-column align-items-center ${!userChats.length || loadingChats ? "justify-content-center" : ""}`} 
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
                    userChats.length ? (
                        <div className="d-flex flex-column w-100" style={{ flexGrow: 1 }}>
                            <div className="d-flex flex-column gap-3" style={{ flexGrow: 1 }}>
                                {                    
                                    userChats.map((chat) => (
                                        chat.isGroup ? (
                                            <GroupChatCard 
                                                    key={chat.id}
                                                    chatId={chat.id}
                                                    chatMembers={chat.chatMembers}
                                                    groupName={chat.groupName}
                                                    unreadMessages={chat.unreadMessages}
                                            />
                                        ) : (
                                            <DirectChatCard 
                                                key={chat.id}
                                                chatId={chat.id}
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
                    <NewDirectChatModal showChatModal={showChatModal} setShowChatModal={setShowChatModal}></NewDirectChatModal>
                </>
            ) : <>
                    <CreateElementBtn tooltip={"Create new chat"} onClickFunction={handleShowChatModal}/>
                    <NewGroupDirectChatModal showChatModal={showChatModal} setShowChatModal={setShowChatModal}></NewGroupDirectChatModal>
                </>
        }
    </>
}


export default function Home(){
    return (
        <>
        <Navbar/>

        <Container>
            <Tabs
                defaultActiveKey="direct"
                className="mt-4 mb-4"
            >
                <Tab eventKey="direct" title="Direct Chats">
                    <ChatsSection chatType={"direct"}/>
                </Tab>
                <Tab eventKey="group" title="Group Chats">
                    <ChatsSection chatType={"group"}/>
                </Tab>
            </Tabs>
            </Container>
        </>
    )
}