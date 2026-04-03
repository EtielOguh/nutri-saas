import api from './api'

/**
 * Serviço de Autenticação
 */
export const authService = {
  /**
   * Login de nutricionista
   */
  login: async (email, senha) => {
    const response = await api.post('/auth/login', {
      username: email,
      password: senha
    })
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('nutricionista', JSON.stringify(response.data.nutricionista))
    }
    
    return response.data
  },

  /**
   * Logout
   */
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('nutricionista')
  },

  /**
   * Verificar se está autenticado
   */
  isAuthenticated: () => {
    return !!localStorage.getItem('token')
  },

  /**
   * Obter dados do nutricionista autenticado
   */
  getCurrentNutricionista: () => {
    const data = localStorage.getItem('nutricionista')
    return data ? JSON.parse(data) : null
  }
}

export default authService
