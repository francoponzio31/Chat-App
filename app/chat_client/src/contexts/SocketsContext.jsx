import { createContext, useContext, useState, useEffect } from "react"
import client from "socket.io-client"
import { useAuth } from "../contexts/AuthContext.jsx"



const BASE_URL = import.meta.env.VITE_API_BASE_URL

export const SocketsContext = createContext(null)

export const useSocket = () => {
    const context = useContext(SocketsContext)
    if (!context) {
      throw new Error("useSocket must be used within a SocketsProvider")
    }
    return context
}

export function SocketsProvider({ children }) {
    const [socket, setSocket] = useState(null)
    const [isConnected, setIsConnected] = useState(false)
    const authContext = useAuth()

    useEffect(() => {
        if (!authContext.token || !authContext.userId) {
            console.log("No token or userId available, skipping socket connection")
            return
        }

        console.log("Initializing socket connection to:", BASE_URL)
        
        const newSocket = client(BASE_URL, {
            auth: {
                "token": authContext.token,
            },
        })

        // Connection event handlers
        newSocket.on("connect", () => {
            console.log("Connected to server, socket ID:", newSocket.id)
            setIsConnected(true)
        })

        newSocket.on("connected", (data) => {
            console.log("Server confirmed connection")
        })

        newSocket.on("disconnect", (reason) => {
            console.log("Disconnected from server:", reason)
            setIsConnected(false)
        })

        newSocket.on("connect_error", (error) => {
            console.error("Connection error:", error)
            setIsConnected(false)
        })

        newSocket.on("error", (error) => {
            console.error("Socket error:", error)
        })

        newSocket.on("chat_created", (data) => {
            const chatMembers = data.chatMembers || []
            if (chatMembers.includes(authContext.userId)) {
                console.log("Chat created event received, joining chat room:", data.chatId)
                newSocket.emit("join_chat", {
                    token: authContext.token,
                    detail: {
                        chatId: data.chatId
                    }
                })
            }
        })

        setSocket(newSocket)

        return () => {
            console.log("Cleaning up socket connection")
            newSocket.disconnect()
            setSocket(null)
            setIsConnected(false)
        }
    }, [authContext.token, authContext.userId])

    return (
        <SocketsContext.Provider value={{ socket, isConnected }}>
            {children}
        </SocketsContext.Provider>
    )
}