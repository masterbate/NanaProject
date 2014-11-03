import hashlib

class Datagram:
    
    def __init__(self):
        self.header = ''
        self.data = {}
        self.authenticity = ''
        
    def setHeader(self, header):
        self.header = header
        
    def setData(self, data):
        if isinstance(data, dict):
            self.data = data
        else:
            #Data is invalid
            return 'Invalid data-type'
        
    def updateAuth(self):
        pascal = hashlib.md5()
        data = ''
        for key in list(self.data.keys()):
            data += key
        for value in list(self.data.values()):
            data += value
        pascal.update(self.header + data)
        self.authenticity = pascal.hexdigest()
        
    def getContents(self):
        return {'header' : self.header, 'data' : self.data, 'auth' : self.authenticity}
