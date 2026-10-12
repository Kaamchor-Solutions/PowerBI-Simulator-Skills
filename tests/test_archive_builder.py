"""Tests for the standard-library source archive builder."""
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_archive  # noqa: E402


class ArchiveBuilderTests(unittest.TestCase):
    def make_fixture(self, root: Path) -> Path:
        source = root / "fixture-package"
        (source / "docs").mkdir(parents=True)
        (source / "README.md").write_text("fixture\n", encoding="utf-8")
        (source / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
        (source / ".git").mkdir()
        (source / ".git" / "config").write_text("git metadata\n", encoding="utf-8")
        (source / "__pycache__").mkdir()
        (source / "__pycache__" / "module.pyc").write_bytes(b"compiled")
        (source / ".venv").mkdir()
        (source / ".venv" / "marker").write_text("venv\n", encoding="utf-8")
        (source / build_archive.RELEASE_MANIFEST).write_text(
            "# Explicitly approved source files\nREADME.md\ndocs/guide.md\n",
            encoding="utf-8",
        )
        return source

    def test_archive_is_byte_reproducible_sorted_and_excludes_generated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            source = self.make_fixture(Path(temp))
            first, count = build_archive.build_archive_bytes(source)
            second, repeated_count = build_archive.build_archive_bytes(source)
            self.assertEqual((first, count), (second, repeated_count))
            with ZipFile(io.BytesIO(first)) as archive:
                names = archive.namelist()
                self.assertEqual(names, [
                    "fixture-package/",
                    "fixture-package/README.md",
                    "fixture-package/docs/guide.md",
                    "fixture-package/release-manifest.txt",
                ])
                self.assertIsNone(archive.testzip())
                self.assertTrue(all(info.date_time == build_archive.FIXED_TIMESTAMP for info in archive.infolist()))

    def test_archive_omits_private_and_unlisted_files(self):
        with tempfile.TemporaryDirectory() as temp:
            source = self.make_fixture(Path(temp))
            private_files = {
                ".env": "SYNTHETIC_NOT_A_REAL_SECRET\n",
                ".env.local": "SYNTHETIC_NOT_A_REAL_SECRET\n",
                "secrets.json": "{}\n",
                "credentials.json": "{}\n",
                "private-data/customer.csv": "synthetic customer\n",
                "local-data/source.xlsx": "synthetic workbook marker\n",
                "results/report.md": "synthetic report\n",
                "output/report.txt": "unrelated output\n",
                "unrelated-untracked.txt": "not approved for release\n",
            }
            for relative, content in private_files.items():
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            payload, _ = build_archive.build_archive_bytes(source)
            with ZipFile(io.BytesIO(payload)) as archive:
                names = set(archive.namelist())

        self.assertEqual(names, {
            "fixture-package/",
            "fixture-package/README.md",
            "fixture-package/docs/guide.md",
            "fixture-package/release-manifest.txt",
        })

    def test_write_archive_verifies_bytes_and_sha256(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = self.make_fixture(base)
            output = base / "fixture-package.zip"
            count, digest = build_archive.write_archive(output, source, verify_reproducible=True)
            payload = output.read_bytes()
            self.assertEqual(count, 3)
            self.assertEqual(digest, hashlib.sha256(payload).hexdigest())
            with ZipFile(output) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn("fixture-package/docs/guide.md", archive.namelist())

    def test_archive_output_inside_source_tree_is_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            source = self.make_fixture(Path(temp))
            output = source / "nested.zip"
            with self.assertRaisesRegex(ValueError, "outside the source tree"):
                build_archive.write_archive(output, source)
            self.assertFalse(output.exists())

    def test_symlink_inputs_are_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            source = self.make_fixture(base)
            external = base / "external.txt"
            external.write_text("outside\n", encoding="utf-8")
            link = source / "external-link.txt"
            link.symlink_to(external)
            manifest = source / build_archive.RELEASE_MANIFEST
            manifest.write_text(manifest.read_text(encoding="utf-8") + "external-link.txt\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "symlink"):
                build_archive.build_archive_bytes(source)

    def test_release_manifest_is_required_and_paths_are_confined(self):
        with tempfile.TemporaryDirectory() as temp:
            source = self.make_fixture(Path(temp))
            manifest = source / build_archive.RELEASE_MANIFEST
            manifest.unlink()
            with self.assertRaisesRegex(ValueError, "Required release manifest"):
                build_archive.build_archive_bytes(source)

            manifest.write_text("../outside.txt\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Unsafe release-manifest path"):
                build_archive.build_archive_bytes(source)

            manifest.write_text("missing.csv\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "does not exist"):
                build_archive.build_archive_bytes(source)


if __name__ == "__main__":
    unittest.main()
