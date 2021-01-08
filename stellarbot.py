import urllib, requests
import config
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

# polling timeout
timeout = 18000.0 + 3600.0 + 3600.0 #7 minuti

print ('Listening ...')
def doWork():
    magicUpdateScraper()
    pass

l = task.LoopingCall(doWork)
l.start(timeout) # call ogni 7 minuti

reactor.run()