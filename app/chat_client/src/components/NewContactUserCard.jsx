import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image"
import { getUserPictureFilename } from "../utils/utils.js"
import { useState, useEffect } from "react"


export default function NewContactUserCard({userId, username, email, pictureId}){

    const [profilePictureFile, setProfilePictureFile] = useState(null)

    useEffect(() => {
        const fetchProfilePicture = async () => {
            const filename = await getUserPictureFilename(pictureId)
            setProfilePictureFile(filename)
        }

        fetchProfilePicture()
    }, [pictureId])

    return (
        <Card body className="" key={userId}>
            <div className="d-flex gap-3 align-items-center">
                <Image
                    src={profilePictureFile}
                    roundedCircle
                    style={{ width: "4.5em", height: "4.5em" }}
                    className="object-fit-cover"
                />
                <div>
                    <Card.Title className="fs-5 fw-medium">{username}</Card.Title>
                    <Card.Text className="" style={{"fontSize": ".9em"}}>{email}</Card.Text>
                </div>
            </div>
        </Card>
    )
}