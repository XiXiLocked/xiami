from sys import stdin
from requests import session, exceptions
from bs4 import BeautifulSoup
from json import loads


class XiamiAccount(object):
    loginURL = 'https://login.xiami.com/member/login'
    logoutURL = 'http://www.xiami.com/member/logout'
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = session()
        self.loggedin = False

    def get_form(self):
        "get hidden login information"
        try:
            r =  self.session.get(XiamiAccount.loginURL)
            if r.status_code == 200:
                form = {}
                for item in BeautifulSoup(r.text).form.find_all('input'):
                    form[item.get('name') ] = item.get('value')
                return form
        except exceptions.RequestException:
            pass

        return None



    def login(self):
        form = self.get_form()
        form['email'] = self.email
        form['password'] = self.password
        try:
            r = self.session.post(XiamiAccount.loginURL, data = form)
            if r.status_code == 200:
                response = loads(r.text)
                self.loggedin = response['status']
                return response
        except exceptions.RequestException:
            pass

        return None


    def logout(self):
        try:
            self.session.get(XiamiAccount.logoutURL)
        except exceptions.RequestException:
            pass
        finally :
            self.session.close()
            self.loggedin = False

class XiamiSignin(object):
    Referer = 'http://www.xiami.com'
    InfoURL = Referer+'/index/home'
    SigninURL =  Referer+'/task/signin'
    #the following two header lines are nessary for retrieve infos
    header = {#'X-Requested-With' : 'XMLHttpRequest',
            'Referer' :Referer,
            'User-Agent':''}#empty is ok, but not be absent
    def __init__(self, email, password):
        self.account = XiamiAccount(email, password)
        self.signed = False

    def sign_info(self):
        if not self.account.loggedin:
            self.account.login()
        "get signin info"
        try:
            r = self.account.session.get(XiamiSignin.InfoURL,
                    headers = XiamiSignin.header)
            if r.status_code == 200:
                response = loads(r.text)
                info = response['data']['userInfo']
                self.signed = info['is'] == 1
                return info
        except exceptions.RequestException:
            pass

        return None


    def signin(self):
        r = self.sign_info()
        if self.signed:
            return (True, r['sign']['persist_num'])
        elif r:
            try:
                self.account.session.post(XiamiSignin.SigninURL,
                        headers = XiamiSignin.header)
                r = self.sign_info()
                return (self.signed, r['sign']['persist_num'])
            except exceptions.RequestException:
                pass

        return (False, '-1')


def main(sign_list):
    for i in range(len(sign_list)//2):
        u = sign_list[2*i].strip()
        p = sign_list[2*i+1].strip()
        xiami = XiamiSignin(u, p)
        res = xiami.signin()
        print("{0}: {1} has signed {2} days".format(
            "Success" if res[0] else "Failure",
            xiami.account.email,
            res[1]))
        xiami.account.logout()



if __name__ == '__main__':
    main(stdin.readlines())
