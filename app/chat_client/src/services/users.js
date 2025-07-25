import axios from "./axiosConfig"


class UsersService{

    apiPrefix = "/api/users"

    async search(limit, offset, username, token, excludeUsers){
        try {
            const response = await axios.get(`${this.apiPrefix}/`, {
                params: {
                    "limit": limit,
                    "offset": offset,
                    "username": username,
                    "excludeUsers": excludeUsers.join(",") 
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

    async getById(userId, token){
        try {
            const response = await axios.get(`${this.apiPrefix}/${userId}`, {
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


    async updateProfilePicture(token, content, filename){
        try {
            const response = await axios.put(`${this.apiPrefix}/picture`, {filename, content},
            {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error.response
        }
    }


    async updateUser(token, newData){
        try {
            const response = await axios.patch(`${this.apiPrefix}`, newData, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error.response
        }
    }
    
}

export default new UsersService()