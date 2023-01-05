from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request
import time
import smtplib
import ssl
from email.message import EmailMessage
from bs4 import BeautifulSoup as bs
import os

# Set up email #
email_sender = 'matthewtransoftdev@gmail.com'
email_password = 'cfnjmcjbkcaiajsb'
email_receiver = 'matthew.tran562@gmail.com'
subject = '*Stock Bot Notification*'
# Set up email #

#beautiful soup stuff
#base=os.path.dirname(os.path.abspath(‘#Name of Python file in which you are currently working))
#beautiful soup stuff

class MyHTMLParser(HTMLParser):
    
    status = False
    cnt = 0
    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)
        

    def send_email(self, inputBody):
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(inputBody)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


# "False" Status means SOLD OUT
# "True" Status means in stock
    def getStatus(self):
        return self.status;
    
    def getStatusString(self):
        if self.status:
            return "Item Status has changed: Item is in stock!"
        else:
            return "Item Status has changed: Item is sold out!"
        
    def handle_starttag(self,tag, data):
        self.cnt = self.cnt + 1
        #print(self.cnt);
        #print(str(data))
        if("unselectable    '), ('data-attr', 'size-value'), ('aria-label', 'Select Size 9.5')" in str(data)):
            print("Item detected as: SIZE 9.5 SOLD OUT")
            self.status = False
        
        elif("selectable    '), ('data-attr', 'size-value'), ('aria-label', 'Select Size 9.5')"in str(data) ):
            print("Item detected as: Size 9.5 IN STOCK")
            self.status = True
        

#    def handle_data(self, data):

        
        


            

        
            

parser = MyHTMLParser()
prevStat = parser.getStatus();

#Loop keeps code running continously
while(True):

    fp = urllib.request.urlopen("https://www.newbalance.com/pd/550/BB550V1-36007.html")
    mybytes = fp.read()

    x = mybytes.decode("utf8")
    fp.close()
    parser.feed(x)
    
#    x = open("testsite.html")
#    parser.feed(str(x.read()))

    
    currStat = parser.getStatus();

    
    if currStat == prevStat:
        print("Status unchanged, no email sent")
        
    
    if currStat != prevStat:
        print("STATUS CHANGED, SENDING EMAIL NOW!")
        parser.send_email(parser.getStatusString())
        prevStat = currStat
        
    parser.close()

        
    time.sleep(10)

parser.close()
