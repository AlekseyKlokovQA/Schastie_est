#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборка статического сайта для GitHub Pages.

GitHub Pages раздаёт только файлы внутри выбранной папки и не умеет
отдавать ничего выше её корня. Локальный сервер app.py берёт фото и
акции из data/content.json (уровнем выше site/), а в docs/ этот путь
недоступен. Поэтому здесь:

  1. build_pages.py собирает html в docs/ (GH_PAGES=1)
  2. site/assets копируется в docs/assets  — css, js, картинки
  3. data/content.json копируется в docs/data — фото и акции
  4. загруженные через админку файлы (data/uploads) тоже копируются

Запуск:  python3 build_gh_pages.py
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")


def clean_docs():
    """docs/ каждый раз собирается с нуля — чтобы не осталось старых страниц."""
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(DOCS)


def run_builder():
    env = dict(os.environ, GH_PAGES="1")
    result = subprocess.run(
        [sys.executable, os.path.join(ROOT, "build_pages.py")],
        cwd=ROOT, env=env, capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit("build_pages.py упал с кодом %d" % result.returncode)
    print(result.stdout.strip())


def copy_tree(src, dst, label):
    if not os.path.isdir(src):
        print("  · %s — нет, пропуск" % label)
        return 0
    shutil.copytree(src, dst, dirs_exist_ok=True)
    n = sum(len(files) for _, _, files in os.walk(dst))
    print("  · %s → %d файл(ов)" % (label, n))
    return n


def patch_content_url():
    """В docs/ данные лежат рядом (docs/data), а не уровнем выше.

    site/assets/js/main.js ищет '../data/content.json' — на GitHub Pages
    такой путь уходит за корень публикации и даёт 404. Ставим прямой путь,
    чтобы не тратить лишний запрос. Оригинал в site/ не трогаем.
    """
    path = os.path.join(DOCS, "assets", "js", "main.js")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        js = f.read()
    js = js.replace("contentUrl: '../data/content.json'", "contentUrl: 'data/content.json'")
    with open(path, "w", encoding="utf-8") as f:
        f.write(js)
    print("  · contentUrl → data/content.json (рядом с html)")


def main():
    print("Сборка для GitHub Pages")
    clean_docs()
    run_builder()

    copy_tree(os.path.join(SITE, "assets"), os.path.join(DOCS, "assets"), "site/assets")
    patch_content_url()

    content = os.path.join(DATA, "content.json")
    if os.path.isfile(content):
        os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)
        shutil.copy2(content, os.path.join(DOCS, "data", "content.json"))
        print("  · data/content.json → docs/data/")
    else:
        print("  ! data/content.json не найден — сайт покажет резервные фото")

    copy_tree(os.path.join(DATA, "uploads"), os.path.join(DOCS, "data", "uploads"), "data/uploads")

    # GitHub Pages не умеет сам обрабатывать 404 для проекта по подпути,
    # но 404.html в корне публикации он использует как страницу ошибки.
    not_found = os.path.join(DOCS, "404.html")
    if os.path.isfile(not_found):
        print("  · 404.html на месте")

    # .nojekyll: без него Jekyll игнорирует файлы и папки с подчёркиванием
    with open(os.path.join(DOCS, ".nojekyll"), "w", encoding="utf-8") as f:
        f.write("")

    files = sum(len(f) for _, _, f in os.walk(DOCS))
    print("\nГотово: docs/ — %d файлов" % files)
    print("Опубликовать: Settings → Pages → Source: Deploy from a branch → main / docs")


if __name__ == "__main__":
    main()
