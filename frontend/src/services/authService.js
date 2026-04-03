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
      email: email,
      senha: senha
    })
    
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('nutricionista', JSON.stringify({
        id: response.data.id,
        nome: response.data.nome,
        email: response.data.email,
        name: response.data.nome, // Compatibilidade
        crn: response.data.crn || null
      }))
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
