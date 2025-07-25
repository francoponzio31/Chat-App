import axios from "./axiosConfig"


class AuthService{

    apiPrefix = "/api/auth"

    async login(email, password){
        try {
            const response = await axios.post(`${this.apiPrefix}/login`, {
                "email": email,
                "password": password,
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
        
    }

    async signup(username, email, password){
        try {
            const response = await axios.post(`${this.apiPrefix}/signup`, {
                "username": username,
                "email": email,
                "password": password,
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
        
    }


    async verifyEmail(userId, token){
        try {
            const response = await axios.post(`${this.apiPrefix}/verify-email/${userId}`, {
                "token": token,
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
        
    }

    async current(token){
        try {
            const response = await axios.get(`${this.apiPrefix}/current`, {
                headers: {
                  Authorization: `Bearer ${token}`,
                }
            })
            return response.data
        } catch (error) {
            console.log(error)
            throw error
        }
        
    }
    
}

export default new AuthService()
