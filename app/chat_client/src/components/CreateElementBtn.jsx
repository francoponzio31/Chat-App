import Button from "react-bootstrap/Button"
import OverlayTrigger from "react-bootstrap/OverlayTrigger"
import Tooltip from "react-bootstrap/Tooltip"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faPlus } from "@fortawesome/free-solid-svg-icons"


export default function CreateElementBtn({tooltip, onClickFunction}){

    return (
        <OverlayTrigger
            placement="left"
            overlay={<Tooltip>{tooltip}</Tooltip>}
        >
            <Button className="rounded-pill floating-btn" size="lg" onClick={onClickFunction}>
                <FontAwesomeIcon icon={faPlus} size="xs"/>
            </Button>
        </OverlayTrigger>
    )
}