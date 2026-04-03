import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { PrivateRoute } from './components'
import {
  LoginPage,
  DashboardPage,
  ClientsPage,
  ClientDetailPage,
  SettingsPage
} from './pages'
import './App.css'

/**
 * App.jsx - Configuração de rotas e layout da aplicação
 */
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Rota de Login - Pública */}
          <Route path="/login" element={<LoginPage />} />

          {/* Rotas Protegidas */}
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <DashboardPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/clientes"
            element={
              <PrivateRoute>
                <ClientsPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/clientes/:clientId"
            element={
              <PrivateRoute>
                <ClientDetailPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/clientes/:clientId/editar"
            element={
              <PrivateRoute>
                <ClientDetailPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/clientes/novo"
            element={
              <PrivateRoute>
                <ClientsPage />
              </PrivateRoute>
            }
          />

          <Route
            path="/configuracoes"
            element={
              <PrivateRoute>
                <SettingsPage />
              </PrivateRoute>
            }
          />

          {/* Redirecionamento padrão */}
          <Route path="/" element={<Navigate to="/dashboard" />} />
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
