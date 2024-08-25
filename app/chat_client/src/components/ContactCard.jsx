import Card from "react-bootstrap/Card"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faCircleUser } from "@fortawesome/free-solid-svg-icons"
import "../index.css"

export default function ContactCard({contactName, contactUserId}){

    return (
        <Card body className="" data-user-id={contactUserId}>
            <div className="d-flex gap-3 align-items-center">
                <FontAwesomeIcon icon={faCircleUser} style={{ fontSize: "2.5em" }}/>
                <Card.Title className="fs-4">{contactName}</Card.Title>
            </div>
        </Card>
    )

}