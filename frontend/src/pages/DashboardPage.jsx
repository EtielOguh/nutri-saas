import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { nutricionistaService, clientService } from '../services'
import { Layout, Card } from '../components'
import './Dashboard.css'

/**
 * Página Dashboard - Visualização principal com métricas
 */
export const DashboardPage = () => {
  const { user } = useAuth()
  const [dashboard, setDashboard] = useState(null)
  const [clients, setClients] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadDashboard()
  }, [user])

  const loadDashboard = async () => {
    if (!user?.id) return

    try {
      setLoading(true)
      setError(null)

      // Carrega dashboard com métricas
      const dashboardData = await nutricionistaService.getDashboard(user.id)
      setDashboard(dashboardData)

      // Carrega lista de clientes
      const clientsData = await clientService.listClients(user.id, 1, 5)
      setClients(clientsData.items || [])
    } catch (err) {
      console.error('Erro ao carregar dashboard:', err)
      setError('Falha ao carregar dados. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="dashboard-header">
        <h1>Bem-vindo, {user?.name || 'Nutricionista'}!</h1>
        <p>Aqui está um resumo do seu consultório</p>
      </div>

      {error && (
        <div className="error-alert">
          ⚠️ {error}
        </div>
      )}

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando dados...</p>
        </div>
      ) : dashboard ? (
        <>
          {/* Métricas */}
          <section className="metrics-section">
            <h2>Métricas</h2>
            <div className="metrics-grid">
              <Card
                title="Total de Clientes"
                value={dashboard.total_clients}
                icon="👥"
              />
              <Card
                title="Clientes Este Mês"
                value={dashboard.clients_this_month}
                icon="📅"
              />
              <Card
                title="TMB Médio"
                value={dashboard.average_tmb?.toFixed(0) || 'N/A'}
                icon="🔥"
              />
              <Card
                title="Taxa de Retenção"
                value={`${dashboard.retention_rate?.toFixed(1) || '0'}%`}
                icon="📈"
              />
            </div>
          </section>

          {/* Clientes Recentes */}
          {clients.length > 0 && (
            <section className="clients-section">
              <div className="section-header">
                <h2>Clientes Recentes</h2>
                <a href="/clientes" className="view-all-link">Ver todos →</a>
              </div>
              <div className="clients-list">
                {clients.map((client) => (
                  <div key={client.id} className="client-item">
                    <div className="client-info">
                      <h3>{client.name}</h3>
                      <p className="client-meta">
                        Adicionado em {new Date(client.created_at).toLocaleDateString('pt-BR')}
                      </p>
                    </div>
                    <div className="client-actions">
                      <a href={`/clientes/${client.id}`} className="btn-small">
                        Ver Detalhes
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Próximas Ações */}
          <section className="quick-actions">
            <h2>Ações Rápidas</h2>
            <div className="actions-grid">
              <a href="/clientes" className="action-card">
                <span className="action-icon">➕</span>
                <span className="action-text">Novo Cliente</span>
              </a>
              <a href="/configuracoes" className="action-card">
                <span className="action-icon">⚙️</span>
                <span className="action-text">Configurações</span>
              </a>
              <a href="/clientes" className="action-card">
                <span className="action-icon">📊</span>
                <span className="action-text">Ver Relatórios</span>
              </a>
            </div>
          </section>
        </>
      ) : (
        <div className="empty-state">
          <p>Nenhum dado disponível</p>
        </div>
      )}
    </Layout>
  )
}

export default DashboardPage
