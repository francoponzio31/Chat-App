import Container from "react-bootstrap/Container"
import Navbar from "../components/Navbar.jsx"
import Message from "../components/Message.jsx"
import Image from "react-bootstrap/Image"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faLocationArrow } from "@fortawesome/free-solid-svg-icons"
import { getUserPictureFilename } from "../utils/utils.js"
import { useParams } from "react-router-dom"
import { useState } from "react"


export default function Home(){
  
    const { chatId } = useParams()
    console.log("chatId:", chatId)

    //? Obtener los datos del chat con sus ultimo mensajes

    return (
        <>
            <Navbar/>
            <Container className="d-flex flex-column">

                <h3 className="mt-3 mb-1">Chat Room</h3>
                
                <div className="d-flex position-relative ms-2" style={{ gap: "0" }}>
                    <Image
                        src={"/files/0d7c65ed-3b98-4ac4-a4d3-748743200aed"}
                        roundedCircle
                        style={{
                            width: "2.15em",
                            height: "2.15em",
                            marginLeft: "-0.5em",
                            zIndex: 2,
                        }}
                        className="object-fit-cover mt-1 border border-dark"
                
                    />
                    <Image
                        src={"/circle-user-solid.svg"}
                        roundedCircle
                        style={{
                            width: "2.15em",
                            height: "2.15em",
                            marginLeft: "-0.5em",
                            zIndex: 1,
                        }}
                        className="object-fit-cover mt-1 border border-dark"
                    />
                </div>
                
                <hr className=""/>
                
                <Container className="d-flex flex-column gap-2 mt-1 overflow-y-auto" style={{ height: "65vh" }}>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"Hola"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"que tal?"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Jose"} content={"Todo bien"} sentTime={"12/09/2024 14:08"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"Hola"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"que tal?"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Jose"} content={"Todo bien"} sentTime={"12/09/2024 14:08"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"Hola"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"que tal?"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Jose"} content={"Todo bien"} sentTime={"12/09/2024 14:08"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"Hola"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"que tal?"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Jose"} content={"Todo bien"} sentTime={"12/09/2024 14:08"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"Hola"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Pepe"} userPictureId={"0d7c65ed-3b98-4ac4-a4d3-748743200aed"} content={"que tal?"} sentTime={"12/09/2024 14:05"}/>
                    <Message userName={"Jose"} content={"Todo bien"} sentTime={"12/09/2024 14:08"}/>
                </Container>
                

                <Form.Group className="input-group mt-4 mb-3">
                    <Form.Control
                        type="text"
                        placeholder="Write a message"
                    />
                    <Button className="btn-primary">
                        <FontAwesomeIcon icon={faLocationArrow} style={{ transform: "rotate(45deg)" }}/>
                    </Button>
                </Form.Group>
            </Container>

        </>
    )
}