from pathlib import Path
import re
import unittest


class TestHomePage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = Path('index.html').read_text(encoding='utf-8')

    def test_no_placeholder_values_remain(self):
        placeholders = [
            'your.email@example.com',
            'your-github-username',
        ]
        for placeholder in placeholders:
            self.assertNotIn(placeholder, self.content)

    def test_document_is_real_html_not_markdown(self):
        self.assertIn('<!doctype html>', self.content.lower())
        self.assertNotIn('\n---\n', self.content)

    def test_github_links_use_same_username(self):
        profile = re.search(r'https://github\.com/([\w-]+)', self.content)
        stats = re.search(r'github-readme-stats\.vercel\.app/api\?username=([\w-]+)', self.content)
        views = re.search(r'komarev\.com/ghpvc/\?username=([\w-]+)', self.content)
        self.assertIsNotNone(profile)
        self.assertIsNotNone(stats)
        self.assertIsNotNone(views)
        self.assertEqual(profile.group(1), stats.group(1))
        self.assertEqual(profile.group(1), views.group(1))

    def test_core_sections_exist_for_navigation(self):
        for section_id in ('about', 'projects', 'skills', 'contact'):
            self.assertIn(f'id="{section_id}"', self.content)

    def test_interactive_ui_hooks_exist(self):
        self.assertIn('id="theme-toggle"', self.content)
        self.assertIn('localStorage.setItem(', self.content)
        self.assertIn('IntersectionObserver', self.content)


if __name__ == '__main__':
    unittest.main()
