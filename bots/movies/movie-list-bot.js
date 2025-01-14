
const Bot = require('../default-bots/bot.js')

class MovieListBot extends Bot {
  constructor (client) {
    super(client, 'help')
  }

  handleMessage (client, message, args) {

  }
}

module.exports = MovieListBot
