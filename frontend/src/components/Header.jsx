import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Header.css'

/**
 * Componente de Header/Navbar
 */
export const Header = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="header-logo">
          <span className="logo-icon">🌿</span>
          <span className="logo-text">Nutri SaaS</span>
        </Link>

        {user && (
          <nav className="header-nav">
            <Link to="/dashboard" className="nav-link">Dashboard</Link>
            <Link to="/clientes" className="nav-link">Clientes</Link>
          </nav>
        )}

        <div className="header-user">
          {user && (
            <>
              <span className="user-name">{user.nome}</span>
              <button onClick={handleLogout} className="logout-btn">
                Sair
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
