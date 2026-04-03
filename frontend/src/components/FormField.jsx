import React from 'react'
import './FormField.css'

/**
 * Componente de campo de formulário reutilizável
 */
export const FormField = ({
  label,
  name,
  type = 'text',
  value,
  onChange,
  required = false,
  placeholder,
  error,
  disabled = false,
  options,
  rows,
  min,
  max,
  step,
}) => {
  const isSelect = type === 'select'
  const isTextarea = type === 'textarea'

  return (
    <div className="form-field">
      {label && (
        <label htmlFor={name} className="form-label">
          {label} {required && <span className="required">*</span>}
        </label>
      )}

      {isSelect ? (
        <select
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className={`form-input ${error ? 'error' : ''}`}
        >
          <option value="">Selecione uma opção</option>
          {options?.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ) : isTextarea ? (
        <textarea
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          disabled={disabled}
          placeholder={placeholder}
          rows={rows || 4}
          className={`form-input ${error ? 'error' : ''}`}
        />
      ) : (
        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          disabled={disabled}
          placeholder={placeholder}
          required={required}
          min={min}
          max={max}
          step={step}
          className={`form-input ${error ? 'error' : ''}`}
        />
      )}

      {error && <span className="form-error">{error}</span>}
    </div>
  )
}

export default FormField
