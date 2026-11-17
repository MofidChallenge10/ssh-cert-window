import datetime as dt, unittest
from ssh_cert_window.core import parse_key_info
FIXTURE='''Type: ssh-ed25519-cert-v01@openssh.com user certificate
Key ID: "deploy-readonly"
Serial: 42
Valid: from 2026-11-01T00:00:00 to 2027-01-01T00:00:00
Principals:
        deploy
        release
'''
class TestParse(unittest.TestCase):
 def test_valid(self):
  now=dt.datetime(2026,11,18,tzinfo=dt.timezone.utc)
  result=parse_key_info(FIXTURE,now=now)
  self.assertEqual(result['status'],'VALID'); self.assertEqual(result['principals'],['deploy','release'])
 def test_expired(self):
  now=dt.datetime(2027,1,2,tzinfo=dt.timezone.utc)
  self.assertEqual(parse_key_info(FIXTURE,now=now)['status'],'EXPIRED')
 def test_bad(self):
  with self.assertRaises(ValueError): parse_key_info('not certificate output')
if __name__=='__main__': unittest.main()
