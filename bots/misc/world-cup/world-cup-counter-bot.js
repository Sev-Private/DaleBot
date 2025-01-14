const Bot = require('../../default-bots/bot.js')

class WorldCupCounterBot extends Bot {
  constructor (client) {
    super(client, 'diaspracopa')
    this.startDate = new Date('11/06/2026')
  }

  handleMessage (message, args) {
    const today = new Date()
    const difference = this.startDate.getTime() - today.getTime()
    const days = Math.ceil(difference / (1000 * 3600 * 24))

    const newMessage = 'Faltam ' + days + ' dias para a copa do mundo!'

    super.setNickname(message, 'Dias para copa')
    super.sendTextMessage(message, newMessage)
  }
}

module.exports = WorldCupCounterBot
