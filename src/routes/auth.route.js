const express = require('express')
const router = express.Router()
const User = require('../models/user')
const jtw = require('jsonwebtoken')
const passport = require('passport')
const validateSignupInput = require('../utils/validators/signup.validator')
const validateLoginInput = require('../utils/validators/login.validator')

router.get('/logout', (req, res) => {
  req.logout()
})

router.post('/login', async (req, res, next) => {
  try {
    const { errors, isValid } = validateLoginInput(req.body)
    
    // input data is incomplete
    if(!isValid)
      return res.status(422).json({ errors })

    const user = await User.findOne({ email: req.body.email })
    
    // user not exist
    if(!user)
      return res.status(401).json({errors: {password: 'El correo o contraseña son incorrectos'} })
    
    // incorrect password
    if(!user.comparePassword(req.body.password))
      return res.status(401).json({errors: {password: 'El correo o contraseña son incorrectos'} })
    
    // user match
    const payload = user.getSimple()
    
    jtw.sign(payload,
      process.env.SECRET_JWT_KEY, 
      { expiresIn: parseInt(process.env.TOKEN_EXP_TIME || 3600)  }, 
      (err, token) => {
          if(err)
            next(err)
          res.json({
            success: true,
            token: token
          })
      }
    )
  } catch(err) {
    next(err)
  }
})

router.post('/signup', async (req, res, next) => {
  try {
    const { errors, isValid } = validateSignupInput(req.body)
    
    // input data is incomplete
    if(!isValid)
      return res.status(422).json({ errors })

    const userByEmail = await User.findOne({ email: req.body.email })

    // email already exist
    if(userByEmail)
      return res.status(409).json({errors: {email: 'El correo ya está registrado'} })

    // create user
    const newUser = new User({
      name: req.body.name,
      email: req.body.email
    })
    newUser.password = newUser.encryptPassword(req.body.password)

    // save user
    const user = await newUser.save()
    const payload = user.getSimple()
    jtw.sign(payload,
        process.env.SECRET_JWT_KEY, 
        { expiresIn: parseInt(process.env.TOKEN_EXP_TIME || 3600)  }, 
        (err, token) => {
            if(err)
              next(err)
            res.json({
              success: true,
              token: token
            })
        }
      )
  } catch(err) {
    next(err)
  }
})

router.get('/refreshToken', passport.authenticate('jwt', {session: false}), async (req, res) => {
  const user = await User.findById(req.user._id)
  const payload = user.getSimple()
  console.log(user)    
  jtw.sign(payload,
    process.env.SECRET_JWT_KEY, 
    { expiresIn: 3600 }, 
    (err, token) => {
      if(err)
        next(err)
      res.json({
        success: true,
        token: token
      })
    }
  )
})

router.get('/current', passport.authenticate('jwt', {session: false}), async (req, res) => {
  const user = await User.findById(req.user._id)

  if(!user)
    return res.status(401).json({errors: {user: 'Usuario no autenticado'} })
    
  return res.json(await user.getSimple())
})

module.exports = router