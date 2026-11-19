import shutil
import tempfile
import pathlib
import unittest

from cargo_package_health_auditor.audit import audit_workspace

class TestAudit(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = pathlib.Path(tempfile.mkdtemp())
        # crate1: all good
        crate1 = self.tmp_dir / "crate1"
        crate1.mkdir()
        (crate1 / "Cargo.toml").write_text(
            '[package]\nname = "crate1"\nversion = "0.1.0"\nlicense = "MIT"\n'
        )
        (crate1 / "README.md").write_text("# Crate1")
        (crate1 / "LICENSE").write_text("MIT License text")
        # crate2: missing README, license file, license field
        crate2 = self.tmp_dir / "crate2"
        crate2.mkdir()
        (crate2 / "Cargo.toml").write_text(
            '[package]\nname = "crate2"\nversion = "0.1.0"\n'
        )
        # crate3: license field Apache-2.0, license file missing SPDX
        crate3 = self.tmp_dir / "crate3"
        crate3.mkdir()
        (crate3 / "Cargo.toml").write_text(
            '[package]\nname = "crate3"\nversion = "0.1.0"\nlicense = "Apache-2.0"\n'
        )
        (crate3 / "README.txt").write_text("Crate3 readme")
        (crate3 / "LICENSE").write_text("Some other license text")
        # crate4: license field unknown
        crate4 = self.tmp_dir / "crate4"
        crate4.mkdir()
        (crate4 / "Cargo.toml").write_text(
            '[package]\nname = "crate4"\nversion = "0.1.0"\nlicense = "Unknown-License"\n'
        )
        (crate4 / "README.rst").write_text("Crate4 readme")
        (crate4 / "LICENSE-foo").write_text("Unknown-License text")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_audit(self):
        reports = audit_workspace(self.tmp_dir)
        reports_dict = {r["crate_path"]: r for r in reports}
        # crate1
        r1 = reports_dict["crate1"]
        self.assertTrue(r1["readme_present"])
        self.assertTrue(r1["license_file_present"])
        self.assertTrue(r1["license_field_present"])
        self.assertTrue(r1["license_field_valid"])
        self.assertTrue(r1["license_file_contains_spdx"])
        # crate2
        r2 = reports_dict["crate2"]
        self.assertFalse(r2["readme_present"])
        self.assertFalse(r2["license_file_present"])
        self.assertFalse(r2["license_field_present"])
        self.assertFalse(r2["license_field_valid"])
        self.assertFalse(r2["license_file_contains_spdx"])
        # crate3
        r3 = reports_dict["crate3"]
        self.assertTrue(r3["readme_present"])
        self.assertTrue(r3["license_file_present"])
        self.assertTrue(r3["license_field_present"])
        self.assertTrue(r3["license_field_valid"])
        self.assertFalse(r3["license_file_contains_spdx"])
        # crate4
        r4 = reports_dict["crate4"]
        self.assertTrue(r4["readme_present"])
        self.assertTrue(r4["license_file_present"])
        self.assertTrue(r4["license_field_present"])
        self.assertFalse(r4["license_field_valid"])
        self.assertFalse(r4["license_file_contains_spdx"])

if __name__ == "__main__":
    unittest.main()
