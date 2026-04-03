import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { clientService } from '../services'
import { Layout } from '../components'
import './Clients.css'

/**
 * Página de Clientes - Lista com paginação
 */
export const ClientsPage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [search, setSearch] = useState('')
  const [pageSize] = useState(10)

  useEffect(() => {
    loadClients()
  }, [user, page, search])

  const loadClients = async () => {
    if (!user?.id) return

    try {
      setLoading(true)
      setError(null)

      const response = await clientService.listClients(user.id, page, pageSize)
      setClients(response.items || [])
      setTotalPages(response.total_pages || 1)
    } catch (err) {
      console.error('Erro ao carregar clientes:', err)
      setError('Falha ao carregar clientes. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteClient = async (clientId) => {
    if (!window.confirm('Tem certeza que deseja deletar este cliente?')) {
      return
    }

    try {
      await clientService.deleteClient(clientId)
      loadClients() // Recarrega a lista
    } catch (err) {
      console.error('Erro ao deletar cliente:', err)
      alert('Falha ao deletar cliente')
    }
  }

  const handleSearch = (e) => {
    setSearch(e.target.value)
    setPage(1) // Reseta para primeira página
  }

  const filteredClients = clients.filter((client) =>
    client.name.toLowerCase().includes(search.toLowerCase()) ||
    (client.email && client.email.toLowerCase().includes(search.toLowerCase()))
  )

  return (
    <Layout>
      <div className="clients-header">
        <div>
          <h1>Meus Clientes</h1>
          <p>Gerencie todos os seus clientes</p>
        </div>
        <button
          className="btn-primary"
          onClick={() => navigate('/clientes/novo')}
        >
          ➕ Novo Cliente
        </button>
      </div>

      {error && (
        <div className="error-alert">
          ⚠️ {error}
        </div>
      )}

      {/* Filtro de Busca */}
      <div className="search-container">
        <input
          type="text"
          placeholder="🔍 Buscar por nome ou email..."
          value={search}
          onChange={handleSearch}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando clientes...</p>
        </div>
      ) : filteredClients.length > 0 ? (
        <>
          {/* Tabela de Clientes */}
          <div className="table-container">
            <table className="clients-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Telefone</th>
                  <th>Idade</th>
                  <th>Adicionado em</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredClients.map((client) => (
                  <tr key={client.id}>
                    <td className="cell-name">{client.name}</td>
                    <td>{client.email || '-'}</td>
                    <td>{client.phone || '-'}</td>
                    <td>{client.age || '-'}</td>
                    <td>
                      {new Date(client.created_at).toLocaleDateString('pt-BR')}
                    </td>
                    <td className="cell-actions">
                      <button
                        className="btn-action btn-view"
                        onClick={() => navigate(`/clientes/${client.id}`)}
                        title="Ver detalhes"
                      >
                        👁️
                      </button>
                      <button
                        className="btn-action btn-edit"
                        onClick={() => navigate(`/clientes/${client.id}/editar`)}
                        title="Editar"
                      >
                        ✏️
                      </button>
                      <button
                        className="btn-action btn-delete"
                        onClick={() => handleDeleteClient(client.id)}
                        title="Deletar"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Paginação */}
          <div className="pagination">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="pagination-btn"
            >
              ← Anterior
            </button>

            <span className="pagination-info">
              Página {page} de {totalPages}
            </span>

            <button
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page === totalPages}
              className="pagination-btn"
            >
              Próxima →
            </button>
          </div>
        </>
      ) : (
        <div className="empty-state">
          <p>📋 Nenhum cliente encontrado</p>
          {search && <p className="empty-hint">Tente ajustar sua busca</p>}
        </div>
      )}
    </Layout>
  )
}

export default ClientsPage
