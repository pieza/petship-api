const Validator = require('validator')
const isEmpty = require('./is-empty')

module.exports = function validateSignupInput(data) {
  let errors = {}

  data.name = !isEmpty(data.name) ? data.name : ''
  data.email = !isEmpty(data.email) ? data.email : ''
  data.password = !isEmpty(data.password) ? data.password : ''
  data.confirmPassword = !isEmpty(data.confirmPassword) ? data.confirmPassword : ''
      
  if (!Validator.isLength(data.name, { min: 2, max: 30 })) 
    errors.name = 'Nombre inválido (de 2 a 30 caracteres)'
  
  if (Validator.isEmpty(data.name)) 
    errors.name = 'El nombre es requerido'

  if (Validator.isEmpty(data.email))
    errors.email = 'El correo es requerido'
  
  if (!Validator.isEmail(data.email)) 
    errors.email = 'Correo electrónico inválido'

  if (Validator.isEmpty(data.password))
    errors.password ='La contraseña es requerida'
  
  if (!Validator.isLength(data.password, { min: 5, max: 50 }))
    errors.password ='La contraseña no es segura'

  if (Validator.isEmpty(data.confirmPassword)) 
    errors.confirmPassword = 'Confirmar contraseña es requerido'
      
  else if (!Validator.equals(data.password, data.confirmPassword)) 
    errors.confirmPassword = 'Las contraseñas no coinciden'

  return {
    errors,
    isValid: isEmpty(errors)
  }
}