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
    logo_url: '',
    valor_consulta: '',
    link_agendamento: ''
  })

  const [nutricionistaData, setNutricionistaData] = useState({
    nome: '',
    crn: ''
  })

  const [logoFile, setLogoFile] = useState(null)
  const [logoPreview, setLogoPreview] = useState(null)
  const fileInputRef = React.useRef(null)

  useEffect(() => {
    loadSettings()
  }, [user])

  const loadSettings = async () => {
    if (!user?.id) return

    try {
      setLoading(true)
      // Atualizar dados do nutricionista (nome e CRN)
      setNutricionistaData({
        nome: user?.nome || user?.name || '',
        crn: user?.crn || ''
      })

      // Tenta carregar configurações
      try {
        const configData = await nutricionistaService.getConfig(user.id)
        setConfig({
          logo_url: configData.logo_url || '',
          valor_consulta: configData.valor_consulta || '',
          link_agendamento: configData.link_agendamento || ''
        })
      } catch (err) {
        // Se não existir configuração, usar padrão
        console.log('Usando configurações padrão')
      }
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
      // Validar tipo de arquivo
      if (!file.type.startsWith('image/')) {
        setError('Por favor selecione uma imagem válida')
        return
      }

      setLogoFile(file)
      const reader = new FileReader()
      reader.onload = (event) => {
        setLogoPreview(event.target?.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleUploadLogo = async (e) => {
    e.preventDefault()

    if (!logoFile) {
      setError('Selecione uma imagem primeiro')
      return
    }

    try {
      setSaving(true)
      setError(null)
      setSuccess(null)

      await nutricionistaService.uploadLogo(user.id, logoFile)
      setSuccess('Logo atualizado com sucesso!')
      setLogoFile(null)
      setLogoPreview(null)
      
      // Recarregar configurações
      await loadSettings()

      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('Erro ao fazer upload do logo:', err)
      setError(err.response?.data?.detail || 'Falha ao fazer upload do logo')
    } finally {
      setSaving(false)
    }
  }

  const handleSaveConfig = async (e) => {
    e.preventDefault()

    // Validações
    if (config.valor_consulta && parseFloat(config.valor_consulta) <= 0) {
      setError('O valor da consulta deve ser maior que zero')
      return
    }

    try {
      setSaving(true)
      setError(null)
      setSuccess(null)

      // Salvar configurações de consulta
      await nutricionistaService.updateConfig(user.id, {
        valor_consulta: config.valor_consulta ? parseFloat(config.valor_consulta) : null,
        link_agendamento: config.link_agendamento || null
      })

      // Salvar dados do nutricionista (nome e CRN)
      if (nutricionistaData.nome || nutricionistaData.crn) {
        await nutricionistaService.updateNutricionista(user.id, {
          nome: nutricionistaData.nome,
          crn: nutricionistaData.crn
        })
      }
      
      setSuccess('Configurações salvas com sucesso!')
      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('Erro ao salvar configurações:', err)
      setError(err.response?.data?.detail || 'Falha ao salvar configurações')
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
      <div className="settings-page">
        <div className="settings-header">
          <h1>Configurações do Perfil</h1>
          <p>Customize sua clínica e preferências</p>
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

        {/* Profile Picture Section - Instagram Style */}
        <section className="profile-picture-section">
          <div className="profile-picture-container">
            <div className="profile-picture">
              {logoPreview ? (
                <img src={logoPreview} alt="Preview da clínica" />
              ) : config.logo_url ? (
                <img src={config.logo_url} alt="Logo da clínica" />
              ) : (
                <div className="picture-placeholder">
                  🏥
                </div>
              )}
              <button
                type="button"
                className="change-picture-btn"
                onClick={() => fileInputRef.current?.click()}
                title="Clique para trocar a foto (como Instagram)"
              >
                📸
              </button>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleLogoSelect}
              style={{ display: 'none' }}
            />
          </div>

          {logoFile && (
            <form onSubmit={handleUploadLogo} className="upload-logo-form">
              <button
                type="submit"
                disabled={saving}
                className="btn-primary w-full"
              >
                {saving ? '⏳ Enviando...' : '✅ Confirmar Nova Foto'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setLogoFile(null)
                  setLogoPreview(null)
                }}
                className="btn-secondary w-full"
              >
                ❌ Cancelar
              </button>
            </form>
          )}
        </section>

        {/* Settings Sections */}
        <div className="settings-grid">
          {/* Dados de Perfil */}
          <section className="settings-section settings-card">
            <h2>Dados Profissionais</h2>
            <form onSubmit={handleSaveConfig}>
              <div className="form-group">
                <label htmlFor="nome">Nome</label>
                <input
                  id="nome"
                  type="text"
                  name="nome"
                  value={nutricionistaData.nome}
                  onChange={(e) => setNutricionistaData({ ...nutricionistaData, nome: e.target.value })}
                  placeholder="Seu nome completo"
                />
              </div>

              <div className="form-group">
                <label htmlFor="crn">CRN (Conselho Regional de Nutricionistas)</label>
                <input
                  id="crn"
                  type="text"
                  name="crn"
                  value={nutricionistaData.crn}
                  onChange={(e) => setNutricionistaData({ ...nutricionistaData, crn: e.target.value })}
                  placeholder="Ex: 123456/SP"
                />
              </div>
            </form>
          </section>

          {/* Configurações de Consulta */}
          <section className="settings-section settings-card">
            <h2>Agendamento & Preços</h2>
            <form onSubmit={handleSaveConfig}>
              <div className="form-group">
                <label htmlFor="valor_consulta">Valor da Consulta (R$)</label>
                <input
                  id="valor_consulta"
                  type="number"
                  name="valor_consulta"
                  value={config.valor_consulta}
                  onChange={handleConfigChange}
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                />
              </div>

              <div className="form-group">
                <label htmlFor="link_agendamento">Link de Agendamento</label>
                <input
                  id="link_agendamento"
                  type="url"
                  name="link_agendamento"
                  value={config.link_agendamento}
                  onChange={handleConfigChange}
                  placeholder="https://seu-agenda-online.com"
                />
              </div>

              <button
                type="submit"
                disabled={saving}
                className="btn-primary w-full"
              >
                {saving ? '⏳ Salvando...' : '💾 Salvar Configurações'}
              </button>
            </form>
          </section>
        </div>

        {/* Account Section */}
        <section className="settings-section settings-card">
          <h2>Conta</h2>
          <div className="account-info">
            <div className="info-item">
              <label>Email (Não pode ser alterado)</label>
              <p>{user?.email || '-'}</p>
            </div>
          </div>

          <div className="danger-zone">
            <h3>Zona de Perigo</h3>
            <button
              onClick={handleLogout}
              className="btn-danger w-full"
            >
              🚪 Sair da Conta
            </button>
          </div>
        </section>
      </div>
    </Layout>
  )
}

export default SettingsPage
