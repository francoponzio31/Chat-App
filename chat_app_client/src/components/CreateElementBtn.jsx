import Button from "react-bootstrap/Button"
import OverlayTrigger from "react-bootstrap/OverlayTrigger"
import Tooltip from "react-bootstrap/Tooltip"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPlus } from "@fortawesome/free-solid-svg-icons"
import "../index.css"


export default function CreateElementBtn({tooltip}){

    return (
        <OverlayTrigger
            placement="left"
            overlay={<Tooltip>{tooltip}</Tooltip>}
        >
            <Button className="rounded-pill floating-btn" size="lg">
                <FontAwesomeIcon icon={faPlus} size="xs"/>
            </Button>
        </OverlayTrigger>
    )
}