require('dotenv').config()
const BabyBot = require('./users/baby-bot.js')
const IgorBot = require('./users/igor-bot.js')
const VictorBot = require('./users/victor-bot.js')
const JoaoBot = require('./users/joao-bot.js')
const InstantsBot = require('./misc/instants/instants-bot.js')
const VazaBot = require('./config/vaza-bot.js')
const WorldCupCounterBot = require('./misc/world-cup/world-cup-counter-bot.js')
const RoletaRussaBot = require('./config/roleta-russa-bot')
const FaroBot = require('./misc/rodrigo-faro/faro-bot')

// Comentário Sev: "O Batman"
class BotManager {
  constructor (client) {
    this.client = client

    this.bots = [
      // Users
      new BabyBot(client),
      new IgorBot(client),
      new VictorBot(client),
      new JoaoBot(client),

      // Misc
      new InstantsBot(client),
      new WorldCupCounterBot(client),
      new FaroBot(client),

      // Config
      new VazaBot(client),
      new RoletaRussaBot(client)
    ].reduce(function (map, bot) {
      map[bot.command] = bot
      return map
    }, {})

    client.on('ready', () => {
      this.handleStart()
    })

    client.on('messageCreate', (message) => {
      this.handleMessage(message, this.bots)
    })

    client.login(this.authToken)
  }

  get authToken () {
    return process.env.DISCORD_AUTH_TOKEN
  }

  handleStart () {
    console.log('Connected')
    // client.user.setAvatar('./resources/img/profile-image.jpeg');
  }

  handleMessage (message) {
    console.log('mensagem recebida')

    const content = message.content

    if (content.substring(0, 1) === ';') {
      let args = content.substring(1).split(' ')
      const cmd = args[0]

      args = args.splice(1)
      console.log(cmd)

      const bot = this.bots[cmd]
      if (bot === undefined) return

      bot.handleMessage(message, args)
    }
  }
}

module.exports = BotManager

// TODO: Github add {cmd} {frase}
