const request = require('request')
const AudioBot = require('../../default-bots/audio-bot.js')

class InstantsBot extends AudioBot {
  constructor (client) {
    super(client, 'instant')
  }

  instantSearchQuery (args) {
    return args.join(' ')
  }

  validURL (str) {
    const pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
          '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
          '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
          '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
          '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
          '(\\#[-a-z\\d_]*)?$', 'i') // fragment locator
    return !!pattern.test(str)
  }

  handleMessage (message, args) {
    const query = this.instantSearchQuery(args)
    if (query == null) {
      return
    }
    console.log(query)

    let url = ''
    if (this.validURL(query)) {
      url = query
    } else {
      url = 'https://www.myinstants.com/search/?name=' + query.split(' ').join('+')
    }

    console.log(url)

    const that = this
    request({ uri: url },
      function (error, response, body) {
        console.error('error:', error)
        that.parseHTMLfirstResult(body, message)
      }
    )
  }

  parseHTMLfirstResult (body, message) {
    if (body == null) {
      return
    }

    const pattern = /onclick="play\('(.*?)'\)"/g
    const results = body.match(pattern)
    this.formatUrl(message, results)
    super.setNickname(message, 'My instants')
  }

 formatUrl(message, instant) {
    if (instant === null || !Array.isArray(instant) || instant.length === 0) {
      return;
    }
  
    console.log(instant);
  
    // Updated regex to specifically check for 'onclick="play(' and capture the URL part
    let regex = /onclick="play\('([^']+)'/;
  
    // Loop through the array and check each string
    for (let i = 0; i < instant.length; i++) {
      let str = instant[i];
  
      // Try to find a match for the regex in the current string
      let match = str.match(regex);
  
      // If a match is found, process and return the URL
      if (match && match[1]) {
        const url = 'https://www.myinstants.com' + match[1];
        console.log("Formatted URL:", url);
        super.sendVoiceMessage(message, url);
        return; // Exit after the first match
      }
    }
  
    // If no match is found in any string
    console.log("No match found in any of the instant strings.");
  }
}

module.exports = InstantsBot
