const Bot = require('../default-bots/bot.js')

class HelpBot extends Bot {
  constructor (client) {
    super(client, 'help')
  }

  handleMessage (client, message, args) {

  }
}

module.exports = HelpBot
