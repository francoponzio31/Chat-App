import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image"
import { getUserPictureFilename } from "../utils/utils.js"
import { useState, useEffect } from "react"


export default function Message({userName, userPictureId, content, sentTime}){

    const [profilePictureFile, setProfilePictureFile] = useState(null)
    useEffect(() => {
        const fetchProfilePicture = async () => {
            const filename = await getUserPictureFilename(userPictureId)
            setProfilePictureFile(filename)
        }

        fetchProfilePicture()
    }, [])

    return (
        <div className="d-flex flex-row gap-2" >
            <Image
                src={profilePictureFile}
                roundedCircle
                style={{ width: "2.75em", height: "2.75em" }}
                className="object-fit-cover mt-1"
            />
            <Card className="bg-dark-subtle border-dark flex-grow-1">
                <Card.Body className="py-2 pe-2">
                    <Card.Title className="mb-1 text-body-secondary" style={{ fontSize: "1.1em"}}>{userName}</Card.Title>
                    <p className="fw-medium lh-sm text-light mb-0" style={{ fontSize: "1em"}}>{content}</p>
                    <span className="text-secondary-emphasis lh-1 ms-auto d-block" style={{ fontSize: ".71em", textAlign: "right" }}>{sentTime}</span>
                </Card.Body>
            </Card>
        </div>
    )

}