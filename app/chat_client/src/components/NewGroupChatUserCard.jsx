import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image"
import Button from "react-bootstrap/Button"
import OverlayTrigger from "react-bootstrap/OverlayTrigger"
import Tooltip from "react-bootstrap/Tooltip"
import { getUserPictureFilename } from "../utils/utils.js"
import { useState, useEffect } from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPlus } from "@fortawesome/free-solid-svg-icons"


export default function NewGroupChatUserCard({userId, username, email, pictureId, onClick}){


    const [profilePictureFile, setProfilePictureFile] = useState(null)

    useEffect(() => {
        const fetchProfilePicture = async () => {
            const filename = getUserPictureFilename(pictureId)
            setProfilePictureFile(filename)
        }

        fetchProfilePicture()
    }, [])

    
    function handleAddUser(){
        onClick()
    }

    return (
        <Card body className="bg-dark-subtle border-dark-subtle" key={userId}>
            <div className="d-flex flex-row align-items-center pe-2 gap-3">
                <Image
                    src={profilePictureFile}
                    roundedCircle
                    style={{ width: "3.75em", height: "3.75em" }}
                    className="object-fit-cover"
                />
                <div className="text-truncate">
                    <Card.Title className="fw-medium" style={{ fontSize: "1.25em"}}>{username}</Card.Title>
                    <Card.Text className="text-truncate" style={{ fontSize: "0.825em"}}>{email}</Card.Text>
                </div>
                <div className="ms-auto">
                    <OverlayTrigger
                        placement="left"
                        overlay={<Tooltip>Add to group</Tooltip>}
                    >
                        <Button className="rounded-pill" onClick={handleAddUser}>
                            <FontAwesomeIcon icon={faPlus} size="xs"/>
                        </Button>
                    </OverlayTrigger>
                </div>
            </div>
        </Card>
    )
}