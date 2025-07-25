import Container from "react-bootstrap/Container"
import Navbar from "../components/Navbar.jsx"
import Message from "../components/Message.jsx"
import Image from "react-bootstrap/Image"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faLocationArrow } from "@fortawesome/free-solid-svg-icons"
import { getUserPictureFilename } from "../utils/utils.js"
import Spinner from "react-bootstrap/Spinner"
import { useParams } from "react-router-dom"
import { useState, useEffect, useRef } from "react"
import chatsService from "../services/chats.js"
import { useAuth } from "../contexts/AuthContext.jsx"
import { useSocket } from "../contexts/SocketsContext.jsx"
import { format } from "date-fns"
import { toZonedTime } from "date-fns-tz"


const MESSAGES_FETCH_LIMIT = 20

export default function Chat(){
  
    const authContext = useAuth()
    const socketContext = useSocket()
    const { chatId } = useParams()
    const [chat, setChat] = useState(null)
    const [messages, setMessages] = useState([])
    const [isLoadingMoreMessages, setIsLoadingMoreMessages] = useState(false)
    const [hasMoreMessages, setHasMoreMessages] = useState(true)

    const messageInputRef = useRef(null)
    const messagesContainerRef = useRef(null)

    const scrollToBottom = () => {
        if (messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight
        }
    }

    const loadMoreMessages = async () => {
        if (isLoadingMoreMessages || !hasMoreMessages) return

        setIsLoadingMoreMessages(true)
        try {
            const messagesResponse = await chatsService.getChatMessages({ 
                chatId,
                limit: MESSAGES_FETCH_LIMIT,
                offset: messages.length,
                token: authContext.token 
            })
            const newMessages = messagesResponse.messages

            if (newMessages.length === 0) {
                setHasMoreMessages(false)
            } else {
                setMessages(prevMessages => {                    
                    return [...prevMessages, ...newMessages]
                })
            }
        } catch (error) {
            console.error("Error loading more messages:", error)
        } finally {
            setIsLoadingMoreMessages(false)
        }
    }

    useEffect(() => {
        async function fetchChatData() {
            try {
                // Reset state when switching chats
                setMessages([])
                setHasMoreMessages(true)
                setIsLoadingMoreMessages(false)

                const chatResponse = await chatsService.getChatById({ chatId, token: authContext.token })
                setChat(chatResponse.chat)

                const messagesResponse = await chatsService.getChatMessages({ 
                    chatId,
                    limit: MESSAGES_FETCH_LIMIT,
                    offset: 0,
                    token: authContext.token 
                })
                const messages = messagesResponse.messages
                setMessages(messages)
                setHasMoreMessages(messages.length === MESSAGES_FETCH_LIMIT) // If we receive less than 20, there are no more messages

                // set fetched unread messages to read
                const unreadMessages = messages.filter(message => !message.readByUser)
                chatsService.markMessagesAsRead({ messageIds: unreadMessages.map(msg => msg.id), token: authContext.token })

                // Scroll to bottom after messages are loaded
                setTimeout(() => scrollToBottom(), 100)

            } catch (error) {
                console.error("Error fetching chat data:", error)
            }
        }

        if (chatId && authContext.token) {
            fetchChatData()
        }
    }, [chatId, socketContext.socket, socketContext.isConnected, authContext.userId])

    // useEffect to handle scroll and load more messages
    useEffect(() => {
        const messagesContainer = messagesContainerRef.current
        if (!messagesContainer) return

        const handleScroll = () => {
            // If the user is near the top (scrollTop < 100px), load more messages
            if (messagesContainer.scrollTop < 100 && hasMoreMessages && !isLoadingMoreMessages) {
                const previousScrollHeight = messagesContainer.scrollHeight
                const previousScrollTop = messagesContainer.scrollTop

                loadMoreMessages().then(() => {
                    // Maintain scroll position after loading more messages
                    setTimeout(() => {
                        const newScrollHeight = messagesContainer.scrollHeight
                        const scrollDifference = newScrollHeight - previousScrollHeight
                        messagesContainer.scrollTop = previousScrollTop + scrollDifference
                    }, 0)
                })
            }
        }

        messagesContainer.addEventListener('scroll', handleScroll)
        return () => messagesContainer.removeEventListener('scroll', handleScroll)
    }, [hasMoreMessages, isLoadingMoreMessages, messages.length])

    useEffect(() => {
        if (!socketContext.socket || !socketContext.isConnected || !authContext.userId) return

        const handleNewMessage = (messageData) => {
            // Check if the message belongs to the current chat
            if (String(messageData.chatId) !== String(chatId)) return

            setMessages(prevMessages => {
                // Check if the message already exists to avoid duplicates
                const messageExists = prevMessages.some(msg => msg.id === messageData.id)
                if (messageExists) {
                    console.log("Message already exists, not adding duplicate")
                    return prevMessages
                }

                // Set readByUser based on if current user is the sender
                const readByUser = messageData.senderUser.id === parseInt(authContext.userId)
                if (!readByUser) {
                    chatsService.markMessagesAsRead({ messageIds: [messageData.id], token: authContext.token })
                }

                const newMessage = {
                    ...messageData,
                    readByUser: readByUser,
                }
                
                return [newMessage, ...prevMessages]
            })

            console.log("New message added to chat:", messageData)
        }

        socketContext.socket.on("new_message", handleNewMessage)

        // Cleanup: remove event listeners when component unmounts
        return () => {
            if (socketContext.socket) {
                socketContext.socket.off("new_message", handleNewMessage)
            }
        }
    }, [socketContext.socket, socketContext.isConnected, chatId, authContext.userId, authContext.token])

    const handleSendMessage = async () => {
        const messageContent = messageInputRef.current.value.trim()
        if (!messageContent) return

        try {
            const response = await chatsService.sendMessage({
                chatId,
                content: messageContent,
                token: authContext.token
            })
            const sendedMessage = response.newMessage
            console.log("Message sent successfully")

            if (sendedMessage) {
                // Notify other users in the chat room about the new message
                if (socketContext.socket && socketContext.isConnected) {
                    socketContext.socket.emit("send_message", {
                        token: authContext.token,
                        message: {
                            "id": sendedMessage.id,
                            "chatId": sendedMessage.chatId,
                            "content": sendedMessage.content,
                            "senderUser": sendedMessage.senderUser,
                            "sentDate": sendedMessage.sentDate
                        }
                    })
                    console.log("send_message event emitted successfully")
                }
            }
        } catch (error) {
            console.error("Error sending message:", error)
        }

        messageInputRef.current.value = ""
        setTimeout(() => scrollToBottom(), 100)
    }

    if (!chat) {
        return (
            <Container
                className={"d-flex flex-column align-items-center justify-content-center"} 
                style={{"minHeight": "35em"}}
            >
                <Spinner
                    as="span"
                    style={{ minWidth: "3em", minHeight: "3em", fontSize: "1.3em" }}
                />
            </Container>
        )
    }


    const chatName = (
        chat.isGroup ? chat.groupName :
        `Chat room with ${chat.chatMembers.find(member => member.user.id !== parseInt(authContext.userId))?.user.username}`
    )

    return (
        <>
            <Navbar/>
            <Container className="d-flex flex-column">

                <h3 className="mt-3 mb-2 ms-2">{chatName}</h3>

                <div className="d-flex position-relative ms-2" style={{ gap: "0" }}>
                    {chat.chatMembers.map((member, index) => (
                        <Image
                            key={member.user.id}
                            src={getUserPictureFilename(member.user.pictureId)}
                            roundedCircle
                            style={{
                                width: "2.15em",
                                height: "2.15em",
                                marginLeft: index > 0 ? "-0.5em" : "0",
                                zIndex: chat.chatMembers.length - index,
                            }}
                            className="object-fit-cover mt-1 border border-dark"
                        />
                    ))}
                </div>
                
                <hr className=""/>
                
                <Container 
                    ref={messagesContainerRef}
                    className="d-flex flex-column gap-2 mt-1 overflow-y-auto" 
                    style={{ height: "65vh" }}
                >
                    {isLoadingMoreMessages && (
                        <div className="d-flex justify-content-center py-2">
                            <Spinner size="sm" />
                        </div>
                    )}
                    {messages.length > 0 ? (
                        messages.slice().reverse().map(message => {
                            const zonedDate = toZonedTime(new Date(message.sentDate), Intl.DateTimeFormat().resolvedOptions().timeZone)
                            return (
                                <Message
                                    key={message.id}
                                    userName={message.senderUser.username}
                                    userPictureId={message.senderUser.pictureId}
                                    content={message.content}
                                    sentTime={format(zonedDate, 'Pp')}
                                />
                            )
                        })
                    ) : (
                        <span className="text-center fs-5 fw-medium text-muted mt-5">
                            No messages yet. Start the conversation!
                        </span>
                    )}
                </Container>
                
                <Form.Group className="input-group mt-4 mb-3">
                    <Form.Control
                        type="text"
                        placeholder="Write a message"
                        ref={messageInputRef}
                        onKeyDown={e => {
                            if (e.key === "Enter") {
                                e.preventDefault()
                                handleSendMessage()
                            }
                        }}
                    />
                    <Button 
                        className="btn-primary" 
                        onClick={() => {handleSendMessage()}}
                    >
                        <FontAwesomeIcon icon={faLocationArrow} style={{ transform: "rotate(45deg)" }}/>
                    </Button>
                </Form.Group>
            </Container>
        </>
    )
}