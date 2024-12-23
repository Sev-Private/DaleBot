const Bot = require('.bot.js')

class DBBot extends Bot {
  constructor (client, command) {
    super(client, command)
  }

  handleMessage (client, message, args) {

  }
}

module.exports = DBBot
