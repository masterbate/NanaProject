import Appnada
import os
import json

class MassInviteCode:
    
    def __init__(self):
        #Use this class to have a massive amount of accounts all use your inviteCode ;)
        self.appnana = Appnada.Appnada()
        self.inviteCode = 'L6329154'
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
            jsonInfo = self.appnana.inviteVerify(self.inviteCode)
            status = json.loads(jsonInfo)['response']
            print 'The result for ' + formatted + ' was ' + status
        print 'Done!'

MassInviteCode = MassInviteCode()
