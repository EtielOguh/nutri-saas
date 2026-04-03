import React from 'react'
import Header from './Header'
import './Layout.css'

/**
 * Componente de Layout principal
 */
export const Layout = ({ children, sidebar = true }) => {
  return (
    <div className="layout">
      <Header />
      <div className="layout-content">
        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout
