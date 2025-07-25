import Card from "react-bootstrap/Card"
import Badge from "react-bootstrap/Badge"
import Image from "react-bootstrap/Image"
import { useAuth } from "../contexts/AuthContext.jsx"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { getUserPictureFilename } from "../utils/utils.js"
import "../index.css"

export function DirectChatCard({chatId, chatMembers, unreadMessages}){

    const navigate = useNavigate()
    const authContext = useAuth()
    const currentUserId = parseInt(authContext.userId)
    const chatPartner = chatMembers.find(member => member.user.id !== currentUserId)

    const [partnerProfilePictureFile, setPartnerProfilePictureFile] = useState(null)

    useEffect(() => {
        const fetchProfilePicture = async () => {
            const filename = getUserPictureFilename(chatPartner.user.pictureId)
            setPartnerProfilePictureFile(filename)
        }

        fetchProfilePicture()
    }, [])

    function handleChatRedirect(chatId){
        navigate(`/chat/${chatId}`)
    }

    return (
        <Card
            body
            onClick={() => handleChatRedirect(chatId)}
            className={`selectable ${unreadMessages ? "bg-black border-primary-subtle" : "bg-secondary-subtle border-dark-subtle"}`}
        >
            <div className="d-flex gap-3 align-items-center justify-content-center">
                <Image
                    src={partnerProfilePictureFile}
                    roundedCircle
                    style={{ width: "3em", height: "3em" }}
                    className="object-fit-cover"
                />
                <Card.Title className="fs-5">
                    {chatPartner.user.username}
                </Card.Title>
                {
                    <div className="ms-auto">
                        {unreadMessages ? <Badge pill className="me-2 bg-primary">{unreadMessages}</Badge> : null}
                    </div>
                }
                
            </div>
        </Card>
    )

}

export function GroupChatCard({chatId, chatMembers, groupName, unreadMessages}){
    
    const navigate = useNavigate()
    function handleChatRedirect(chatId){
        navigate(`/chat/${chatId}`)
    }

    return (
        <Card 
            body
            onClick={() => handleChatRedirect(chatId)}
            className={`selectable ${unreadMessages ? "bg-black border-primary-subtle" : "bg-secondary-subtle border-dark-subtle"}`}
        >
            <div className="d-flex gap-3 align-items-center justify-content-center">
                <Image
                    src="/users-group-solid.svg"
                    style={{ width: "3em", height: "3em" }}
                />
                <Card.Title className="fs-5">
                    {
                        groupName || chatMembers.map(member => member.user.username).join(", ")
                    }
                </Card.Title>
                {
                    <div className="ms-auto">
                        {unreadMessages ? <Badge pill className="me-2 bg-primary">{unreadMessages}</Badge> : null}
                    </div>
                }
                
            </div>
        </Card>
    )

}