import axios from "./axiosConfig"


class ChatsService{

    apiPrefix = "/chats"

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

}

export default new ChatsService()