import api from './api'

/**
 * Serviço de Clientes
 */
export const clientService = {
  /**
   * Listar clientes de um nutricionista
   */
  listClients: async (nutricionistaId, page = 1, pageSize = 10) => {
    const response = await api.get(`/nutricionistas/${nutricionistaId}/clientes`, {
      params: {
        skip: (page - 1) * pageSize,
        limit: pageSize
      }
    })
    return response.data
  },

  /**
   * Obter detalhe de um cliente
   */
  getClient: async (clienteId) => {
    const response = await api.get(`/clientes/${clienteId}`)
    return response.data
  },

  /**
   * Criar novo cliente
   */
  createClient: async (nutricionistaId, clientData) => {
    const response = await api.post(`/nutricionistas/${nutricionistaId}/clientes`, clientData)
    return response.data
  },

  /**
   * Atualizar cliente
   */
  updateClient: async (clienteId, clientData) => {
    const response = await api.put(`/clientes/${clienteId}`, clientData)
    return response.data
  },

  /**
   * Deletar cliente
   */
  deleteClient: async (clienteId) => {
    const response = await api.delete(`/clientes/${clienteId}`)
    return response.data
  },

  /**
   * Obter medições de um cliente
   */
  getMeasurements: async (clienteId) => {
    const response = await api.get(`/clientes/${clienteId}/medicoes`)
    return response.data
  },

  /**
   * Adicionar medição
   */
  addMeasurement: async (clienteId, measurement) => {
    const response = await api.post(`/clientes/${clienteId}/medicoes`, measurement)
    return response.data
  }
}

export default clientService
