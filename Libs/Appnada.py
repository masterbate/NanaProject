import requests
import hashlib
import json
import random
import string

class Appnada:
    
    def __init__(self):
        self.email = ''
        self.BASE_REQUEST_URL = "http://appnana2.mapiz.com/api/";
        self.FINISH_OFFER_RFN_URL = "http://appnana2.mapiz.com/api/finish_offer_rfn/";
        self.GET_REWARDS_REQUEST_URL = "http://appnana2.mapiz.com/api/rewards/";
        self.GET_SETTINGS_REQUEST_URL = "http://appnana2.mapiz.com/api/settings/";
        self.GET_USER_INFO_REQUEST_URL = "http://appnana2.mapiz.com/api/get_nanaer_info/";
        self.INVITE_VERIFY_REQUEST_URL = "http://appnana2.mapiz.com/api/invite_verify/";
        self.LOGIN_REQUEST_URL = "http://appnana2.mapiz.com/api/nanaer_login/";
        self.LOGOUT_REQUEST_URL = "http://appnana2.mapiz.com/api/nanaer_logout/";
        self.REDEEM_REQUEST_URL = "http://appnana2.mapiz.com/api/redeem/";
        self.REGISTER_REQUEST_URL = "http://appnana2.mapiz.com/api/nanaer_register/";
        self.session = requests.session()
        
    def sendPost(self, payload, link):
        headers = {
         'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; Nexus One Build/FRF50) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
         'Accept-Language' : 'da, en-gb;q=0.8, en;q=0.7'}
        r = self.session.post(link, headers=headers, data = payload)
        return r
        
    def sendGet(self, payload, link):
        headers = {
         'Accept' : 'application/json',
         'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; Nexus One Build/FRF50) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
         'Accept-Language' : 'da, en-gb;q=0.8, en;q=0.7'}
        r = self.session.get(link + '?email=x', headers=headers)
        return r
        
    def finishOfferRfn(self):
        payload = {
         'device' : 'QlpoOTFBWSZTWSDpIrkAAAVcAAAQAAF1gAAAEIAAiGgbUIMmIE2ccg8XckU4UJAg6SK5A'}
        print self.sendPost(payload, self.FINISH_OFFER_RFN_URL).text
        
    def getSignupKey(self):
        m = hashlib.sha1()
        m.update("20013fea6bcc820c" + self.email + "Android" + "VU58A2ND8S9")
        return m.hexdigest()
        
    def getSigninKey(self):
        m = hashlib.sha1()
        m.update("20013fea6bcc820c" + self.email + "VU58A2ND8S9")
        return m.hexdigest()
        
    def inviteVerify(self, code):
        payload = {'email' : self.email, 'invitation' : code}
        return self.sendPost(payload, self.INVITE_VERIFY_REQUEST_URL).text
        
    def getUserInfo(self):
        payload = {"email" : self.email}
        return self.sendGet(payload, self.GET_USER_INFO_REQUEST_URL).text
 
    def login(self, email):
        self.email = email
        accountCreds = {
         'email' : self.email,
         'password' : 'testpassword',
         'source' : 'Android',
         'signkey' : self.getSigninKey(),
         'android_id' : '20013fea6bcc820c',
         'gaid' : '1',
         'gaid_enabled' : 'True'}
        response = self.sendPost(accountCreds, self.LOGIN_REQUEST_URL).text
        success = json.loads(response)['header']['errstr']
        if not success == 'SUCCESS':
            return 'LMFAO PORN'
        
    def registerAccount(self):
        self.generateNewEmail()
        #self.storeEmail(self.email, storage)
        accountCreds = {
         'email' : self.email,
         'password' : 'testpassword',
         'source' : 'Android',
         'signupkey' : self.getSignupKey(),
         'android_id' : "20013fea6bcc820c",
         'system_version' : '4.0.4',
         'system_name' : 'iAmAPhone',
         'device_type' : 'galaxy',
         'android_imei' : '352605059157941',
         'gaid' : '1',
         }
        response = self.sendPost(accountCreds, self.REGISTER_REQUEST_URL).text
        success = json.loads(response)['header']['errstr']
        if not success == 'SUCCESS':
            print 'Error occured on account generation!'
        return self.email
        
    def redeemCode(self, code):
        {'email' : ''}
        
    def generateNewEmail(self, size=random.randint(7, 15), chars=string.ascii_lowercase + string.digits):
        self.email = ''.join(random.choice(chars) for _ in range(size)) + '@gmail.com'
        
    def storeEmail(self, email, storage):
        with open('accountIds.appnana', 'a') as f:
            f.write(email + '\n')
