import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { clientService } from '../services'
import { Layout } from '../components'
import './ClientDetail.css'

/**
 * Página de Detalhe do Cliente
 */
export const ClientDetailPage = () => {
  const { clientId } = useParams()
  const navigate = useNavigate()

  const [client, setClient] = useState(null)
  const [measurements, setMeasurements] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showMeasurementForm, setShowMeasurementForm] = useState(false)
  const [newMeasurement, setNewMeasurement] = useState({
    weight: '',
    height: '',
    waist: '',
    hip: '',
    notes: ''
  })

  useEffect(() => {
    loadClient()
  }, [clientId])

  const loadClient = async () => {
    if (!clientId) return

    try {
      setLoading(true)
      setError(null)

      const clientData = await clientService.getClient(clientId)
      setClient(clientData)

      const measurementsData = await clientService.getMeasurements(clientId)
      setMeasurements(measurementsData || [])
    } catch (err) {
      console.error('Erro ao carregar cliente:', err)
      setError('Falha ao carregar dados do cliente')
    } finally {
      setLoading(false)
    }
  }

  const handleAddMeasurement = async (e) => {
    e.preventDefault()

    if (!newMeasurement.weight) {
      alert('Peso é obrigatório')
      return
    }

    try {
      await clientService.addMeasurement(clientId, {
        ...newMeasurement,
        weight: parseFloat(newMeasurement.weight),
        height: newMeasurement.height ? parseFloat(newMeasurement.height) : null,
        waist: newMeasurement.waist ? parseFloat(newMeasurement.waist) : null,
        hip: newMeasurement.hip ? parseFloat(newMeasurement.hip) : null,
        date: new Date().toISOString()
      })

      setNewMeasurement({
        weight: '',
        height: '',
        waist: '',
        hip: '',
        notes: ''
      })
      setShowMeasurementForm(false)
      loadClient() // Recarrega para atualizar a lista
    } catch (err) {
      console.error('Erro ao adicionar medição:', err)
      alert('Falha ao adicionar medição')
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando cliente...</p>
        </div>
      </Layout>
    )
  }

  if (error || !client) {
    return (
      <Layout>
        <div className="error-container">
          <p>⚠️ {error || 'Cliente não encontrado'}</p>
          <button
            onClick={() => navigate('/clientes')}
            className="btn-back"
          >
            ← Voltar para Clientes
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="client-detail-header">
        <button
          onClick={() => navigate('/clientes')}
          className="btn-back-small"
        >
          ← Voltar
        </button>
        <div>
          <h1>{client.nome}</h1>
          <p className="client-meta">
            Adicionado em {new Date(client.created_at).toLocaleDateString('pt-BR')}
          </p>
        </div>
        <button
          onClick={() => navigate(`/clientes/${clientId}/editar`)}
          className="btn-primary"
        >
          ✏️ Editar Cliente
        </button>
      </div>

      {/* Informações Básicas */}
      <section className="client-info-section">
        <h2>Informações Básicas</h2>
        <div className="info-grid">
          <div className="info-card">
            <label>Email</label>
            <p>{client.email || '-'}</p>
          </div>
          <div className="info-card">
            <label>Telefone</label>
            <p>{client.phone || '-'}</p>
          </div>
          <div className="info-card">
            <label>Idade</label>
            <p>{client.idade || '-'}</p>
          </div>
          <div className="info-card">
            <label>Gênero</label>
            <p>{client.gender || '-'}</p>
          </div>
          <div className="info-card">
            <label>Peso Inicial</label>
            <p>{client.initial_weight ? `${client.initial_weight} kg` : '-'}</p>
          </div>
          <div className="info-card">
            <label>Altura</label>
            <p>{client.altura ? `${client.altura} m` : '-'}</p>
          </div>
        </div>

        {client.notes && (
          <div className="info-notes">
            <h3>Notas</h3>
            <p>{client.notes}</p>
          </div>
        )}
      </section>

      {/* Medições */}
      <section className="measurements-section">
        <div className="section-header">
          <h2>Medições</h2>
          <button
            onClick={() => setShowMeasurementForm(!showMeasurementForm)}
            className="btn-secondary"
          >
            {showMeasurementForm ? '✕ Cancelar' : '➕ Nova Medição'}
          </button>
        </div>

        {showMeasurementForm && (
          <form onSubmit={handleAddMeasurement} className="measurement-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="weight">Peso (kg) *</label>
                <input
                  id="weight"
                  type="number"
                  step="0.1"
                  value={newMeasurement.weight}
                  onChange={(e) => setNewMeasurement({ ...newMeasurement, weight: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="height">Altura (m)</label>
                <input
                  id="height"
                  type="number"
                  step="0.01"
                  value={newMeasurement.height}
                  onChange={(e) => setNewMeasurement({ ...newMeasurement, height: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label htmlFor="waist">Cintura (cm)</label>
                <input
                  id="waist"
                  type="number"
                  step="0.1"
                  value={newMeasurement.waist}
                  onChange={(e) => setNewMeasurement({ ...newMeasurement, waist: e.target.value })}
                />
              </div>
              <div className="form-group">
                <label htmlFor="hip">Quadril (cm)</label>
                <input
                  id="hip"
                  type="number"
                  step="0.1"
                  value={newMeasurement.hip}
                  onChange={(e) => setNewMeasurement({ ...newMeasurement, hip: e.target.value })}
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="notes">Notas</label>
              <textarea
                id="notes"
                value={newMeasurement.notes}
                onChange={(e) => setNewMeasurement({ ...newMeasurement, notes: e.target.value })}
                placeholder="Adicione observações sobre esta medição"
                rows="3"
              />
            </div>
            <button type="submit" className="btn-primary">
              💾 Salvar Medição
            </button>
          </form>
        )}

        {measurements.length > 0 ? (
          <div className="measurements-list">
            {measurements.map((measurement, index) => (
              <div key={measurement.id || index} className="measurement-item">
                <div className="measurement-date">
                  📅 {new Date(measurement.date || measurement.created_at).toLocaleDateString('pt-BR')}
                </div>
                <div className="measurement-data">
                  <span className="measurement-stat">
                    <strong>Peso:</strong> {measurement.weight} kg
                  </span>
                  {measurement.height && (
                    <span className="measurement-stat">
                      <strong>Altura:</strong> {measurement.height} m
                    </span>
                  )}
                  {measurement.waist && (
                    <span className="measurement-stat">
                      <strong>Cintura:</strong> {measurement.waist} cm
                    </span>
                  )}
                  {measurement.hip && (
                    <span className="measurement-stat">
                      <strong>Quadril:</strong> {measurement.hip} cm
                    </span>
                  )}
                </div>
                {measurement.notes && (
                  <div className="measurement-notes">
                    {measurement.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-measurements">
            📊 Nenhuma medição registrada ainda
          </div>
        )}
      </section>
    </Layout>
  )
}

export default ClientDetailPage
