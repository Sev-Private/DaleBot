require('dotenv').config()
const Bot = require('../default-bots/bot.js')
const utils = require('../helpers/utils.js')
const { Client } = require('pg')

class PersonBot extends Bot {
  constructor (client, command, name) {
    super(client, command)
    this.name = name
    this.dbCredentials = {
      connectionString: process.env.DB_CONNECTION,
      ssl: {
        rejectUnauthorized: false
      }
    }
  }

  // TODO
  addPhrase () {

  }

  handleMessage (message, args) {
    this.getTableData(message, args)
  }

  sendMessage (message, args, phrases) {
    const newMessage = utils.getRandomFromArray(phrases)

    const that = this
    super.setNickname(message, that.name)
      .then(() => {
        super.sendTextMessage(message,
          newMessage,
          that.formatOptions(args))
      })
      .catch(err => { console.log('Error on sending message', err) })
  }

  formatOptions (args) {
    const tts = args.includes('tts')
    return { tts: tts }
  }

  async getTableData (message, args) {
    const dbClient = new Client(this.dbCredentials)
    await dbClient.connect()

    const query = "SELECT frase from Palhassada where otario = '{0}'".format(this.command)
    const results = await dbClient.query(query)

    const items = results.rows.map(function (row) {
      return row.frase
    })

    this.sendMessage(message, args, items)

    await dbClient.end()
  }
}

module.exports = PersonBot
