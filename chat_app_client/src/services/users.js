import axios from "./axiosConfig"


class UsersService{

    apiPrefix = "/users"

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


    async getProfilePicture(userId, token){
        try {
            const response = await axios.get(`${this.apiPrefix}/picture/${userId}`, {
                headers: {
                    "Authorization": `Bearer ${token}`,
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }    
    }


    async updateProfilePicture(userId, token, content, filename){
        try {
            const response = await axios.put(`${this.apiPrefix}/picture/${userId}`, {filename, content},
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


    async updateUser(userId, token, newData){
        try {
            const response = await axios.patch(`${this.apiPrefix}/${userId}`, newData, {
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