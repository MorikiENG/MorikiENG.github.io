"""Run with: python3 -m unittest discover -s tests -v (standard library only)."""
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://morikieng.github.io/'
FILES = ['index.html', 'cad.html', '3d-print.html', 'engineering.html',
         'software.html', 'works.html', 'company.html', 'contact.html']
PAGES = FILES + ['en/' + f for f in FILES]


def canonical(path):
    return BASE + (path[:-10] if path.endswith('index.html') else path)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.feed((ROOT / path).read_text())

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def matching(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


class SEOTests(unittest.TestCase):
    def test_metadata_and_language_pairs(self):
        titles, descriptions = [], []
        for path in PAGES:
            p = Page(path)
            self.assertEqual(p.matching('html')[0]['lang'], 'en' if path.startswith('en/') else 'ja')
            self.assertEqual(len(p.matching('title')), 1)
            from re import search
            titles.append(search(r'<title>(.*?)</title>', (ROOT / path).read_text())[1])
            d = p.matching('meta', name='description')
            self.assertEqual(len(d), 1)
            self.assertTrue(d[0]['content'].strip())
            descriptions.append(d[0]['content'])
            self.assertEqual(p.matching('link', rel='canonical'), [{'rel': 'canonical', 'href': canonical(path)}])
            self.assertEqual(p.matching('meta', property='og:url')[0]['content'], canonical(path))
            self.assertEqual(p.matching('meta', property='og:description')[0]['content'], d[0]['content'])
            jp = path.removeprefix('en/')
            for lang, target in [('ja', jp), ('en', 'en/' + jp), ('x-default', jp)]:
                self.assertEqual(p.matching('link', rel='alternate', hreflang=lang),
                                 [{'rel': 'alternate', 'hreflang': lang, 'href': canonical(target)}])
            for a in p.matching('meta'):
                if a.get('name', '').lower() in ('robots', 'googlebot', 'bingbot'):
                    self.assertNotIn('noindex', a.get('content', '').lower())
        self.assertEqual(len(set(titles)), 16)
        self.assertEqual(len(set(descriptions)), 16)

    def test_sitemap(self):
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
        entries = ET.parse(ROOT / 'sitemap.xml').findall('s:url', ns)
        self.assertEqual(len(entries), 16)
        self.assertEqual({e.find('s:loc', ns).text for e in entries}, {canonical(p) for p in PAGES})
        for e in entries:
            path = e.find('s:loc', ns).text.removeprefix(BASE)
            jp = path.removeprefix('en/') or 'index.html'
            self.assertEqual({a.attrib['hreflang']: a.attrib['href'] for a in e.findall('x:link', ns)},
                             {'ja': canonical(jp), 'en': canonical('en/' + jp), 'x-default': canonical(jp)})

    def test_robots(self):
        parser = RobotFileParser()
        parser.parse((ROOT / 'robots.txt').read_text().splitlines())
        self.assertEqual(parser.site_maps(), [BASE + 'sitemap.xml'])
        for path in PAGES:
            for agent in ['Googlebot', 'bingbot', '*']:
                self.assertTrue(parser.can_fetch(agent, canonical(path)))

    def test_local_links_assets_and_fragments(self):
        for path in PAGES:
            p = Page(path)
            for tag, a in p.tags:
                key = 'href' if tag in ['a', 'link'] else 'src' if tag in ['script', 'img'] else 'srcset' if tag == 'source' else None
                if not key or key not in a:
                    continue
                u = urlsplit(urljoin(BASE + path, a[key]))
                if u.netloc != urlsplit(BASE).netloc:
                    continue
                f = ROOT / u.path.lstrip('/')
                if f.is_dir():
                    f = f / 'index.html'
                self.assertTrue(f.is_file(), (path, a[key]))
                if u.fragment:
                    target = Page(f.relative_to(ROOT))
                    self.assertTrue(any(v.get('id') == u.fragment for _, v in target.tags), (path, a[key]))

    def test_organization(self):
        import re
        organizations = []
        for path in ['index.html', 'en/index.html']:
            raw = re.findall(r'<script type="application/ld\+json">(.*?)</script>', (ROOT / path).read_text(), re.S)
            self.assertEqual(len(raw), 1)
            data = json.loads(raw[0])
            self.assertEqual(data['@type'], 'Organization')
            self.assertEqual(data['url'], BASE)
            self.assertEqual(set(data), {'@context', '@type', '@id', 'name', 'alternateName', 'url', 'logo', 'email'})
            organizations.append(data)
        self.assertEqual(organizations[0], organizations[1])


if __name__ == '__main__':
    unittest.main()
