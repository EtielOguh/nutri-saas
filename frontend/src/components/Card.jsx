import React from 'react'
import './Card.css'

/**
 * Componente Card genérico
 */
export const Card = ({ title, value, icon, onClick, loading = false }) => {
  return (
    <div className="card" onClick={onClick} style={{ cursor: onClick ? 'pointer' : 'default' }}>
      <div className="card-header">
        {icon && <span className="card-icon">{icon}</span>}
        <h3 className="card-title">{title}</h3>
      </div>
      <div className="card-body">
        {loading ? (
          <div className="card-loading">Carregando...</div>
        ) : (
          <div className="card-value">{value}</div>
        )}
      </div>
    </div>
  )
}

export default Card
