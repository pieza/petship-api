const Validator = require('validator')
const isEmpty = require('./is-empty')

module.exports = function validateLoginInput(data) {
  let errors = {}

  data.email = !isEmpty(data.email) ? data.email : ''
  data.password = !isEmpty(data.password) ? data.password : ''

  if (Validator.isEmpty(data.email))
    errors.email = 'El correo es requerido'

  if (!Validator.isEmail(data.email)) 
    errors.email = 'Correo electrónico inválido'

  if (Validator.isEmpty(data.password))
    errors.password ='La contraseña es requerida'

  return {
    errors,
    isValid: isEmpty(errors)
  }
}