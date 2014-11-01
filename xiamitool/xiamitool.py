from sys import stdin
from requests import session,exceptions
from bs4 import BeautifulSoup

class Account(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password

class Login(Account):
    loginurl = 'https://login.xiami.com/member/login'
    logouturl = 'http://www.xiami.com/member/logout'
    def __init__(self, email, password):
        super(Login, self).__init__(email,password)
        self.session = session()
        self.form = {} #form for login post
        self.loggedin = False

    def fill_form(self):
        try:
            #get hidden login information
            html = self.session.get(Login.loginurl).text
            for item in BeautifulSoup(html).form.find_all('input'):
                #because password input box has no 'value'
                self.form[item.get('name') ] = item.get('value')
            self.form['email'] = self.email
            self.form['password'] = self.password
        except exceptions.RequestException:
            #ignore connection exception
            pass


    def login(self):
        try:
            self.fill_form()
            r = self.session.post(Login.loginurl, data = self.form)
            if r.status_code ==200:
                self.loggedin = True
        except exceptions.RequestException:
            pass

    def logout(self):
        try:
            self.session.get(Login.logouturl)
            self.session.close()
            self.loggedin = False
        except exceptions.RequestException:
            pass

class Signin(Login):
    signurl = 'http://www.xiami.com/task/signin'
    def __init__(self, email, password):
        super(Signin, self).__init__(email, password)
        self.signedday = 0
        #the following two header lines are nessary for signin
        self.head = {'Referer':'http://www.xiami.com',
                #'X-Requested-With':'XMLHttpRequest',
                'User-Agent':''}#empty is ok, just present it.

    def day(self):
        #get signinde days
        try:
            r = self.session.post(Signin.signurl,headers = self.head)
            if r.status_code ==200:
                self.signedday = r.text
        except exceptions.RequestException:
            pass

    def signin(self):
        try:
            self.day()
            #the 't_sign_auth' cookie is nessary
            r = self.session.post(Signin.signurl,
                    headers = self.head,
                    cookies = {'t_sign_auth':self.signedday})
            if r.status_code ==200 and self.signedday != r.text:
                self.signedday = r.text
                return True

        except exceptions.RequestException:
            pass
        return False

def main(sign_list):
    for i in range(len(sign_list)//2):
        u = sign_list[2*i].strip()
        p = sign_list[2*i+1].strip()
        xiami = Signin(u,p)
        xiami.login()
        if xiami.signin():
            print("Success: {0} has signed {1} days".format(u,xiami.signedday))
        else:
            print("Failure: {0} ".format(u))
        xiami.logout()



if __name__ == '__main__':
    main(stdin.readlines())
