const mongoose = require('mongoose')
const { Schema } = mongoose
const bcrypt = require('bcrypt')

const UserSchema = new Schema({
  name: { type: String, required: true },
  email: { type: String, required: true },
  password: { type: String, required: true }
})

UserSchema.methods.encryptPassword = (password) => {
  return bcrypt.hashSync(password, bcrypt.genSaltSync(10))
}

UserSchema.methods.comparePassword = function (password) {
  return bcrypt.compareSync(password, this.password)
}


UserSchema.methods.getSimple = function () {
  return { 
    _id: this._id,
    name: this.name,
    email: this.email
  }
}

module.exports = mongoose.model('User', UserSchema)