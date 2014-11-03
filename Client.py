from twisted.internet import reactor
from twisted.internet import protocol
import Datagram
import json
import hashlib

class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    
    def __init__(self):
        self.token = ''
    
    def connectionMade(self):
        print 'Connected!'
        self.beginLogin()
        
    def beginLogin(self):
        username = raw_input('Please enter your username: ')
        passwordRaw = raw_input('Please enter your password: ')
        password = self.hashPassword(passwordRaw)
        dg = Datagram.Datagram()
        dg.setHeader('authenticate')
        dg.setData({'username':username, 'password' : password, 'token' : '0'})
        dg.updateAuth()
        self.sendDatagram(dg)
        
    def hashPassword(self, passwordRaw):
        hasher = hashlib.md5()
        hasher.update(passwordRaw)
        return hasher.hexdigest()
        
    def sendDatagram(self, dg):
        datagram = dg.getContents()
        self.transport.write(json.dumps(datagram))
    
    def dataReceived(self, data):
        data = json.loads(data)
        header = data['header']
        response = data['data']
        if header == 'loginresp':
            if not response['success'] == 'True':
                print 'Login failed. %s' % response['reason']
                self.transport.loseConnection()
            else:
                print 'Login successful!'
                self.token = response['token']
                self.beginInteraction()
        elif header == 'updateresponse':
            print response
                
    def beginInteraction(self):
        dg = Datagram.Datagram()
        dg.setHeader('get-update')
        dg.setData({'username' : 'username', 'password' : 'password', 'token' : self.token})
        dg.updateAuth()
        self.sendDatagram(dg)

    
    def connectionLost(self, reason):
        print "connection lost"

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server runing on port 8000
def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
