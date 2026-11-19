"""Find film references on Pixabay. Only publish source pages, never API/media URLs or the key.

The Actions job passes PIXABAY_KEY only to this process. No extra Python packages required.
On a fresh query: one SafeSearch request per media type and at most 128 preview bytes per type.
The rendered public result (not the authenticated response) is reusable for 24 hours.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from http.client import HTTPException
from urllib import error, parse, request

API = 'https://pixabay.com/api/'
DAY = 86400


class LookupFailed(Exception):
    """Only safe, deliberately authored messages may reach the run summary."""


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward an authenticated URL to a redirected host.


OPENER = request.build_opener(NoRedirect())


def official(url, hosts):
    if not isinstance(url, str):
        return False
    try:
        u = parse.urlsplit(url)
        return u.scheme == 'https' and u.netloc in hosts and not u.fragment
    except ValueError:
        return False


def page_link(hit):
    url = hit.get('pageURL'); i = hit.get('id')
    if type(i) is not int or i <= 0 or not official(url, {'pixabay.com', 'www.pixabay.com'}):
        return None
    u = parse.urlsplit(url)
    if u.query or not re.fullmatch(r'/[\w./%~-]*[-/]' + str(i) + r'/?', u.path):
        return None
    return 'https://pixabay.com' + parse.quote(u.path, safe='/%~-')


def search(kind, query, key):
    params = {'key': key, 'q': query, 'safesearch': 'true', 'per_page': 5}
    if kind == 'photos':
        params['image_type'] = 'photo'
    url = API + ('videos/' if kind == 'videos' else '') + '?' + parse.urlencode(params)
    req = request.Request(url, headers={'User-Agent': 'my-films-stock/1', 'Accept': 'application/json'})
    try:
        with OPENER.open(req, timeout=15) as res:
            raw = res.read(524289)
        if len(raw) > 524288:
            raise LookupFailed('استجابة البحث كبيرة على نحو غير متوقع.')
        hits = json.loads(raw)['hits']
        if not isinstance(hits, list):
            raise ValueError
        return hits
    except error.HTTPError as exc:
        # Some API errors can echo the request: inspect a small prefix, but never print it.
        with exc:
            msg = exc.read(2048).lower()
        if b'key' in msg and (b'invalid' in msg or b'not a valid' in msg):
            raise LookupFailed('أفادت Pixabay بأن مفتاح API غير صالح.') from None
        if exc.code == 429:
            raise LookupFailed('بلغت طلبات Pixabay حدّ الاستخدام؛ حاول لاحقًا.') from None
        raise LookupFailed(f'رفضت خدمة البحث الطلب (HTTP {exc.code})؛ لم نتحقّق من المفتاح.') from None
    except (OSError, HTTPException, ValueError, KeyError, TypeError):
        raise LookupFailed('تعذّر الاتصال بخدمة البحث أو قراءة استجابتها.') from None


def probe(hit, kind):
    """Check a bounded prefix, not a standalone download or redistribution."""
    if kind == 'photos':
        url = hit.get('previewURL')
    else:
        variants = hit.get('videos') or {}
        url = next((v['url'] for tag in ('tiny', 'small', 'medium')
                    if isinstance((v := variants.get(tag)), dict) and v.get('url')), None)
    if not official(url, {'cdn.pixabay.com', 'pixabay.com', 'www.pixabay.com'}):
        return False
    try:
        req = request.Request(url, headers={'Range': 'bytes=0-127', 'User-Agent': 'my-films-stock/1'})
        with OPENER.open(req, timeout=10) as res:
            sample = res.read(128); mime = res.headers.get_content_type()
        if not sample:
            return False
        if kind == 'videos':
            return mime.startswith('video/') or sample[4:8] == b'ftyp'
        return mime.startswith('image/') or sample.startswith((b'\xff\xd8\xff', b'\x89PNG'))
    except (OSError, HTTPException, ValueError):
        return False


def lookup(kind, query, key, cache):
    path = cache / hashlib.sha256((kind + '\0' + query).encode()).hexdigest()
    now = time.time()
    try:
        result = json.loads(path.read_text())
        if 0 <= now - result['at'] < DAY:
            return result, True
    except (FileNotFoundError, KeyError, ValueError, TypeError):
        pass
    hits = search(kind, query, key)
    pairs = [(h, u) for h in hits if isinstance(h, dict) and (u := page_link(h))]
    if hits and not pairs:
        raise LookupFailed('وصل ردّ بحث، لكن بلا روابط مصادر صالحة للعرض.')
    result = {'at': now, 'pages': [u for _, u in pairs], 'preview': bool(pairs) and probe(pairs[0][0], kind)}
    path.write_text(json.dumps(result))
    return result, False


def main():
    key = os.environ.get('PIXABAY_KEY', '').strip()
    if not key:
        raise LookupFailed('لم يصل سرّ PIXABAY_KEY إلى هذه المهمة. تحقّق من اسمه في Repository secrets.')
    query = os.environ.get('STOCK_QUERY', '').strip() or (Path(__file__).parents[1] / 'stock-query.txt').read_text().strip()
    if not 1 <= len(query) <= 100 or any(ord(c) < 32 for c in query):
        raise LookupFailed('أدخل عبارة بحث واحدة، من 1 إلى 100 حرف.')
    cache = Path(os.environ.get('RUNNER_TEMP') or Path.home() / '.cache') / 'my-films-pixabay-public'
    cache.mkdir(parents=True, exist_ok=True)
    for kind, label in [('photos', 'صور'), ('videos', 'فيديو')]:
        result, cached = lookup(kind, query, key, cache)
        note = 'نتيجة محفوظة خلال 24 ساعة؛ لم يُختبَر المفتاح مجددًا' if cached else 'استجاب بحث Pixabay الآن'
        pages = result['pages']
        details = '؛ قُرئت بداية ملف المعاينة' if result['preview'] else ('؛ لم تتأكد معاينة الملف' if pages else '؛ لا نتائج لهذه العبارة')
        status = f'{label}: {note} — {len(pages)}{details}.'
        # Only the validated public landing pages leave this process. No raw errors or stock binaries.
        print(status, *pages, sep='\n')
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print(f'::notice title=Pixabay {kind}::{status} ' + (pages[0] if pages else ''))
        if info := os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(info, 'a', encoding='utf-8') as f:
                f.write(f'### {status}\n' + ''.join(f'- [Pixabay · {label} {i}]({url})\n' for i, url in enumerate(pages, 1)) + '\n')


if __name__ == '__main__':
    try:
        main()
    except LookupFailed as exc:
        print(('::error::' if os.environ.get('GITHUB_ACTIONS') == 'true' else '') + str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception:
        # Third-party exception messages may contain URLs. Never dump a traceback with request data.
        sys.exit('تعذّر إكمال اختبار Pixabay. لم تُطبع بيانات الطلب أو المفتاح.')
