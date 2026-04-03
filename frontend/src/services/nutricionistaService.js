import api from './api'

/**
 * Serviço de Nutricionista
 */
export const nutricionistaService = {
  /**
   * Obter informações do nutricionista
   */
  getInfo: async (nutricionistaId) => {
    const response = await api.get(`/nutricionistas/${nutricionistaId}`)
    return response.data
  },

  /**
   * Obter dashboard do nutricionista
   */
  getDashboard: async (nutricionistaId) => {
    const response = await api.get(`/nutricionistas/${nutricionistaId}/dashboard`)
    return response.data
  },

  /**
   * Atualizar configurações
   */
  updateConfig: async (nutricionistaId, config) => {
    const response = await api.put(
      `/nutricionistas/${nutricionistaId}/configuracao`,
      config
    )
    return response.data
  },

  /**
   * Upload de logo
   */
  uploadLogo: async (nutricionistaId, file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post(
      `/nutricionistas/${nutricionistaId}/upload-logo`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  }
}

export default nutricionistaService
