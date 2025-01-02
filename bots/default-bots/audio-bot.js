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
const fs = require('fs');

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
      // url = ytdl(url)
      ytdl('https://www.youtube.com/watch?v=EnLNDuKya04', { filter: 'audioonly' })
      .pipe(fs.createWriteStream('audio.mp3'))
      .on('error', console.error);
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
