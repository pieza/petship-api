const Validator = require('validator')
const isEmpty = require('./is-empty')

module.exports = function validatePetInput(data) {
  let errors = {}

  data.name = !isEmpty(data.name) ? data.name : ''
  data.race = !isEmpty(data.race) ? data.race : ''
  data.gender = !isEmpty(data.gender) ? data.gender : ''
      
  if (!Validator.isLength(data.name, { min: 2, max: 30 })) 
    errors.name = 'Inserte un nombre válido(de 2 a 30 caracteres)'
  
  if (Validator.isEmpty(data.name)) 
    errors.name = 'El nombre es requerido'

  if (!Validator.isLength(data.race, { min: 2, max: 30 })) 
    errors.race = 'Inserte una raza válida (de 2 a 30 caracteres)'
  
  if (Validator.isEmpty(data.race)) 
    errors.race = 'La raza es requerida'

  if (!(Validator.equals(data.gender, 'male') || Validator.equals(data.gender, 'female')))
    errors.gender = 'Inserte sexo válido'
  
  if (Validator.isEmpty(data.gender)) 
    errors.gender = 'El sexo es requerido'

  return {
    errors,
    isValid: isEmpty(errors)
  }
}