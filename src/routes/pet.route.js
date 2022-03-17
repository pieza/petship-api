const express = require('express')
const router = express.Router()
const passport = require('passport')
const User = require('../models/user')
const Pet = require('../models/pet')
const validatePetInput =  require('../utils/validators/pet.validator')

router.get('/', async (req, res, next) => {
  try {
    let filters = req.query

    const pets = await Pet.find(filters)

    return res.status(200).json(pets)
  } catch(err) {
    next(err)
  }
})

router.post('/', passport.authenticate('jwt', { session: false }), async (req, res, next) => {
  try {
    const { body, user } = req
    const { errors, isValid } = validatePetInput(body)

    if(!isValid)
      return res.status(422).json({ errors })

    const pet = new Pet({
      ...body,
      owner: user._id
    })

    return res.status(200).json(await pet.save())
  } catch (err) {
    next(err)
  }
})

module.exports = router