from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

from Libs import Appnada

import cgi
import hashlib
import json

import thread
import time
import os

loginPage = '<div id="login_form"><form name="f1" method="post" id="f1"><table><tr><td class="f1_label">User Name :</td><td><input type="text" name="username" value="" /></td></tr><tr><td class="f1_label">Password  :</td><td><input type="password" name="password" value=""  /></td></tr><tr><td><input type="submit" name="method" value="login" style="font-size:18px; " /></td></tr></table></form></div>'
actionPick = '<div id="choice_form"><form name="f1" method="post" id="f1"><table><tr><td class="f1_label">Choose what you need:</td></tr><tr><td><input type="submit" name="method" value="stats" style="font-size:20px; " /></td></tr></table></form></div><div id="choice_form"><form name="f2" method="post" id="f2"><table><tr><td><input type="submit" name="method" value="login" style="font-size:20px; " /></td></tr></table></form></div>  <div id="choice_form"><form name="f2" method="post" id="f2"><table><tr><td><input type="submit" name="method" value="new database" style="font-size:20px; " /></td></tr></table></form></div>'

class Manager:
    
    def __init__(self):
        self.session2user = {}
        self.loggedIn = []
        self.timestamp2user = {}
        print 'Manager running'

Manager = Manager()

class FormPage(Resource):
    
    def render_GET(self, request):
        return loginPage

    def render_POST(self, request):
        params = request.args
        method = params['method'][0]
        if method == 'login':
            if self.handleLogin(params, request):
                return '<meta http-equiv="refresh" content="1; url=/account" />'
            else:
                return 'Invalid credentials!'
        else:
            return 'Access Denied.'
        
    def hashPassword(self, passwordRaw):
        hasher = hashlib.md5()
        hasher.update(passwordRaw)
        return hasher.hexdigest()
        
    def handleLogin(self, request, sender):
        username = request['username'][0]
        password = request['password'][0]
        password = self.hashPassword(password)
        with open('DB/Users.db', 'r') as db:
            lines = db.readlines()
            for line in lines:
                userAndPass = line.split(':')
                if not len(userAndPass) == 2:
                    print 'Login array exception occured:'
                    print userAndPass
                    return False
                rusername = userAndPass[0]
                rpassword = userAndPass[1]
                if str(rusername.rstrip()) == str(username.rstrip()) and str(rpassword.rstrip()) == str(password.rstrip()):
                    Manager.loggedIn = sender.getSession().uid
                    Manager.session2user[sender.getSession().uid] =  username
                    return True
            print 'Invalid credentials!'
            return False
                    
class AccountPage(Resource):
    
    def __init__(self):
        self.a = Appnada.Appnada()
        self.timestamp2user = {}
        self.dailyThread = thread.start_new_thread()
        
    def dailyNanaThread(self):
        while True:
            user in self.timestamp2user.keys():
                oldStamp = self.timestamp2user[user]
                newStamp = time.time()
                stampDifference = newStamp - oldStamp
                #if stampDifference > 86430:
                if stampDifference > 60:
                    print 'Starting Daily Nanas for: %s' % user
                    self.loginStamp(user)
            time.sleep(10)
    
    def render_GET(self, request):
        if not request.getSession().uid in Manager.loggedIn:
            return 'Permission Denied'
        #return 'Welcome to the account page, %s' % Manager.session2user[request.getSession().uid] + ' here is a quick update on your standings... \n Accounts in current Database: %s' % self.countDB(request.getSession().uid)
        return actionPick
        
    def render_POST(self, request):
        if not request.getSession().uid in Manager.loggedIn:
            return 'Permission Denied'
        params = request.args
        method = params['method'][0]
        if method == 'stats':
            dbAccounts = self.countDB(request.getSession().uid)
            accountNanas = self.countNanas(request.getSession().uid)
            return 'Your Database object has %s' % dbAccounts + ' Accounts in it, each containing %s' % accountNanas + ' Nanas.'
        elif method == 'login':
            username = Manager.session2user[request.getSession().uid]
            fileName = username + '.appnana'
            if os.path.isfile('DB/' + fileName):
                thread.start_new_thread(self.loginAccounts, (request.getSession().uid,) )
                return 'The server is now logging into your accounts, this may take a little while.. Please check the Stats button in a few minutes to see changes.'
            return 'You do not have a DB file!'
        elif method == 'new database':
            return '<div id="login_form"><form name="f1" method="post" id="f1"><table><tr><td class="f1_label">Amount of accounts:</td><td><input type="text" name="amount" value="" /></td></tr><tr><td><input type="submit" name="method" value="create" style="font-size:18px; " /></td></tr></table></form></div>'
        elif method == 'create':
            try:
                amount = int(params['amount'][0])
            except:
                return 'You need to input a number for your amount'
            thread.start_new_thread(self.createNewDB, (amount, request.getSession().uid,) )
            return 'The sever is now creating your new database object, please be patient with this as it may take a while, check progress using the Stats button'
        
    def countDB(self, uid):
        username = Manager.session2user[uid]
        fileName = username + '.appnana'
        if os.path.isfile('DB/' + fileName):
            with open('DB/' + fileName, 'r') as db:
                lines = db.readlines()
                return len(lines)
        return '*No DB File*'
            
    def countNanas(self, uid):
        username = Manager.session2user[uid]
        fileName = username + '.appnana'
        if os.path.isfile('DB/' + fileName):
            with open('DB/' + fileName, 'r') as db:
                lines = db.readlines()
                account = lines[0]
                self.a.login(account.rstrip())
                jsonInfo = self.a.getUserInfo()
                nanaCount = json.loads(jsonInfo)['response']['nanas']
                return nanaCount
        return '*No DB File*'
            
    def loginAccounts(self, uid):
        username = Manager.session2user[uid]
        print 'Starting a login thread for %s' % username
        fileName = username + '.appnana'
        with open('DB/' + fileName, 'r') as f:
            accounts = f.readlines()
        for account in accounts:
            formatted = account.rstrip()
            self.a.login(formatted)
        #generate a timestamp
        self.timestamp2user[username] = time.time()
        print 'Finished login thread for %s' % username
        return True
        
    def loginStamp(self, username):
        print 'Getting Daily nanas for %s' % username
        fileName = username + '.appnana'
        with open('DB/' + fileName, 'r') as f:
            accounts = f.readlines()
        for account in accounts:
            formatted = account.rstrip()
            self.a.login(formatted)
        #generate a timestamp
        self.timestamp2user[username] = time.time()
        print 'Finished login thread for %s' % username
        return True
        
    def createNewDB(self, amount, uid):
        username = Manager.session2user[uid]
        print 'Starting a DB Creation thread for %s' % username
        fileName = username + '.appnana'
        amount = int(amount)
        open('DB/' + fileName, 'w')
        for acc in xrange(amount):
            email = self.a.registerAccount()
            with open('DB/' + fileName, 'a') as db:
                db.write(email + '\n')
        print 'Finished a DB Creation thread for %s' % username
            

root = Resource()
root.putChild("", FormPage())
root.putChild("account", AccountPage())
factory = Site(root)
reactor.listenTCP(8800, factory)
reactor.run()
