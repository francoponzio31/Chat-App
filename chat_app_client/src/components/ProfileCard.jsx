import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image"
import Spinner from "react-bootstrap/Spinner"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faCircleUser } from "@fortawesome/free-solid-svg-icons"


export default function ProfileCard({username, userEmail, profilePicture, loading}){
    return (
        <Card body className="">
            <div className="d-flex gap-3 align-items-center">
                {
                    loading ? (
                        <div className="d-flex align-items-center justify-content-center" style={{ width: "4.5em", height: "4.5em"}}>
                            <Spinner animation="border">
                                <span className="visually-hidden">Loading...</span>
                            </Spinner>
                        </div>
                    ) : profilePicture ? (
                        <Image
                            src={`data:image/png;base64,${profilePicture}`}
                            roundedCircle
                            style={{ width: "4.5em", height: "4.5em" }}
                            className="object-fit-cover"
                        />
                    ) : (
                        <FontAwesomeIcon icon={faCircleUser} style={{ fontSize: "4.5em" }}/>
                    )
                }
                
                <div>
                    <Card.Title className="fs-4">{username}</Card.Title>
                    <Card.Text>{userEmail}</Card.Text>
                </div>
            </div>
        </Card>
    )
}