const {
  Client,
  Intents
} = require('discord.js')
const BotManager = require('./bots/bot-manager.js')

// Initialize Discord Bot
const client = new Client({
  intents: [
    Intents.FLAGS.GUILDS,
    Intents.FLAGS.GUILD_MEMBERS,
    Intents.FLAGS.GUILD_MESSAGES,
    Intents.FLAGS.GUILD_VOICE_STATES
  ]
})
new BotManager(client)