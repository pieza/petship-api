const mongoose = require('mongoose')
const { Schema } = mongoose

const PetSchema = new Schema({
  owner: { type: Schema.Types.ObjectId, ref: 'User', require: true },
  name: { type: String },
  type: { type: String },
  gender: { type: String },
  race: { type: String },
  weight: { type: Number },
  image: { type: String },
  birthday: { type: Date, default: Date.now }
})

module.exports = mongoose.model('Pet', PetSchema)