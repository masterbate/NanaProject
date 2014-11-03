import Appnada
import os
import json

class NanaCheckup:
    
    def __init__(self):
        #Use this class to check up on the nana count on each of your accounts
        self.appnana = Appnada.Appnada()
        self.account2nana = {}
        self.validateFileExistance()
        
    def validateFileExistance(self):
        if os.path.isfile('accountIds.appnana'):
            self.beginLogins()
        else:
            print 'Your accountIds.appnana file cannot be found (Maybe you have not run TimeBasedGenerator.py?)'
            
    def beginLogins(self):
        with open('accountIds.appnana', 'r') as f:
            self.accounts = f.readlines()
        for account in self.accounts:
            formatted = account.rstrip()
            self.appnana.login(formatted)
            jsonInfo = self.appnana.getUserInfo()
            nanaCount = json.loads(jsonInfo)['response']['nanas']
            self.account2nana[formatted] = nanaCount
            print formatted + ' has %s' % nanaCount + ' nanas'
        print 'Done!'
            
            
NanaCheckup = NanaCheckup()
