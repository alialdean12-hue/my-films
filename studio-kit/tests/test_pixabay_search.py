"""Offline contract checks; no real credential or network access."""
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch
from email.message import Message

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import pixabay_search as ps


class StockTest(unittest.TestCase):
    def test_request_and_no_key_in_cache(self):
        calls = []
        def fixture(req, timeout):
            url = urlsplit(req.full_url);calls.append(url)
            self.assertEqual(url.scheme, 'https')
            if url.hostname == 'pixabay.com':
                self.assertEqual(url.path, '/api/videos/')
                q = parse_qs(url.query)
                self.assertEqual(q['key'], ['offline-test']);self.assertEqual(q['q'], ['palm trees'])
                return io.BytesIO(json.dumps({'hits': [{'id': 123, 'pageURL': 'https://pixabay.com/videos/id-123/', 'videos': {'tiny': {'url': 'https://cdn.pixabay.com/video/x.mp4'}}}]}).encode())
            self.assertEqual(url.hostname, 'cdn.pixabay.com');self.assertFalse(url.query)
            self.assertEqual(req.get_header('Range'), 'bytes=0-127')
            r = io.BytesIO(b'\0\0\0\x18ftypisom');r.headers = Message();r.headers['Content-Type'] = 'video/mp4';return r
        with tempfile.TemporaryDirectory() as directory, patch.object(ps.OPENER, 'open', side_effect=fixture):
            data, cached = ps.lookup('videos', 'palm trees', 'offline-test', Path(directory))
            self.assertFalse(cached);self.assertTrue(data['preview']);self.assertEqual(data['pages'], ['https://pixabay.com/videos/id-123/'])
            self.assertTrue(ps.lookup('videos', 'palm trees', 'offline-test', Path(directory))[1]);self.assertEqual(len(calls), 2)
            cache = next(Path(directory).iterdir());text = cache.read_text();self.assertNotIn('offline-test', text);self.assertNotIn('cdn.pixabay.com', text)
            cache.write_text(json.dumps({**data, 'at': data['at'] - ps.DAY - 1}));self.assertFalse(ps.lookup('videos','palm trees','offline-test',Path(directory))[1])

    def test_key_missing_before_network(self):
        with patch.dict(os.environ, {'PIXABAY_KEY':''}), patch.object(ps.OPENER, 'open') as network:
            with self.assertRaisesRegex(ps.LookupFailed, 'PIXABAY_KEY'):ps.main()
            network.assert_not_called()

    def test_sanitized_errors(self):
        url = 'https://pixabay.com/api/?key=offline-test'
        for code,body,expected in [(400, b'Invalid API key offline-test', 'غير صالح'),(403, url.encode(), 'HTTP 403'),(429,b'', 'حدّ الاستخدام')]:
            with patch.object(ps.OPENER,'open',side_effect=HTTPError(url,code,'',{},io.BytesIO(body))):
                with self.assertRaisesRegex(ps.LookupFailed, expected) as cm:ps.search('photos','palm','offline-test')
                self.assertNotIn('offline-test',str(cm.exception))

    def test_only_public_source_pages(self):
        hit={'id':123,'pageURL':'https://pixabay.com/photos/palms-123/'};self.assertEqual(ps.page_link(hit),hit['pageURL'])
        for bad in ['https://example.org/photos/id-123/','https://pixabay.com/photos/id-123/?key=offline-test','https://user@pixabay.com/photos/id-123/']:
            self.assertIsNone(ps.page_link({**hit,'pageURL':bad}))


if __name__=='__main__':unittest.main()
