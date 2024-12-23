const {
  joinVoiceChannel,
  entersState,
  createAudioPlayer,
  createAudioResource,
  StreamType,
  AudioPlayerStatus,
  VoiceConnectionStatus
} = require('@discordjs/voice')
const Bot = require('./bot.js')
const ytdl = require('ytdl-core')

class AudioBot extends Bot {
  constructor (client, command) {
    super(client, command)
    this.player = createAudioPlayer()
  }

  sendVoiceMessage (message, url) {
    const connection = joinVoiceChannel({
      channelId: message.member.voice.channel.id,
      guildId: message.guild.id,
      adapterCreator: message.guild.voiceAdapterCreator
    })

    entersState(connection, VoiceConnectionStatus.Ready, 30e3)

    if (url.includes('youtube.com')) {
      url = ytdl(url)
    }

    console.log(url)

    const resource = createAudioResource(url,
      {
        inputType: StreamType.Arbitrary
      })

    this.player.play(resource)

    entersState(this.player, AudioPlayerStatus.Playing, 5e3)

    connection.subscribe(this.player)
  }
}

module.exports = AudioBot
