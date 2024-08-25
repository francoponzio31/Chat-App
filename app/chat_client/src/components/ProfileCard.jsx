import Card from "react-bootstrap/Card"
import Image from "react-bootstrap/Image"
import Spinner from "react-bootstrap/Spinner"


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
                    ) : (
                        <Image
                            src={profilePicture}
                            roundedCircle
                            style={{ width: "4.5em", height: "4.5em" }}
                            className="object-fit-cover"
                        />
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