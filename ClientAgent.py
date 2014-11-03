from Libs import Appnada
from twisted.internet import reactor
from twisted.internet import protocol
import hashlib
import Datagram
import json
import random
import time

class Echo(protocol.Protocol):
    
    def __init__(self):
        self.appnana = Appnada.Appnada()
        self.unauthedConnections = []
        self.authedConnections = {}
        self.username2invite = {'admin' : 'l6329154', 'tommackinnon1' : 't6391754'}
    
    def connectionMade(self):
        connection = self.transport
        self.unauthedConnections.append(connection)
        print 'Got an incoming UnAuthenticated connection from %s' % connection.getPeer().host
        
    def connectionLost(self, reason):
        print 'We lost %s' % self.transport.getPeer().host
        if self.transport in self.unauthedConnections:
            self.unauthedConnections.remove(self.transport)
        
    def sendDatagram(self, dg, who):
        datagram = dg.getContents()
        who.write(json.dumps(datagram))
        
    def hashPassword(self, passwordRaw):
        hasher = hashlib.md5()
        hasher.update(passwordRaw)
        return hasher.hexdigest()
        
    def newToken(self, username):
        tokenGen = hashlib.md5()
        tokenGen.update(username + str(time.time()) + str(random.randint(2048, 65535)))
        return tokenGen.hexdigest()
    
    def dataReceived(self, data):
        post = data.split('\r\n\r\n')[1]
        if post.startswith('username'):
            print 'yes!'
            self.transport.write('ok')
        return
        data = json.loads(data)
        sender = self.transport
        header = data['header']
        contents = data['data']
        auth = data['auth']
        if sender in self.unauthedConnections:
            if not header == 'authenticate':
                print 'Non-Authed client tried to send a non-authenticate message'
                sender.loseConnection()
                self.unauthedConnections.remove(sender)
                return
        token = contents['token']
        if not self.authentic(header, contents, auth):
            print 'Got non-authentic packet from %s' % sender.getPeer().host
            del self.authedConnections[token]
            sender.loseConnection()
            return
        if header == 'authenticate':
            self.handleLogin(contents, sender)
        elif header == 'get-update':
            self.handleGetupdate(contents, sender, token)
        else:
            print 'Invalid header recieved!'
            del self.authedConnections[token]
            sender.loseConnection()
            return
            
    def authentic(self, header, data, authKey):
        pascal = hashlib.md5()
        contents = ''
        for key in list(data.keys()):
            contents += str(key)
        for value in list(data.values()):
            contents += str(value)
        pascal.update(header + contents)
        serverKey = pascal.hexdigest()
        if serverKey == authKey:
            return True
        return False
        
    def handleLogin(self, data, sender):
        if not len(data) == 3:
            print 'Invalid login data provided'
            self.unauthedConnections.remove(sender)
            sender.loseConnection()
            return
        if not 'username' in data.keys() or not 'password' in data.keys():
            print 'Invalid login data provided'
            self.unauthedConnections.remove(sender)
            sender.loseConnection()
            return
        username = data['username']
        password = data['password']
        if not self.checkLogin(username, password):
            print 'Failed login'
            dg = Datagram.Datagram()
            dg.setHeader('loginresp')
            dg.setData({'success' : 'False', 'reason' : 'Bad credentials'})
            dg.updateAuth()
            self.sendDatagram(dg, sender)
            return
        token = self.newToken(username)
        dg = Datagram.Datagram()
        dg.setHeader('loginresp')
        dg.setData({'success' : 'True', 'token' : token})
        dg.updateAuth()
        self.sendDatagram(dg, sender)
        self.unauthedConnections.remove(sender)
        self.authedConnections[token] = username
        
    def checkLogin(self, username, password):
        with open('DB/Users.db', 'r') as db:
            lines = db.readlines()
            for line in lines:
                rusername, rpassword = line.split(':')
                if rusername.rstrip() == str(username) and rpassword.rstrip() == str(password):
                    return True
                else:
                    return False
                    
    def handleGetupdate(self, data, sender, token):
        jsonData = self.appnana.getUserInfo()
        dg = Datagram.Datagram()
        dg.setHeader('updateresponse')
        dg.setData({'stats' : jsonData})
        dg.updateAuth()
        self.sendDatagram(dg, sender)

def main():
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()



