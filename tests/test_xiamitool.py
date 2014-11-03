from xiamitool.xiamitool import XiamiAccount, XiamiSignin
import unittest

#test account
usrname = input('username\n>')
passwd = input('password\n>')

class TestXiami1(unittest.TestCase):
    def setUp(self):
        self.u = 'username'
        self.p = 'pwpwpw'
        self.t_account = XiamiAccount(self.u, self.p)
        self.t_account2 = XiamiSignin(self.u, self.p)

    def test_XiamiAccount_initialization(self):
        self.assertEqual(self.t_account.email,  self.u)
        self.assertEqual(self.t_account.password,  self.p)
        self.assertFalse(self.t_account.loggedin)

        self.assertEqual(self.t_account2.account.email,  self.u)
        self.assertEqual(self.t_account2.account.password,  self.p)
        self.assertFalse(self.t_account2.signed)

class Test_with_connection(unittest.TestCase):
    def setUp(self):
        self.u = usrname
        self.p = passwd
        self.t_account = XiamiAccount(self.u, self.p)
        self.t_account2 = XiamiSignin(self.u, self.p)

    def test_get_form(self):
        form = self.t_account.get_form()
        self.assertIsNotNone(form)
        self.t_account.session.close()

    def test_login(self):
        self.t_account.login()
        self.assertTrue(self.t_account.loggedin)
        self.assertGreater(len(self.t_account.session.cookies), 0)
        self.t_account.logout()

    def test_issigned(self):
        info = self.t_account2.sign_info()
        self.assertIsNotNone(info)
        self.t_account2.account.logout()

    def test_signin(self):
        (a, b) = self.t_account2.signin()
        self.assertTrue(a)
        print(b)
        self.t_account2.account.logout()

if __name__ == '__main__':
    unittest.main()
