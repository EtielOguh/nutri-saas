import React, { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { nutricionistaService } from '../services'
import { Layout } from '../components'
import './Settings.css'

/**
 * Página de Configurações
 */
export const SettingsPage = () => {
  const { user, logout } = useAuth()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const [config, setConfig] = useState({
    crn: '',
    specialties: '',
    consultation_link: '',
    bio: ''
  })

  const [logoFile, setLogoFile] = useState(null)
  const [logoPreview, setLogoPreview] = useState(null)

  useEffect(() => {
    loadSettings()
  }, [user])

  const loadSettings = async () => {
    if (!user?.id) return

    try {
      setLoading(true)
      const data = await nutricionistaService.getInfo(user.id)
      setConfig({
        crn: data.crn || '',
        specialties: data.specialties || '',
        consultation_link: data.consultation_link || '',
        bio: data.bio || ''
      })
    } catch (err) {
      console.error('Erro ao carregar configurações:', err)
      setError('Falha ao carregar configurações')
    } finally {
      setLoading(false)
    }
  }

  const handleConfigChange = (e) => {
    const { name, value } = e.target
    setConfig((prev) => ({
      ...prev,
      [name]: value
    }))
  }

  const handleLogoSelect = (e) => {
    const file = e.target.files?.[0]
    if (file) {
      setLogoFile(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setLogoPreview(event.target?.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSaveConfig = async (e) => {
    e.preventDefault()

    try {
      setSaving(true)
      setError(null)
      setSuccess(null)

      await nutricionistaService.updateConfig(user.id, config)
      setSuccess('Configurações salvas com sucesso!')

      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('Erro ao salvar configurações:', err)
      setError('Falha ao salvar configurações')
    } finally {
      setSaving(false)
    }
  }

  const handleUploadLogo = async (e) => {
    e.preventDefault()

    if (!logoFile) {
      alert('Selecione uma imagem primeiro')
      return
    }

    try {
      setSaving(true)
      setError(null)

      await nutricionistaService.uploadLogo(user.id, logoFile)
      setSuccess('Logo atualizado com sucesso!')
      setLogoFile(null)
      setLogoPreview(null)

      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('Erro ao fazer upload do logo:', err)
      setError('Falha ao fazer upload do logo')
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = async () => {
    if (window.confirm('Deseja realmente sair?')) {
      logout()
    }
  }

  if (loading) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando configurações...</p>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="settings-header">
        <h1>Configurações</h1>
        <p>Gerencie as configurações do seu perfil</p>
      </div>

      {error && (
        <div className="error-alert">
          ⚠️ {error}
        </div>
      )}

      {success && (
        <div className="success-alert">
          ✅ {success}
        </div>
      )}

      <div className="settings-grid">
        {/* Logo */}
        <section className="settings-section">
          <h2>Logo da Clínica</h2>
          <form onSubmit={handleUploadLogo} className="logo-form">
            <div className="logo-preview">
              {logoPreview ? (
                <img src={logoPreview} alt="Preview" />
              ) : (
                <div className="logo-placeholder">
                  📸
                </div>
              )}
            </div>
            <div className="form-group">
              <label htmlFor="logo">Selecionar imagem</label>
              <input
                id="logo"
                type="file"
                accept="image/*"
                onChange={handleLogoSelect}
              />
            </div>
            <button
              type="submit"
              disabled={!logoFile || saving}
              className="btn-primary"
            >
              {saving ? 'Enviando...' : '⬆️ Enviar Logo'}
            </button>
          </form>
        </section>

        {/* Configurações Básicas */}
        <section className="settings-section">
          <h2>Informações Profissionais</h2>
          <form onSubmit={handleSaveConfig}>
            <div className="form-group">
              <label htmlFor="crn">CRN</label>
              <input
                id="crn"
                type="text"
                name="crn"
                value={config.crn}
                onChange={handleConfigChange}
                placeholder="123456/UF"
              />
            </div>

            <div className="form-group">
              <label htmlFor="specialties">Especialidades</label>
              <textarea
                id="specialties"
                name="specialties"
                value={config.specialties}
                onChange={handleConfigChange}
                placeholder="Ex: Nutrição Clínica, Esportes, Infantil"
                rows="3"
              />
            </div>

            <div className="form-group">
              <label htmlFor="consultation_link">Link de Consulta</label>
              <input
                id="consultation_link"
                type="url"
                name="consultation_link"
                value={config.consultation_link}
                onChange={handleConfigChange}
                placeholder="https://seu-link-consulta.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                name="bio"
                value={config.bio}
                onChange={handleConfigChange}
                placeholder="Descrição sobre você e sua prática"
                rows="4"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="btn-primary"
            >
              {saving ? 'Salvando...' : '💾 Salvar Configurações'}
            </button>
          </form>
        </section>
      </div>

      {/* Conta */}
      <section className="settings-section">
        <h2>Conta</h2>
        <div className="account-info">
          <div className="info-item">
            <label>Nome</label>
            <p>{user?.name || '-'}</p>
          </div>
          <div className="info-item">
            <label>Email</label>
            <p>{user?.email || '-'}</p>
          </div>
        </div>

        <div className="danger-zone">
          <h3>Zona de Perigo</h3>
          <button
            onClick={handleLogout}
            className="btn-danger"
          >
            🚪 Sair da Conta
          </button>
        </div>
      </section>
    </Layout>
  )
}

export default SettingsPage
