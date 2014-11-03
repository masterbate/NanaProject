import Appnada
import os

class TimeBasedGenerator:
    
    def __init__(self):
        #Only use this class to generate your x amount of accounts that you will use to whore up some daily nana's
        #Remember to use "MassLogin.py" daily to keep up with this ;)
        #Emails stored in accountIds.appnana and password is always testpassword
        self.accountNumber = raw_input('How many accounts would you like? ')
        self.appnada = Appnada.Appnada()
        self.validateNumber()
        
    def validateNumber(self):
        try:
            self.accountNumber = int(self.accountNumber)
            self.areYouSure()
        except ValueError:
            print 'You did not input a valid number'
            
    def areYouSure(self):
        if os.path.isfile('accountIds.appnana'):
            print 'You already have an accountIds.appnana file, if you over-write this you may lose all your progress!'
            print 'Type "delete" if you agree to continue'
            response = raw_input('')
            if response == 'delete':
                self.generateAccounts()
            else:
                self.areYouSure()
        else:
            self.generateAccounts()
            
    def generateAccounts(self):
        for i in xrange(self.accountNumber):
            self.appnada.registerAccount()
        print 'Done!'
        
TimeBasedGenerator = TimeBasedGenerator()
