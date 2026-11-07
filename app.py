#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
«Счастье есть» — локальный сервер сайта и админ-панели.

Запуск:
    python3 app.py                 # http://0.0.0.0:8080
    PORT=3000 python3 app.py

Пароль администратора при первом запуске создаётся в data/auth.json
и печатается в консоль. Сменить: удалите data/auth.json и перезапустите
(или задайте ADMIN_PASSWORD при первом старте).
"""

import hashlib
import hmac
import json
import mimetypes
import os
import secrets
import shutil
import sys
import threading
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
ADMIN = os.path.join(ROOT, 'admin')
DATA = os.path.join(ROOT, 'data')
UPLOADS = os.path.join(DATA, 'uploads')
CONTENT = os.path.join(DATA, 'content.json')
LEADS = os.path.join(DATA, 'leads.json')
AUTH = os.path.join(DATA, 'auth.json')

PORT = int(os.environ.get('PORT', '8080'))
HOST = os.environ.get('HOST', '0.0.0.0')
MAX_BODY = 8 * 1024 * 1024  # 8 МБ
ALLOWED_UPLOAD = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg', '.avif'}

LOCK = threading.Lock()
SESSIONS = set()

PAGES = {
    '': 'index.html',
    '/': 'index.html',
    '/index.html': 'index.html',
    '/menu.html': 'menu.html',
    '/master-classes.html': 'master-classes.html',
    '/events.html': 'events.html',
    '/gallery.html': 'gallery.html',
    '/contacts.html': 'contacts.html',
    '/booking.html': 'booking.html',
    '/privacy.html': 'privacy.html',
}


# ------------------------------------------------------------------ утилиты
def ensure_dirs():
    for path in (DATA, UPLOADS):
        os.makedirs(path, exist_ok=True)


def read_json(path, default):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path, payload):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def hash_password(password, salt):
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()


def ensure_auth():
    if os.path.exists(AUTH):
        return
    password = os.environ.get('ADMIN_PASSWORD') or 'schastye2026'
    salt = secrets.token_hex(12)
    write_json(AUTH, {'salt': salt, 'hash': hash_password(password, salt)})
    print('=' * 62)
    print('  Админ-панель: http://localhost:%d/admin/  (пароль: %s)' % (PORT, password))
    print('  Пароль хранится в data/auth.json — смените его в настройках панели.')
    print('=' * 62)


def ensure_content():
    if os.path.exists(CONTENT):
        return
    write_json(CONTENT, {'photos': {}, 'promos': []})


# ------------------------------------------------------------------ сервер
class Handler(SimpleHTTPRequestHandler):
    server_version = 'HappinessSite/1.0'
    protocol_version = 'HTTP/1.1'

    # -------------------------------------------------- логирование
    def log_message(self, fmt, *args):
        sys.stderr.write('[%s] %s\n' % (datetime.now().strftime('%H:%M:%S'), fmt % args))

    # -------------------------------------------------- helpers
    def _send(self, code, body=b'', ctype='text/plain; charset=utf-8', extra=None):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store' if ctype.startswith('application/json') else 'no-cache')
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def _json(self, code, payload, extra=None):
        self._send(code, json.dumps(payload, ensure_ascii=False),
                   'application/json; charset=utf-8', extra)

    def _body(self):
        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            return None
        if length <= 0 or length > MAX_BODY:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    def _cookies(self):
        raw = self.headers.get('Cookie') or ''
        out = {}
        for part in raw.split(';'):
            if '=' in part:
                k, v = part.split('=', 1)
                out[k.strip()] = v.strip()
        return out

    def _is_admin(self):
        return self._cookies().get('hsid') in SESSIONS

    def _require_admin(self):
        if self._is_admin():
            return True
        self._json(401, {'error': 'Требуется вход в админ-панель'})
        return False

    # -------------------------------------------------- статика
    def _file(self, path):
        if not os.path.isfile(path):
            return False
        ctype = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        if ctype.startswith('text/') or ctype in ('application/javascript', 'image/svg+xml'):
            ctype += '; charset=utf-8'
        with open(path, 'rb') as f:
            body = f.read()
        self._send(200, body, ctype)
        return True

    def do_GET(self):
        path = unquote(urlparse(self.path).path)

        if path.startswith('/api/'):
            return self.api_get(path)

        if path in PAGES:
            return self._file(os.path.join(SITE, PAGES[path])) or self._not_found()

        # «красивые» адреса: /menu, /events/, /master-classes без .html
        clean = path.rstrip('/')
        if clean and not os.path.splitext(clean)[1]:
            pretty = clean.lstrip('/') + '.html'
            if pretty in PAGES.values():
                return self._file(os.path.join(SITE, pretty)) or self._not_found()

        if path in ('/admin', '/admin/'):
            return self._file(os.path.join(ADMIN, 'index.html')) or self._not_found()

        if path.startswith('/uploads/'):
            name = os.path.basename(path)
            if not name or name.startswith('.'):
                return self._not_found()
            return self._file(os.path.join(UPLOADS, name)) or self._not_found()

        if path == '/data/content.json':
            return self._file(CONTENT) or self._json(404, {'error': 'no content'})

        # только ассеты сайта и админки — остальное (data/, app.py) наружу не отдаём
        for base in (SITE, ADMIN):
            candidate = os.path.normpath(os.path.join(base, path.lstrip('/')))
            if os.path.isfile(candidate) and self._safe(base, candidate):
                return self._file(candidate)

        return self._not_found()

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith('/api/'):
            return self.api_post(path)
        self._json(404, {'error': 'not found'})

    # -------------------------------------------------- API: чтение
    def api_get(self, path):
        if path == '/api/session':
            return self._json(200, {'authenticated': self._is_admin()})

        if path == '/api/content':
            return self._json(200, read_json(CONTENT, {'photos': {}, 'promos': []}))

        if path == '/api/leads':
            if not self._require_admin():
                return
            leads = read_json(LEADS, [])
            return self._json(200, {'leads': leads, 'total': len(leads)})

        if path == '/api/export.csv':
            if not self._require_admin():
                return
            return self.export_csv()

        if path == '/api/stats':
            if not self._require_admin():
                return
            leads = read_json(LEADS, [])
            by_status = {}
            for lead in leads:
                by_status[lead.get('status', 'new')] = by_status.get(lead.get('status', 'new'), 0) + 1
            return self._json(200, {
                'total': len(leads),
                'new': by_status.get('new', 0),
                'progress': by_status.get('progress', 0),
                'done': by_status.get('done', 0),
                'subscribers': sum(1 for l in leads if l.get('subscribe'))
            })

        self._json(404, {'error': 'unknown endpoint'})

    # -------------------------------------------------- API: запись
    def api_post(self, path):
        if path == '/api/login':
            return self.login()
        if path == '/api/logout':
            SESSIONS.discard(self._cookies().get('hsid'))
            return self._json(200, {'ok': True}, {'Set-Cookie': 'hsid=; Path=/; Max-Age=0'})
        if path == '/api/leads':
            return self.create_lead()
        if path == '/api/content':
            return self.save_content()
        if path == '/api/upload':
            return self.upload()
        if path == '/api/password':
            return self.change_password()
        if path == '/api/leads/status':
            return self.update_status()
        if path == '/api/leads/delete':
            return self.delete_lead()
        self._json(404, {'error': 'unknown endpoint'})

    # -------------------------------------------------- /api/login
    def login(self):
        body = self._body() or {}
        auth = read_json(AUTH, None)
        if not auth:
            return self._json(500, {'error': 'auth не инициализирован'})
        candidate = hash_password(str(body.get('password', '')), auth['salt'])
        if not hmac.compare_digest(candidate, auth['hash']):
            return self._json(401, {'error': 'Неверный пароль'})
        token = secrets.token_urlsafe(24)
        SESSIONS.add(token)
        return self._json(200, {'ok': True},
                          {'Set-Cookie': 'hsid=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=86400' % token})

    def change_password(self):
        if not self._require_admin():
            return
        body = self._body() or {}
        new = str(body.get('password', '')).strip()
        if len(new) < 6:
            return self._json(400, {'error': 'Пароль минимум 6 символов'})
        salt = secrets.token_hex(12)
        write_json(AUTH, {'salt': salt, 'hash': hash_password(new, salt)})
        self._json(200, {'ok': True})

    # -------------------------------------------------- заявки
    def create_lead(self):
        body = self._body()
        if not body:
            return self._json(400, {'error': 'Некорректный запрос'})
        phone = str(body.get('phone', '')).strip()
        name = str(body.get('name', '')).strip()
        if len(name) < 2 or len(phone.replace(' ', '')) < 10:
            return self._json(422, {'error': 'Укажите имя и телефон'})
        if not body.get('consent'):
            return self._json(422, {'error': 'Нужно согласие на обработку данных'})

        lead = {
            'id': secrets.token_hex(8),
            'name': name,
            'phone': phone,
            'email': str(body.get('email', '') or '—'),
            'type': str(body.get('form', 'Заявка')),
            'topic': str(body.get('topic', '') or '—'),
            'date': str(body.get('date', '') or '—'),
            'guests': str(body.get('guests', '') or '—'),
            'message': str(body.get('message', '') or ''),
            'subscribe': bool(body.get('subscribe')),
            'consent': True,
            'page': str(body.get('page', '')),
            'createdAt': datetime.now().isoformat(timespec='seconds'),
            'status': 'new'
        }
        with LOCK:
            leads = read_json(LEADS, [])
            leads.insert(0, lead)
            write_json(LEADS, leads[:2000])
        print('  → новая заявка: %s, %s (%s)' % (lead['name'], lead['phone'], lead['type']))
        return self._json(201, {'ok': True, 'id': lead['id']})

    def update_status(self):
        if not self._require_admin():
            return
        body = self._body() or {}
        lead_id = body.get('id')
        status = body.get('status')
        if status not in ('new', 'progress', 'done', 'cancel'):
            return self._json(400, {'error': 'Неизвестный статус'})
        with LOCK:
            leads = read_json(LEADS, [])
            for lead in leads:
                if lead.get('id') == lead_id:
                    lead['status'] = status
                    write_json(LEADS, leads)
                    return self._json(200, {'ok': True})
        return self._json(404, {'error': 'Заявка не найдена'})

    def delete_lead(self):
        if not self._require_admin():
            return
        body = self._body() or {}
        lead_id = body.get('id')
        with LOCK:
            leads = read_json(LEADS, [])
            rest = [l for l in leads if l.get('id') != lead_id]
            write_json(LEADS, rest)
        return self._json(200, {'ok': True, 'removed': len(leads) - len(rest)})

    def export_csv(self):
        import csv
        import io
        leads = read_json(LEADS, [])
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=';')
        writer.writerow(['Имя', 'Телефон', 'E-mail', 'Тип', 'Тема', 'Дата', 'Гостей',
                         'Комментарий', 'Подписка', 'Получена', 'Статус'])
        for lead in leads:
            writer.writerow([lead.get('name', ''), lead.get('phone', ''), lead.get('email', ''),
                             lead.get('type', ''), lead.get('topic', ''), lead.get('date', ''),
                             lead.get('guests', ''), lead.get('message', ''),
                             'да' if lead.get('subscribe') else 'нет',
                             lead.get('createdAt', ''), lead.get('status', '')])
        data = ('\ufeff' + buf.getvalue()).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv; charset=utf-8')
        self.send_header('Content-Disposition',
                         'attachment; filename="happiness-leads-%s.csv"' % datetime.now().strftime('%Y-%m-%d'))
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # -------------------------------------------------- контент
    def save_content(self):
        if not self._require_admin():
            return
        body = self._body()
        if not isinstance(body, dict):
            return self._json(400, {'error': 'Ожидается JSON-объект'})
        current = read_json(CONTENT, {'photos': {}, 'promos': []})
        if 'photos' in body and isinstance(body['photos'], dict):
            current['photos'] = {k: str(v) for k, v in body['photos'].items()}
        if 'promos' in body and isinstance(body['promos'], list):
            promos = []
            for p in body['promos']:
                if not isinstance(p, dict):
                    continue
                promos.append({
                    'title': str(p.get('title', ''))[:140],
                    'text': str(p.get('text', ''))[:600],
                    'badge': str(p.get('badge', ''))[:40],
                    'until': str(p.get('until', ''))[:40]
                })
            current['promos'] = promos
        write_json(CONTENT, current)
        return self._json(200, {'ok': True, 'content': current})

    def upload(self):
        if not self._require_admin():
            return
        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            return self._json(400, {'error': 'Файл слишком большой (максимум 8 МБ)'})
        raw = self.rfile.read(length)
        ctype = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in ctype:
            return self._json(400, {'error': 'Нужен multipart/form-data'})
        boundary = ctype.split('boundary=')[-1].strip().strip('"').encode()
        filename, data = self.parse_multipart(raw, boundary)
        if not data:
            return self._json(400, {'error': 'Файл не найден в запросе'})
        ext = os.path.splitext(filename or '')[1].lower()
        if ext not in ALLOWED_UPLOAD:
            return self._json(400, {'error': 'Допустимы форматы: %s' % ', '.join(sorted(ALLOWED_UPLOAD))})
        name = '%s-%s%s' % (datetime.now().strftime('%Y%m%d%H%M%S'), secrets.token_hex(4), ext)
        with open(os.path.join(UPLOADS, name), 'wb') as f:
            f.write(data)
        return self._json(200, {'ok': True, 'url': '/uploads/' + name})

    @staticmethod
    def parse_multipart(raw, boundary):
        marker = b'--' + boundary
        for part in raw.split(marker):
            if b'\r\n\r\n' not in part:
                continue
            head, body = part.split(b'\r\n\r\n', 1)
            if b'filename=' not in head:
                continue
            body = body.rstrip(b'\r\n')
            name = ''
            # Заголовок вида: Content-Disposition: form-data; name="file"; filename="photo.jpg"
            for line in head.split(b'\r\n'):
                if b'filename=' not in line:
                    continue
                chunk = line.split(b'filename=', 1)[-1].strip()
                if chunk.startswith(b'"'):
                    end = chunk.find(b'"', 1)
                    chunk = chunk[1:end] if end != -1 else chunk[1:]
                name = chunk.decode('utf-8', 'ignore').strip()
            return name, body
        return '', b''

    # -------------------------------------------------- прочее
    @staticmethod
    def _safe(base, candidate):
        base_abs = os.path.abspath(base)
        return os.path.abspath(candidate).startswith(base_abs + os.sep) or \
            os.path.abspath(candidate) == base_abs

    def _not_found(self):
        page = os.path.join(SITE, '404.html')
        if os.path.isfile(page):
            with open(page, 'rb') as f:
                return self._send(404, f.read(), 'text/html; charset=utf-8')
        self._send(404,
                   '<!DOCTYPE html><html lang="ru"><meta charset="utf-8">'
                   '<title>Страница не найдена</title>'
                   '<body style="font-family:sans-serif;padding:40px">'
                   '<h1>Страница не найдена</h1>'
                   '<p><a href="/">На главную сайта</a> · <a href="/admin/">Админ-панель</a></p>',
                   'text/html; charset=utf-8')


def main():
    ensure_dirs()
    ensure_auth()
    ensure_content()
    index_file = os.path.join(SITE, 'index.html')
    if not os.path.isfile(index_file):
        print('ВНИМАНИЕ: не найден %s — соберите страницы: python3 build_pages.py' % index_file)
    if not os.path.exists(LEADS):
        write_json(LEADS, [])
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print('\n  «Счастье есть» — сайт:   http://localhost:%d/' % PORT)
    print('  Админ-панель:            http://localhost:%d/admin/' % PORT)
    print('  Остановить: Ctrl+C\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nОстановлено.')
        server.server_close()


if __name__ == '__main__':
    main()
