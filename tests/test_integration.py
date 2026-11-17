import shutil, subprocess, tempfile, unittest
from pathlib import Path
from ssh_cert_window.core import inspect_certificate

@unittest.skipUnless(shutil.which("ssh-keygen"), "openssh-client is not installed")
class OpenSSHIntegration(unittest.TestCase):
    def test_generated_user_certificate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(root / "ca")], check=True)
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(root / "user")], check=True)
            subprocess.run(["ssh-keygen", "-q", "-s", str(root / "ca"), "-I", "ci-deploy", "-n", "deploy", "-V", "+1d", str(root / "user.pub")], check=True)
            result = inspect_certificate(root / "user-cert.pub")
            self.assertEqual(result["key_id"], "ci-deploy")
            self.assertIn("deploy", result["principals"])
            self.assertIn(result["status"], {"VALID", "EXPIRING_SOON"})

if __name__ == "__main__":
    unittest.main()
