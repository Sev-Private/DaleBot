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
const ytdl = require('@distube/ytdl-core')
const fs = require('fs')

class AudioBot extends Bot {
  constructor (client, command) {
    super(client, command)
    this.player = createAudioPlayer()
  }

  sendVoiceMessage(message, url) {
    
    if (message.member.voice.channel == null) {
      this.sendTextMessage(message, "Conecta num canal de audio primeiro doidão")
      return
    }

    const connection = joinVoiceChannel({
      channelId: message.member.voice.channel.id,
      guildId: message.guild.id,
      adapterCreator: message.guild.voiceAdapterCreator
    })

    if (url.includes('youtube.com')) {
      url = ytdl(url, {
        filter: 'audioonly',
        highWaterMark: 1 << 25, // Increase buffer size to avoid premature end
        dlChunkSize: 0 // Stream directly without chunking
      })
    }
    
    const audioResource = createAudioResource(url, { inlineVolume: true })

    const player = createAudioPlayer()

    entersState(connection, VoiceConnectionStatus.Ready, 30000)
      .then(() => {
        player.stop()
        connection.subscribe(player)
        player.play(audioResource)
      })
      .catch(error => {
        console.error('Error connecting to voice channel:', error)
        connection.destroy() // Cleanup
      })

    // Listen for player events
    player.on(AudioPlayerStatus.Playing, () => {
      console.log('The audio is now playing!')
    })

    player.on(AudioPlayerStatus.Idle, () => {
      console.log('The audio has finished playing!')
    })

    player.on('error', (error) => {
      console.error('Error:', error.message)
    })
  }
}

module.exports = AudioBot
