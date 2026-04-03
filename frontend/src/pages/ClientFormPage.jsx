import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { clientService } from '../services'
import { Layout, FormField, Button } from '../components'
import './ClientForm.css'

/**
 * Página de Criar/Editar Cliente
 */
export const ClientFormPage = ({ isEdit = false, clientId = null }) => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)
  const [initialLoading, setInitialLoading] = useState(isEdit)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    age: '',
    gender: 'outro',
    initial_weight: '',
    height: '',
    objective: '',
    notes: '',
  })

  useEffect(() => {
    if (isEdit && clientId) {
      loadClient()
    }
  }, [clientId, isEdit])

  const loadClient = async () => {
    try {
      setInitialLoading(true)
      const client = await clientService.getClient(clientId)
      setFormData({
        name: client.name || '',
        email: client.email || '',
        phone: client.phone || '',
        age: client.age || '',
        gender: client.gender || 'outro',
        initial_weight: client.initial_weight || '',
        height: client.height || '',
        objective: client.objective || '',
        notes: client.notes || '',
      })
    } catch (err) {
      console.error('Erro ao carregar cliente:', err)
      setError('Falha ao carregar dados do cliente')
    } finally {
      setInitialLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.name || !formData.email) {
      setError('Nome e email são obrigatórios')
      return
    }

    try {
      setLoading(true)
      setError(null)

      if (isEdit && clientId) {
        // Editar cliente
        await clientService.updateClient(clientId, {
          ...formData,
          age: formData.age ? parseInt(formData.age) : null,
          initial_weight: formData.initial_weight ? parseFloat(formData.initial_weight) : null,
          height: formData.height ? parseFloat(formData.height) : null,
        })
        navigate(`/clientes/${clientId}`)
      } else {
        // Criar novo cliente
        const response = await clientService.createClient(user.id, {
          nutricionista_id: user.id,
          ...formData,
          age: formData.age ? parseInt(formData.age) : null,
          initial_weight: formData.initial_weight ? parseFloat(formData.initial_weight) : null,
          height: formData.height ? parseFloat(formData.height) : null,
        })
        navigate(`/clientes/${response.id}`)
      }
    } catch (err) {
      console.error('Erro ao salvar cliente:', err)
      setError(err.response?.data?.detail || 'Falha ao salvar cliente')
    } finally {
      setLoading(false)
    }
  }

  if (initialLoading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando cliente...</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="client-form-header">
        <h1>{isEdit ? '✏️ Editar Cliente' : '➕ Novo Cliente'}</h1>
        <p>{isEdit ? 'Atualize as informações do cliente' : 'Preencha os dados do novo cliente'}</p>
      </div>

      {error && (
        <div className="error-alert">
          ⚠️ {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="client-form">
        {/* Informações Pessoais */}
        <section className="form-section">
          <h2>Informações Pessoais</h2>

          <div className="form-row">
            <div className="form-col">
              <FormField
                label="Nome Completo"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                placeholder="João Silva"
                required
              />
            </div>
            <div className="form-col">
              <FormField
                label="Email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="joao@email.com"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-col">
              <FormField
                label="Telefone"
                name="phone"
                type="tel"
                value={formData.phone}
                onChange={handleChange}
                placeholder="(11) 99999-9999"
              />
            </div>
            <div className="form-col">
              <FormField
                label="Idade"
                name="age"
                type="number"
                value={formData.age}
                onChange={handleChange}
                min="0"
                max="150"
              />
            </div>
            <div className="form-col">
              <FormField
                label="Gênero"
                name="gender"
                type="select"
                value={formData.gender}
                onChange={handleChange}
                options={[
                  { value: 'masculino', label: 'Masculino' },
                  { value: 'feminino', label: 'Feminino' },
                  { value: 'outro', label: 'Outro' },
                ]}
              />
            </div>
          </div>
        </section>

        {/* Dados Físicos */}
        <section className="form-section">
          <h2>Dados Físicos</h2>

          <div className="form-row">
            <div className="form-col">
              <FormField
                label="Peso Inicial (kg)"
                name="initial_weight"
                type="number"
                value={formData.initial_weight}
                onChange={handleChange}
                step="0.1"
                min="0"
              />
            </div>
            <div className="form-col">
              <FormField
                label="Altura (m)"
                name="height"
                type="number"
                value={formData.height}
                onChange={handleChange}
                step="0.01"
                min="0"
                max="3"
                placeholder="1.75"
              />
            </div>
          </div>
        </section>

        {/* Objetivo e Notas */}
        <section className="form-section">
          <h2>Objetivo e Observações</h2>

          <FormField
            label="Objetivo"
            name="objective"
            type="textarea"
            value={formData.objective}
            onChange={handleChange}
            placeholder="Ex: Perder peso, ganhar massa muscular,alimentação balanceada"
            rows="3"
          />

          <FormField
            label="Notas Adicionais"
            name="notes"
            type="textarea"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Informações importantes sobre o cliente, alergias, restrições, etc."
            rows="3"
          />
        </section>

        {/* Botões */}
        <div className="form-actions">
          <Button
            type="button"
            variant="secondary"
            onClick={() => navigate(isEdit ? `/clientes/${clientId}` : '/clientes')}
          >
            ← Cancelar
          </Button>
          <Button
            type="submit"
            variant="primary"
            loading={loading}
          >
            {isEdit ? '💾 Salvar Alterações' : '✅ Criar Cliente'}
          </Button>
        </div>
      </form>
    </Layout>
  )
}

export default ClientFormPage
