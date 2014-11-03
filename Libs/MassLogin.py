import Appnada
import os

class MassLogin:
    
    def __init__(self):
        #This class is here to login to all accounts in your *.appnana file in order to get you your daily nanas
        #be sure to have run TimeBasedGenerator.py before running this to create your accountIds.appnana file
        self.appnana = Appnada.Appnada()
        self.accounts = []
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
        print 'Done!'

            
MassLogin = MassLogin()
