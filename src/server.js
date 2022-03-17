const express = require('express')
const morgan = require('morgan')
const passport = require('passport')
const cors = require('cors')
const app = express()
const handleError = require('./utils/error-handler')

// server settings
app.set('port', process.env.PORT || 5000)
app.set('api_path', process.env.API_PATH || '/api/v1')

// middlewares
app.use(cors())
app.use(morgan('dev'))
app.use(express.json())

// passport middleware
require('./security/passport')
app.use(passport.initialize())

// routes
app.use(`${app.get('api_path')}/auth`, require('./routes/auth.route'))
//app.use(`${app.get('api_path')}/user`, require('./routes/user.route'))
app.use(`${app.get('api_path')}/pets`, require('./routes/pet.route'))

// error handle
app.use(handleError)

module.exports = app