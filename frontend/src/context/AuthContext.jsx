import React, { createContext, useContext, useState, useCallback } from 'react'
import { authService } from '../services'

/**
 * Contexto de Autenticação
 */
const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    return authService.getCurrentNutricionista()
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const login = useCallback(async (email, senha) => {
    setLoading(true)
    setError(null)
    try {
      const data = await authService.login(email, senha)
      setUser(data)
      return data
    } catch (err) {
      const message = err.response?.data?.detail || 'Erro ao fazer login'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
    setError(null)
  }, [])

  const isAuthenticated = !!user && authService.isAuthenticated()

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthContext
