import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Login.css'

/**
 * Página de Login
 */
export const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [error, setError] = useState(null)
  const { login, loading } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)

    try {
      await login(email, senha)
      navigate('/dashboard')
    } catch (err) {
      setError('Email ou senha inválidos')
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <span className="login-icon">🌿</span>
          <h1>Nutri SaaS</h1>
          <p>Gerenciador de Clientes Nutricionista</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>
            <input
              id="senha"
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="login-button"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <footer className="login-footer">
          <p>© 2026 Nutri SaaS. Todos os direitos reservados.</p>
        </footer>
      </div>
    </div>
  )
}

export default LoginPage
