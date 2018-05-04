const PythonShell = require('python-shell')

let nordpool = require('nordpool')
let prices = new nordpool.Prices()

let opts = {
  area: 'EE',
  currency: 'EUR',
}

const mart = (() => {
  prices.hourly(opts, (error, results) => {
    if (error) console.error(error)

    let hourData = results.map(x => {
      let dateArr = x.date.tz('Europe/Tallinn').format("D.M.Y H:mm").split(" ")
      x.time = dateArr[1]
      x.date = dateArr[0]
      return x
    })

    const priceNow = hourData.filter(x => x.time === getTime())
    console.log(priceNow)

    if(priceNow[0].value <= 40) {
      triggerLight('ffff')
    } else {
      triggerLight('0000')
    }
  })
})()

setInterval(() => {
  mart()
}, 3600000)

const getTime = () => new Date(Date.now()).getHours() + ":00"

const triggerLight = (arg) => {
  const options = {
    args: ['1', '0', arg, '/dev/tty.usbserial-FTX1G23K']
  }
  PythonShell.run('index.py', options, function (err, results) {
    if (err) throw err;
    console.log('results: %j', results);
  })
}
