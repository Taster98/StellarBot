import urllib, requests
import config
import telepot
from telepot.loop import MessageLoop
import re
from bs4 import BeautifulSoup
from twisted.internet import task, reactor

# Robe per gli XLM
oldvalue = 0.0
def magicUpdateScraper():
    tosend = False
    # inizializzo la roba per la valuta
    url = config.getScrapSite()
    html = requests.get(url,headers={'Cache-Control': 'no-cache'}).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll('div', {'class':'calculated-rate'})
    valore = str(links)[293:300]
    converted = "NUOVE STATISTICHE DI STELLAR: \n 1 XLM = "+valore +" €"
    global oldvalue
    if(oldvalue == 0.0):
        oldvalue = float(valore)
        tosend = True
    if(abs(oldvalue-float(valore)) >= 0.02):
        tosend = True
        oldvalue = float(valore)
    if(tosend):
        url2 = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
    config.getToken(), config.getId(),converted)
        _ = requests.get(url2, timeout=10)
    print(valore)
    
# Robe per USD to EUR
def usdToEurScraper():
    url3 = "https://transferwise.com/it/currency-converter/usd-to-eur-rate"
    html = requests.get(url3).text
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll('span', {'class':'text-success'})
    converted = str(links[0])[27:31]
    return "Attualmente, 1€ = "+converted

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        if(msg["text"] == "/dollaro" or msg["text"] == "/dollaro@updatestlrbot"):
            bot.sendMessage(chat_id, usdToEurScraper())

# polling timeout
timeout = 3600.0 #1 minuto
# Gestione chat e comandi
bot = telepot.Bot(config.getToken)
bot.message_loop(on_chat_message)
print ('Listening ...')
def doWork():
    magicUpdateScraper()
    pass

l = task.LoopingCall(doWork)
l.start(timeout) # call ogni minuto

reactor.run()