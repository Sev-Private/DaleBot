const AudioBot = require('../../default-bots/audio-bot.js')

class FaroBot extends AudioBot {
  constructor (client) {
    super(client, 'faro')

    this.commands = [
      {
        key: 'uepa',
        message: 'Uêpa!',
        url: 'https://www.youtube.com/watch?v=gQm8hyMfz2o'
      },
      {
        key: 'pare',
        message: 'PARE!',
        url: 'https://www.youtube.com/watch?v=djnyU9-ZyVg'
      },
      {
        key: 'cavalo',
        message: 'Cavalo!',
        url: 'https://www.youtube.com/watch?v=rYd4Y4v9qmw'
      },
      {
        key: 'atumalaca',
        message: 'kkkkkkk',
        url: 'https://www.youtube.com/watch?v=cVScsUqorGo'
      },
      {
        key: 'aoow',
        message: 'AOOOWW POTÊNCIA!!!',
        url: 'https://www.youtube.com/watch?v=P5MphlfhOOA'
      },
      {
        key: 'rapaz',
        message: 'Rapaaaaiz',
        url: 'https://www.youtube.com/watch?v=HXYNW0ft5o4'
      },
      {
        key: 'gato',
        message: 'Miaaau',
        url: 'https://www.youtube.com/watch?v=fTP2IbqMEtU'
      },
      {
        key: 'irra',
        message: ' 🤠 ',
        url: 'https://www.youtube.com/watch?v=uaKKjT_d0jI'
      },
      {
        key: 'queisso',
        message: 'Que isso meu filho, calma!',
        url: 'https://www.youtube.com/watch?v=ou3BlCaj1DM'
      },
      {
        key: 'bombeiro',
        message: 'Chama o bombeiro!!!',
        url: 'https://www.youtube.com/watch?v=oOGOgM46-eE'
      },
      {
        key: 'camisa',
        message: 'TIRA A CAMISA!!!',
        url: 'https://www.youtube.com/watch?v=4BNsD-6I3s4'
      },
      {
        key: 'aleluia',
        message: ' 🙏🙏🙏🙏 ',
        url: 'https://www.youtube.com/watch?v=ou-pUmCRgpY'
      },
      {
        key: 'suspense',
        message: ' 😮  ',
        url: 'https://www.youtube.com/watch?v=nNrliAV85NM'
      },
      {
        key: 'ronaldo',
        message: '...ronaldo',
        url: 'https://www.youtube.com/watch?v=BcTmsC5OTyQ'
      },
      {
        key: 'patrao',
        message: 'Eeeesse é meu patrão hehehehei',
        url: 'https://www.youtube.com/watch?v=KFdFEGpFXyg'
      },
      {
        key: 'danca',
        message: 'Dança gatinho, dança',
        url: 'https://www.youtube.com/watch?v=9TjqvTFBTFU'
      },
      {
        key: 'brasil',
        message: 'BRASIL SIL SIL SIL....',
        url: 'https://www.youtube.com/watch?v=EnLNDuKya04'
      },
      {
        key: 'corneta',
        message: ' 🎺 ',
        url: 'https://www.youtube.com/watch?v=s4rmbuQGdgQ'
      },
      {
        key: 'coracao',
        message: 'Tum tum tum...',
        url: 'https://www.youtube.com/watch?v=z2fNFmbAVCI'
      },
      {
        key: 'aplausos',
        message: ' 👏 👏 👏 ',
        url: 'https://www.youtube.com/watch?v=ajJX8ZGXIxo'
      },
      {
        key: 'vaias',
        message: 'Bhuuu... Bhuuu... Bhuuu...',
        url: 'https://www.youtube.com/watch?v=pvGtop2Sf-4'
      },
      {
        key: 'tarzan',
        message: 'OOOOooooOOooOOOOoo...',
        url: 'https://www.youtube.com/watch?v=ttabWazASo0'
      },
      {
        key: 'ratinho',
        message: 'RratinhooOOoooOOoo...',
        url: 'https://www.youtube.com/watch?v=-d6wB4KyuUk'
      },
      {
        key: 'papelao',
        message: 'Que papelão hein kkkkkkkk',
        url: 'https://www.youtube.com/watch?v=US9QhKiEg6w'
      },
      {
        key: 'rodaaroda',
        message: 'Quem quer dinheiro???!!!',
        url: 'https://www.youtube.com/watch?v=f8qspc1aspE'
      },
      {
        key: 'telesena',
        message: 'Quem quer dinheiro???!!!',
        url: 'https://www.youtube.com/watch?v=UtKKg6wvW1I'
      },
      {
        key: 'peao-sbt',
        message: 'Quem quer dinheiro???!!!',
        url: 'https://www.youtube.com/watch?v=f8qspc1aspE'
      },
      {
        key: 'ai',
        message: 'Aiiiii!!!!',
        url: 'https://www.youtube.com/watch?v=s-9gT1y2bYk'
      },
      {
        key: 'coice',
        message: ' 🐎 ',
        url: 'https://www.youtube.com/watch?v=zTEBYSkJeOs'
      },
      {
        key: 'brincadeira',
        message: 'É brincadeira, hein!!! 😅 ',
        url: 'https://www.youtube.com/watch?v=C57kQv_hd40'
      },
      {
        key: 'chaves-xylophone',
        message: 'Chaves - Xylophone',
        url: 'https://www.youtube.com/watch?v=JJ_lV4h_b9s'
      },
      {
        key: 'chaves-pancada',
        message: 'Chaves - Pancada',
        url: 'https://www.youtube.com/watch?v=xUE_gSdUhZA'
      },
      {
        key: 'chaves-risada',
        message: 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK',
        url: 'https://www.youtube.com/watch?v=Ujt1Q4M43UI'
      },
      {
        key: 'zap',
        message: 'zap zap zap zap zap zap zap zap zap zap zap zap',
        url: 'https://www.youtube.com/watch?v=IUiGbOFjs50'
      },
      {
        key: 'ele-gosta',
        message: ' 😏 ',
        url: 'https://www.youtube.com/watch?v=WFci2lINVE8'
      },
      {
        key: 'olha-ele-ae',
        message: 'Olha ele aé!!!',
        url: 'https://www.youtube.com/watch?v=W8ab00LC-JQ'
      }
    ]
  }

  ajuda (message) {
    super.sendTextMessage(message, 'Se liga nos comandos')
    const allCommands = this.commands.map(element => {
      return element.key
    }).join().replaceAll(',', '\n')
    console.log(allCommands)
    super.sendTextMessage(message, allCommands)
  }

  handleMessage (message, args) {
    const command = args[0]

    if (command === null) {
      console.log('Xiiiiii é brincadeira')
      super.sendTextMessage(message, 'Deu erro no comando doidão')
      this.ajuda(message)
      return
    }

    console.log(command)

    if (command.toLowerCase() === 'ajuda') {
      this.ajuda(message)
      return
    }

    const reaction = this.commands.find(element => {
      return element.key === command
    })

    console.log(reaction)

    if (reaction === null || reaction === undefined) {
      console.log('Coé doidão')
      super.sendTextMessage(message, 'Escolhe o negócio direito')
      return
    }

    super.setNickname(message, 'Hora do Faro')
    super.sendTextMessage(message, reaction.message)
    super.sendVoiceMessage(message, reaction.url)
  }
}

module.exports = FaroBot
