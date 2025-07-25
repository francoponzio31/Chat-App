import axios from "./axiosConfig"


class ChatsService{

    apiPrefix = "/api/chats"

    async getUserChats({limit, offset, type, token}){
        try {
            const response = await axios.get(`${this.apiPrefix}/`, {
                params: {
                    limit,
                    offset,
                    type
                },
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }


    async getDirectChatIdWithSecondUser({secondUserId, token}){
        try {
            const response = await axios.get(`${this.apiPrefix}/direct-chat-id-with-user/${secondUserId}`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }


    async getChatById({chatId, token}){
        try {
            const response = await axios.get(`${this.apiPrefix}/${chatId}`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }


    async createChat({isGroup, groupName, membersIds, token}){
        try {
            const response = await axios.post(`${this.apiPrefix}/`, {
                isGroup,
                groupName,
                chatMembersIds: membersIds
            }, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }

    
    async getChatMessages({chatId, limit, offset, token}){
        try {
            const response = await axios.get(`${this.apiPrefix}/${chatId}/messages`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                params: {
                    limit,
                    offset
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }

    async sendMessage({chatId, content, token}){
        try {
            const response = await axios.post(`${this.apiPrefix}/${chatId}/messages`, 
                { content },
                {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            )
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }

    async markMessagesAsRead({messageIds, token}){
        try {
            const response = await axios.post(`${this.apiPrefix}/messages/record-reading`, 
                { "messages_id": messageIds },
                {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json"
                    }
                }
            )
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
    }

}

export default new ChatsService()