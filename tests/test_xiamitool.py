from xiamitool.xiamitool import Account, Login, Signin
import unittest

#test account
usrname = input('username')
passwd = input('password')

class TestXiami(unittest.TestCase):
  def test_creation(self):
    u = 'username'
    p = 'pwpwpw'
    tt  = Login(u,p)
    self.assertEqual(tt.email,  u)
    self.assertEqual(tt.password,  p)
    self.assertFalse(tt.loggedin)

  def test_fill_form(self):
      u ='ddd'
      p = 'sdfdsf'
      ec = Login(u,p)
      ec.fill_form()
      self.assertEqual(ec.form['password'],p)
      self.assertEqual(ec.form['email'],u)
      ec.logout()

  def test_login_succ(self):
      u = usrname
      p = passwd
      ttt = Login(u,p)
      ttt.login()
      self.assertTrue(ttt.loggedin)
      self.assertEqual(len(ttt.session.cookies), 4)
      ttt.logout()

  def test_login_fail(self):
      u = 'akdsjl@gmail.com'
      p = 'abkjafl'
      ftt = Login(u,p)
      self.assertFalse(ftt.loggedin)
      ftt.logout()

  def test_day(self):
      u = usrname
      p = passwd
      rttt = Signin(u,p)
      rttt.login()
      rttt.day()
      self.assertNotEqual(rttt.signedday,0)
      rttt.logout()
  def test_sign(self):
      u = usrname
      p = passwd
      rttt = Signin(u,p)
      rttt.login()
      rttt.day()
      d = rttt.signedday
      self.assertTrue(rttt.signin())
      rttt.logout()


if __name__ == '__main__':
    unittest.main()
