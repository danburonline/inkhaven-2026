"""Regression checks for generated Essence cards. Run after tools/build.py."""
import json
from pathlib import Path
import unittest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent

class EssenceTests(unittest.TestCase):
    def test_day_seven_card(self):
        soup = BeautifulSoup((ROOT / '7-augmented-cognition/index.html').read_text(), 'html.parser')
        cards = soup.select('aside.essence')
        self.assertEqual(len(cards), 1, 'one Day 7 Essence card required')
        card = cards[0]
        self.assertEqual(card.select_one('.essence-label').text, 'TL;DR')
        self.assertEqual(soup.select_one('.toc a[href="#sec-essence"]').text, 'TL;DR')
        self.assertEqual(card.select_one('.x-callout-text span').text, 'Replies and discussion happen there.')
        text = card.select_one('.essence-text').text
        self.assertLess(len(text.split()), 50)
        self.assertLessEqual(text.count('.'), 2)
        self.assertEqual(text, json.loads((ROOT / 'tools/essence.json').read_text())['7-augmented-cognition'])
        self.assertEqual(card.select_one('a.x-callout')['href'], 'https://x.com/danburonline/status/2123299553327849974')
        self.assertEqual(len(soup.select('a.x-callout')), 1)
        self.assertIsNotNone(card.find_previous_sibling('p').select_one('picture'))
        self.assertIsNotNone(soup.select_one('.toc a[href="#sec-essence"]'))
        self.assertIn('1,821 words', soup.select_one('.post-byline').text)

    def test_every_post_has_a_card(self):
        essences = json.loads((ROOT / 'tools/essence.json').read_text())
        pages = sorted(ROOT.glob('[0-9]*-*/index.html'))
        self.assertGreaterEqual(len(pages), 8)
        for page in pages:
            slug = page.parent.name
            soup = BeautifulSoup(page.read_text(), 'html.parser')
            cards = soup.select('aside.essence')
            self.assertEqual(len(cards), 1, slug)
            text = cards[0].select_one('.essence-text').text
            self.assertEqual(text, essences[slug])
            self.assertLess(len(text.split()), 50, slug)
            self.assertNotIn('\u2014', text)
            self.assertNotIn('thinking trace', text.lower())
            self.assertLessEqual(len([c for c in text if c in '.!?']), 2, slug)
            self.assertEqual(len(soup.select('a.x-callout')), 1, slug)
            self.assertIsNotNone(cards[0].select_one('a.x-callout[href^="https://x.com/danburonline/status/"]'), slug)
            self.assertIsNotNone(soup.select_one('.toc a[href="#sec-essence"]'), slug)

if __name__ == '__main__':
    unittest.main()
