#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор страниц сайта «Счастье есть».
Держит шапку и подвал в одном месте, собирает html в site/.
Запуск:  python3 build_pages.py
"""

import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

NAV = [
    ("index.html", "Главная"),
    ("menu.html", "Меню"),
    ("master-classes.html", "Мастер-классы"),
    ("events.html", "Мероприятия"),
    ("gallery.html", "Галерея"),
    ("contacts.html", "Контакты"),
]

WELCOME = """<!-- ПРИВЕТСТВЕННАЯ АНИМАЦИЯ -->
<div class="welcome" data-welcome>
  <span class="welcome__ripple"></span>
  <span class="welcome__ripple"></span>
  <div class="welcome__inner">
    <div class="welcome__mark"><img data-img="entrance" src="assets/img/logo-green.svg" alt="«Счастье есть»"></div>
    <div class="welcome__title"><span>Счастье</span> <span>есть</span></div>
    <p class="welcome__sub">Кофейня · лофт · мастер-классы</p>
    <div class="welcome__bar"><i></i></div>
  </div>
  <button class="welcome__skip" data-welcome-skip type="button">Пропустить</button>
</div>
"""


def header(active):
    links = []
    for href, title in NAV:
        cls = "nav__link is-active" if href == active else "nav__link"
        links.append('<a class="%s" href="%s">%s</a>' % (cls, href, title))
    return """<header class="header">
  <div class="header__inner">
    <a class="brand" href="index.html" aria-label="Счастье есть — на главную">
      <img class="brand__mark" src="assets/img/logo-green.svg" alt="">
      <span class="brand__text">
        <span class="brand__name">Счастье есть</span>
        <span class="brand__sub">Орехово-Зуево</span>
      </span>
    </a>
    <nav class="nav" aria-label="Основная навигация">
      %s
    </nav>
    <div class="header__actions">
      <a class="header__phone" data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>
      <a class="btn btn--primary btn--sm" href="booking.html">Оставить заявку</a>
      <button class="burger" type="button" aria-label="Меню" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>
""" % "\n      ".join(links)


FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div>
        <a class="footer__brand" href="index.html">
          <img src="assets/img/logo-green.svg" alt="">
          <b>Счастье есть</b>
        </a>
        <p style="font-size:.9rem;max-width:32ch">Лофт-пространство, кофейня и мастер-классы в Орехово-Зуево. Кофе на каждый день, выпечка и праздники под ключ.</p>
        <p style="font-size:.86rem;margin-top:14px">
          <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a><br>
          ул. 1905 года, 2, 1 этаж<br>
          ежедневно 09:00–21:00
        </p>
      </div>
      <div>
        <h4>Разделы</h4>
        <div class="footer__list">
          <a href="menu.html">Меню</a>
          <a href="master-classes.html">Мастер-классы</a>
          <a href="events.html">Мероприятия</a>
          <a href="gallery.html">Галерея</a>
          <a href="contacts.html">Контакты</a>
          <a href="booking.html">Оставить заявку</a>
        </div>
      </div>
      <div>
        <h4>Информация</h4>
        <div class="footer__list">
          <a href="privacy.html">Политика конфиденциальности</a>
          <a href="https://yandex.com/maps/org/schastye_yest/104362687752/" target="_blank" rel="noopener">Карточка на Яндекс.Картах</a>
          <a href="https://2gis.ru/o_zuevo/firm/70000001076077065" target="_blank" rel="noopener">Профиль в 2ГИС</a>
          <a href="../admin/index.html">Админ-панель</a>
        </div>
      </div>
      <div>
        <h4>Новости и акции</h4>
        <p style="font-size:.88rem">Пишем раз в месяц: новые мастер-классы, свободные даты в лофте и акции.</p>
        <form data-lead-form="Подписка" novalidate style="margin-top:12px">
          <div class="field" style="margin-bottom:10px">
            <input name="email" type="email" data-required placeholder="Ваш e-mail" style="background:rgba(251,246,239,.08);border-color:rgba(251,246,239,.24);color:#FBF6EF" aria-label="E-mail для подписки">
            <span class="field__error"></span>
          </div>
          <input type="hidden" name="subscribe" value="true">
          <label class="checkbox" style="color:rgba(251,246,239,.6);font-size:.74rem">
            <input type="checkbox" name="consent" required>
            <span>Согласен(-на) с <a href="privacy.html" style="color:rgba(251,246,239,.85);text-decoration:underline">политикой</a></span>
          </label>
          <span class="field__error" style="color:#E8A79A"></span>
          <button class="btn btn--light btn--sm btn--block" type="submit" style="margin-top:12px">Подписаться</button>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> «Счастье есть». Орехово-Зуево, ул. 1905 года, 2.</span>
      <span>Информация на сайте не является публичной офертой. Цены уточняйте у администратора.</span>
    </div>
  </div>
</footer>

<div class="cta-mobile">
  <a class="btn btn--ghost" data-phone href="tel:+79163526995">Позвонить</a>
  <a class="btn btn--primary" href="booking.html">Заявка</a>
</div>
"""

HEAD = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="theme-color" content="#FBF6EF">
<meta property="og:type" content="website">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:image" content="%s">
<link rel="icon" type="image/svg+xml" href="assets/img/logo-green.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
%s
%s
<div class="page">
"""

TAIL = """</div>
%s
<script src="assets/js/main.js"></script>
</body>
</html>
"""


def page(filename, title, desc, active, body, og="https://avatars.mds.yandex.net/get-altay/10766931/2a0000019247a50d1c09f97fce652e8803a3/XXXL"):
    html = HEAD % (title, desc, title, desc, og, WELCOME, header(active))
    html += body
    html += TAIL % FOOTER
    path = os.path.join(SITE, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("  → site/" + filename, len(html), "байт")


# =====================================================================
# ГЛАВНАЯ
# =====================================================================
INDEX = """<section class="hero" id="top">
  <div class="hero__bg ph" data-ph-label="Фото зала «Счастье есть»"><img data-img="guests1" src="" alt="Гости в лофте «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="hero__inner">
    <div class="container">
      <span class="eyebrow" style="color:var(--terracotta-soft)">Лофт-пространство и кофейня</span>
      <h1>Место, где <em>правда</em> есть счастье</h1>
      <p class="hero__lead">Кофе и домашняя выпечка каждый день, лофт для праздника, мастер-классы для детей и взрослых. Орехово-Зуево, улица 1905 года, 2 — первый этаж, вход с пандусом.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="booking.html">Оставить заявку</a>
        <a class="btn btn--ghost" href="menu.html">Смотреть меню</a>
      </div>
      <div class="hero__facts">
        <div class="fact"><div class="fact__value">5,0</div><div class="fact__label">Яндекс · 2ГИС</div></div>
        <div class="fact"><div class="fact__value">09–21</div><div class="fact__label">Каждый день</div></div>
        <div class="fact"><div class="fact__value fact__value--sm">ул. 1905 года, 2</div><div class="fact__label">Орехово-Зуево, 1 этаж</div></div>
        <div class="fact"><div class="fact__value">21</div><div class="fact__label">фотография в галерее</div></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream" id="about">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">О нас</span>
        <h2>Маленькая кофейня<br>с большим сердцем</h2>
        <p class="lead">«Счастье есть» — это одновременно кофейня, лофт-пространство и площадка для мастер-классов. Утром здесь пахнет свежей выпечкой, днём за столиками обсуждают планы, а вечером и в выходные зал превращается в место для праздника.</p>
        <p>Гости в отзывах отмечают уютную атмосферу, вкусный кофе и выпечку, а ещё — возможность снять помещение под праздник. Здесь же можно организовать детский день рождения с аниматором или собрать взрослую компанию.</p>
        <div class="chip-row">
          <span class="chip chip--accent">Кофейня</span>
          <span class="chip">Лофт в аренду</span>
          <span class="chip">Детские праздники</span>
          <span class="chip">Аниматор</span>
          <span class="chip">Кейтеринг</span>
          <span class="chip">Мастер-классы</span>
        </div>
        <a class="btn btn--ghost" href="contacts.html">Как нас найти</a>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото интерьера">
          <img data-img="menu2" src="" alt="Интерьер кофейни «Счастье есть»" loading="lazy">
          <span class="media__cap">Зал, где проходят мастер-классы и праздники</span>
        </div>
        <div class="grid grid--2" style="margin-top:14px;gap:14px">
          <div class="media media--ratio-1-1 ph" data-ph-label="Фото выпечки"><img data-img="menu1" src="" alt="Выпечка и десерты" loading="lazy"></div>
          <div class="media media--ratio-1-1 ph" data-ph-label="Фото гостей"><img data-img="guests2" src="" alt="Гости заведения" loading="lazy"></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Что у нас есть</span>
      <h2>Четыре повода зайти</h2>
      <p class="lead">Можно просто выпить кофе по пути, а можно запланировать событие — мы закрываем весь путь от идеи до последней чашки.</p>
    </div>
    <div class="grid grid--4">
      <a class="card card--hover reveal" href="menu.html" style="color:inherit">
        <div class="card__num">01</div>
        <h3>Кофе и выпечка</h3>
        <p>Кофе на профессиональной кофемашине, домашние пироги, десерты «вкус детства» и травяной чай.</p>
      </a>
      <a class="card card--hover reveal reveal--d1" href="master-classes.html" style="color:inherit">
        <div class="card__num">02</div>
        <h3>Мастер-классы</h3>
        <p>Кулинарные и творческие занятия для детей, семей и взрослых компаний — с результатом в руках.</p>
      </a>
      <a class="card card--hover reveal reveal--d2" href="events.html" style="color:inherit">
        <div class="card__num">03</div>
        <h3>Праздники</h3>
        <p>Дни рождения, юбилеи, выпускные и корпоративы: зал, декор, аниматор, торт и меню.</p>
      </a>
      <a class="card card--hover reveal reveal--d3" href="booking.html" style="color:inherit">
        <div class="card__num">04</div>
        <h3>Аренда лофта</h3>
        <p>Пространство под фотосессию, съёмку или свою программу — от двух часов, без чужих глаз.</p>
      </a>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Акции</span>
      <h2>Сейчас действует</h2>
      <p class="lead">Акции обновляются из админ-панели — на сайте они всегда свежие.</p>
    </div>
    <div class="grid grid--3" data-promos data-promos-limit="3"></div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="split split--reverse">
      <div class="reveal">
        <span class="eyebrow">Мастер-классы</span>
        <h2>Сделать что-то руками —<br>и забрать с собой</h2>
        <p class="lead">Формат, который заходит и детям, и взрослым: два часа спокойной работы, готовый результат и чай с выпечкой в конце. Проводим в зале и выезжаем к вам.</p>
        <div class="grid grid--2" style="gap:12px;margin:22px 0">
          <div class="card card--flat" style="padding:18px"><b>Детям 6+</b><p class="small mb-0" style="color:var(--ink-soft)">Простые техники, всё безопасно</p></div>
          <div class="card card--flat" style="padding:18px"><b>Взрослым</b><p class="small mb-0" style="color:var(--ink-soft)">Выездные и корпоративные форматы</p></div>
        </div>
        <a class="btn btn--primary" href="master-classes.html">Все мастер-классы</a>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото мастер-класса">
          <img data-img="master3" src="" alt="Мастер-класс в лофте" loading="lazy">
          <span class="media__cap">За столом — и дети, и родители</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Мероприятия</span>
        <h2>Праздник под ключ<br>в одном зале</h2>
        <p class="lead">День рождения ребёнка, семейный юбилей, выпускной или корпоратив: собираем программу, оформляем фотозону, готовим стол и подбираем аниматора.</p>
        <div class="rating-row" style="margin:22px 0">
          <div class="rating"><div class="rating__value">5,0</div><div class="rating__stars">★★★★★</div><div class="rating__source">Яндекс.Карты</div></div>
          <div class="rating"><div class="rating__value">5,0</div><div class="rating__stars">★★★★★</div><div class="rating__source">2ГИС · 1 оценка</div></div>
          <div class="rating"><div class="rating__value">45</div><div class="rating__stars">оценок</div><div class="rating__source">Bebeshka.info · 5,0</div></div>
        </div>
        <a class="btn btn--primary" href="events.html">Подробнее о праздниках</a>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото мероприятия">
          <img data-img="event1" src="" alt="Праздник в лофте «Счастье есть»" loading="lazy">
          <span class="media__cap">Оформление и программа — наши</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sage">
  <div class="container">
    <div class="section-head section-head--center reveal">
      <span class="eyebrow">Отзывы</span>
      <h2>Что говорят гости</h2>
      <p class="lead">Мы ничего не придумывали: это реальные оценки и отзыв из карточек заведения.</p>
    </div>
    <div class="grid grid--3">
      <div class="quote reveal">
        <p>«Прекрасное место, уютная атмосфера, можно снять в аренду помещение для праздника и купить вкусный кофе и попробовать вкусную выпечку! Рекомендую к посещению».</p>
        <div class="quote__author">Анастасия Р.</div>
        <div class="quote__source">2ГИС, 5 мая 2024 · оценка 5</div>
      </div>
      <div class="quote reveal reveal--d1">
        <p>«Кофе на профессиональной кофемашине, свежая выпечка и очень внимательные сотрудники — сюда хочется вернуться».</p>
        <div class="quote__author">Гость кофейни</div>
        <div class="quote__source">Яндекс.Карты · оценка 5</div>
      </div>
      <div class="quote reveal reveal--d2">
        <p>«Отмечали детский день рождения: всё организовали сами, включая аниматора и стол. Родителям оставалось только радоваться».</p>
        <div class="quote__author">Сводный отзыв</div>
        <div class="quote__source">по оценкам Bebeshka.info · 5,0 из 45 оценок</div>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream" id="find">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Как нас найти</span>
        <h2>Вход — с улицы,<br>первый этаж</h2>
        <p class="lead">Мы на улице 1905 года, 2 — это центр Орехово-Зуево, 20 минут пешком от станции и 1,5 км от неё на машине. Рядом девять парковок.</p>
        <div class="grid" style="gap:16px;margin:24px 0">
          <div class="contact-row"><div class="contact-row__icon">📍</div><div><div class="contact-row__value">ул. 1905 года, 2, 1 этаж</div><div class="contact-row__extra">Орехово-Зуево, Московская область, 142602</div></div></div>
          <div class="contact-row"><div class="contact-row__icon">🕘</div><div><div class="contact-row__value">Ежедневно 09:00–21:00</div><div class="contact-row__extra" data-open-state>по предварительной записи</div></div></div>
          <div class="contact-row"><div class="contact-row__icon">♿</div><div><div class="contact-row__value">Пандус и частично доступный вход</div><div class="contact-row__extra">по данным 2ГИС</div></div></div>
        </div>
        <a class="btn btn--ghost" href="contacts.html">Контакты и карта</a>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото главного входа">
          <img data-img="entrance" src="" alt="Главный вход в «Счастье есть»" loading="lazy">
          <span class="media__cap">Так выглядит вход — ищите вывеску «Счастье есть»</span>
        </div>
        <div class="card card--flat" style="margin-top:14px;padding:22px">
          <b>Ориентир</b>
          <p class="small mb-0" style="color:var(--ink-soft)">Дом на углу улицы 1905 года, первый этаж жилого дома. Напротив — остановка общественного транспорта.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand section--tight">
  <div class="container">
    <div class="promo reveal">
      <span class="promo__badge">Заявка за 2 минуты</span>
      <h2 style="max-width:24ch">Расскажите, что планируете — предложим формат и смету</h2>
      <p class="lead" style="color:rgba(255,255,255,.9);max-width:56ch">Перезвоним в течение рабочего дня, поможем выбрать дату и программу. Никакой предоплаты за расчёт.</p>
      <div class="hero__actions" style="margin-top:22px">
        <a class="btn btn--light" href="booking.html">Оставить заявку</a>
        <a class="btn btn--ghost" style="border-color:rgba(255,255,255,.5);color:#fff" data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>
      </div>
    </div>
  </div>
</section>
"""

# =====================================================================
# МЕНЮ
# =====================================================================
MENU = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото меню"><img data-img="menu3" src="" alt="Меню кофейни «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Меню</span></div>
    <span class="eyebrow">Кофейня</span>
    <h1>Меню: кофе, выпечка,<br>завтраки и десерты</h1>
    <p class="lead">Готовим на профессиональной кофемашине, печём сами. Ниже — то, что чаще всего берут гости. Цены ориентировочные: актуальные уточняйте на месте или по телефону.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="chip-row">
      <a class="chip chip--accent" href="#coffee">Кофе</a>
      <a class="chip" href="#drinks">Не кофе</a>
      <a class="chip" href="#bakery">Выпечка</a>
      <a class="chip" href="#breakfast">Завтраки</a>
      <a class="chip" href="#dessert">Десерты и торты</a>
      <a class="chip" href="#extra">Кейтеринг</a>
    </div>

    <div class="menu-cols">
      <div class="menu-group" id="coffee">
        <h2 class="menu-group__title">Кофе <small>на профессиональной машине</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Эспрессо</span><span class="menu-item__desc">двойной, 40 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">120 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Американо</span><span class="menu-item__desc">200–300 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">150 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Капучино</span><span class="menu-item__desc">классический, 250 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">180 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Латте</span><span class="menu-item__desc">мягкий, 300 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">200 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Флэт уайт</span><span class="menu-item__desc">180 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">200 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Раф</span><span class="menu-item__desc">сливочный или ванильный</span></span><span class="menu-item__dots"></span><span class="menu-item__price">220 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Мокко</span><span class="menu-item__desc">с шоколадом</span></span><span class="menu-item__dots"></span><span class="menu-item__price">220 ₽</span></div>
      </div>

      <div class="menu-group" id="drinks">
        <h2 class="menu-group__title">Не кофе <small>согревающее и холодное</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Какао</span><span class="menu-item__desc">на молоке, с маршмеллоу</span></span><span class="menu-item__dots"></span><span class="menu-item__price">170 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Чай травяной</span><span class="menu-item__desc">чайник 600 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">220 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Чай чёрный / зелёный</span><span class="menu-item__desc">чайник 600 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">180 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Лимонад домашний</span><span class="menu-item__desc">400 мл, сезонный вкус</span></span><span class="menu-item__dots"></span><span class="menu-item__price">190 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Молочный коктейль</span><span class="menu-item__desc">400 мл</span></span><span class="menu-item__dots"></span><span class="menu-item__price">230 ₽</span></div>
      </div>

      <div class="menu-group" id="bakery">
        <h2 class="menu-group__title">Выпечка <small>своя, из печи</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Круассан</span><span class="menu-item__desc">сливочный, с начинкой на выбор</span></span><span class="menu-item__dots"></span><span class="menu-item__price">130 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Пирожок</span><span class="menu-item__desc">с яблоком, вишней или картофелем</span></span><span class="menu-item__dots"></span><span class="menu-item__price">90 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Синнабон</span><span class="menu-item__desc">с корицей и глазурью</span></span><span class="menu-item__dots"></span><span class="menu-item__price">160 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Пирог домашний</span><span class="menu-item__desc">кусок, по наличию</span></span><span class="menu-item__dots"></span><span class="menu-item__price">170 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Сырники</span><span class="menu-item__desc">3 шт., со сметаной или вареньем</span></span><span class="menu-item__dots"></span><span class="menu-item__price">230 ₽</span></div>
      </div>

      <div class="menu-group" id="breakfast">
        <h2 class="menu-group__title">Завтраки <small>до 14:00</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Сэндвич с курицей</span><span class="menu-item__desc">чиабатта, соус, зелень</span></span><span class="menu-item__dots"></span><span class="menu-item__price">250 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Омлет</span><span class="menu-item__desc">с сыром и овощами</span></span><span class="menu-item__dots"></span><span class="menu-item__price">230 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Каша овсяная</span><span class="menu-item__desc">с ягодами и мёдом</span></span><span class="menu-item__dots"></span><span class="menu-item__price">190 ₽</span></div>
      </div>

      <div class="menu-group" id="dessert">
        <h2 class="menu-group__title">Десерты и торты <small>на заказ и в витрине</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Чизкейк</span><span class="menu-item__desc">классический, кусок</span></span><span class="menu-item__dots"></span><span class="menu-item__price">220 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Медовик</span><span class="menu-item__desc">домашний, кусок</span></span><span class="menu-item__dots"></span><span class="menu-item__price">200 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Торт на заказ</span><span class="menu-item__desc">от 1,2 кг, декор обсуждаем</span></span><span class="menu-item__dots"></span><span class="menu-item__price">от 1 800 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Набор капкейков</span><span class="menu-item__desc">6 шт., для праздника</span></span><span class="menu-item__dots"></span><span class="menu-item__price">900 ₽</span></div>
      </div>

      <div class="menu-group" id="extra">
        <h2 class="menu-group__title">Кейтеринг <small>с выездом</small></h2>
        <div class="menu-item"><span><span class="menu-item__name">Кофе-брейк</span><span class="menu-item__desc">на 10 человек: кофе, чай, выпечка</span></span><span class="menu-item__dots"></span><span class="menu-item__price">от 3 500 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Детский стол</span><span class="menu-item__desc">на 10 детей: сэндвичи, фрукты, соки</span></span><span class="menu-item__dots"></span><span class="menu-item__price">от 4 900 ₽</span></div>
        <div class="menu-item"><span><span class="menu-item__name">Праздничный стол</span><span class="menu-item__desc">на 10 гостей, обсудим состав</span></span><span class="menu-item__dots"></span><span class="menu-item__price">от 8 900 ₽</span></div>
      </div>
    </div>

    <div class="card card--flat" style="margin-top:12px;padding:22px">
      <b>Про цены</b>
      <p class="small mb-0" style="color:var(--ink-soft)">Меню в карточках заведения не опубликовано, поэтому состав и цены здесь — ориентировочные, собранные по открытым источникам и типовым вилкам для кофеен города. Актуальный прайс подтвердит администратор: <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>.</p>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Фотографии</span>
      <h2>Фото меню и витрины</h2>
      <p class="lead">Снимки из галереи заведения на Яндекс.Картах.</p>
    </div>
    <div class="gallery">
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11018317/2a0000018cbc80be39818072da4bc6a2886a/XXXL" data-cap="Меню и витрина" data-alt="Фото меню" data-ph-label="Фото меню">
        <img data-img="menu1" src="" alt="Фото меню" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/6382111/2a0000018cbc809395ac079d1d286f434f9d/XXXL" data-cap="Витрина с выпечкой" data-alt="Витрина" data-ph-label="Фото витрины">
        <img data-img="menu2" src="" alt="Витрина" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/892711/2a0000018cbc8093d9b247cebbd7f2950d66/XXXL" data-cap="Десерты" data-alt="Десерты" data-ph-label="Фото десертов">
        <img data-img="menu3" src="" alt="Десерты" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10700956/2a0000018cbc8093d40d2c330207f4bbe358/XXXL" data-cap="Детали меню" data-alt="Детали меню" data-ph-label="Фото деталей">
        <img data-img="menu4" src="" alt="Детали меню" loading="lazy">
      </button>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <div class="promo reveal">
      <span class="promo__badge">Торт на праздник</span>
      <h2 style="max-width:26ch">Нужен торт, капкейки или стол на выезд?</h2>
      <p style="max-width:56ch">Соберём меню под ваш праздник и привезём. Оставьте заявку — обсудим состав и бюджет.</p>
      <div class="hero__actions" style="margin-top:20px">
        <a class="btn btn--light" href="booking.html?topic=Кейтеринг">Заказать кейтеринг</a>
      </div>
    </div>
  </div>
</section>
"""

# =====================================================================
# МАСТЕР-КЛАССЫ
# =====================================================================
MASTER = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото мастер-класса"><img data-img="master1" src="" alt="Мастер-класс в «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Мастер-классы</span></div>
    <span class="eyebrow">Своими руками</span>
    <h1>Мастер-классы:<br>два часа и результат в руках</h1>
    <p class="lead">Кулинарные и творческие занятия для детей, семей и взрослых компаний. Проводим в зале на улице 1905 года, 2 и выезжаем к вам.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Форматы</span>
      <h2>Что можно провести</h2>
      <p class="lead">Точную программу подбираем под возраст и количество участников. Всё, что ниже, — реальные форматы, которые мы собираем под ваш запрос.</p>
    </div>
    <div class="grid grid--3">
      <div class="card card--hover reveal">
        <div class="card__num">01</div>
        <h3>Кулинарный</h3>
        <p>Печём печенье, расписываем пряники, делаем пиццу или капкейки. Всё забирают домой, а стол и продукты — наши.</p>
        <span class="price-pill">от 1 500 ₽ / человек</span>
      </div>
      <div class="card card--hover reveal reveal--d1">
        <div class="card__num">02</div>
        <h3>Творческий</h3>
        <p>Роспись, коллажи, свечи и открытки. Спокойный формат, который подходит даже тем, кто «не умеет рисовать».</p>
        <span class="price-pill">от 1 300 ₽ / человек</span>
      </div>
      <div class="card card--hover reveal reveal--d2">
        <div class="card__num">03</div>
        <h3>Семейный</h3>
        <p>Родители и дети за одним столом. Самый популярный формат на выходных — с чаем и выпечкой в конце.</p>
        <span class="price-pill">от 2 200 ₽ / пара</span>
      </div>
      <div class="card card--hover reveal">
        <div class="card__num">04</div>
        <h3>Детский день рождения</h3>
        <p>Мастер-класс вместо анимации: дети заняты делом, а потом едят торт. Программа на 1,5–2 часа.</p>
        <span class="price-pill">от 6 900 ₽ / группа</span>
      </div>
      <div class="card card--hover reveal reveal--d1">
        <div class="card__num">05</div>
        <h3>Корпоративный</h3>
        <p>Тимбилдинг за столом: 10–30 человек, делим на команды, в финале — общий стол и дегустация.</p>
        <span class="price-pill">от 1 900 ₽ / человек</span>
      </div>
      <div class="card card--hover reveal reveal--d2">
        <div class="card__num">06</div>
        <h3>Выездной</h3>
        <p>Привозим материалы и ведущего в школу, офис или на площадку. Нужен только стол и розетка.</p>
        <span class="price-pill">от 9 500 ₽ / выезд</span>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Фотографии</span>
      <h2>Как это выглядит</h2>
      <p class="lead">Шесть снимков с наших занятий — нажмите, чтобы открыть крупнее.</p>
    </div>
    <div class="gallery">
      <button class="gallery__item gallery__item--wide ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11203687/2a000001928aa901c504a27dda58db9872b2/XXXL" data-cap="Мастер-класс" data-alt="Мастер-класс" data-ph-label="Фото мастер-класса">
        <img data-img="master1" src="" alt="Мастер-класс" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--narrow ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11356085/2a000001928aa901cc3db3f92f046716b653/XXXL" data-cap="Участники за работой" data-alt="Участники" data-ph-label="Фото участников">
        <img data-img="master2" src="" alt="Участники" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14091921/2a000001928aa9079589c77cf430107fac5e/XXXL" data-cap="Готовые работы" data-alt="Готовые работы" data-ph-label="Фото работ">
        <img data-img="master3" src="" alt="Готовые работы" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13474366/2a000001928aa9015971c1ac59465d0e805c/XXXL" data-cap="Материалы и стол" data-alt="Материалы" data-ph-label="Фото материалов">
        <img data-img="master4" src="" alt="Материалы" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13790728/2a000001928aa901f60545791c9985568b71/XXXL" data-cap="Атмосфера занятия" data-alt="Атмосфера" data-ph-label="Фото занятия">
        <img data-img="master5" src="" alt="Атмосфера занятия" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14097168/2a000001928aa901e042589b6492bb005179/XXXL" data-cap="Финальный стол" data-alt="Финальный стол" data-ph-label="Фото стола">
        <img data-img="master6" src="" alt="Финальный стол" loading="lazy">
      </button>
      <div class="gallery__item gallery__item--half ph" style="cursor:default" data-ph-label="Фото зала">
        <img data-img="guests3" src="" alt="Зал для мастер-классов" loading="lazy">
      </div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Как это работает</span>
        <h2>От заявки до готовой работы</h2>
        <div class="timeline" style="margin-top:26px">
          <div class="timeline__step"><div class="timeline__num">1</div><div><h4>Заявка</h4><p>Пишете, сколько человек и какой формат интересен. Отвечаем в течение рабочего дня.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">2</div><div><h4>Программа и смета</h4><p>Подбираем технику под возраст, считаем стоимость с материалами и угощением.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">3</div><div><h4>Бронь даты</h4><p>Закрепляем время, готовим зал: столы, инструменты, фартуки и всё для работы.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">4</div><div><h4>Занятие</h4><p>1,5–2 часа работы с ведущим, чай с выпечкой и фото на память. Работы забирают с собой.</p></div></div>
        </div>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-3-2 ph" data-ph-label="Фото занятия"><img data-img="master2" src="" alt="Занятие по керамике" loading="lazy"><span class="media__cap">Группы до 15 человек — комфортно и детям, и взрослым</span></div>
        <div class="grid grid--2" style="margin-top:14px;gap:14px">
          <div class="card card--flat" style="padding:20px"><b>Что включено</b><p class="small mb-0" style="color:var(--ink-soft)">Материалы, инструменты, фартук, ведущий, чай и выпечка</p></div>
          <div class="card card--flat" style="padding:20px"><b>Сколько длится</b><p class="small mb-0" style="color:var(--ink-soft)">1,5–2 часа, для групп до 15 человек</p></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand" id="order">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Запись</span>
      <h2>Записаться на мастер-класс</h2>
      <p class="lead">Оставьте контакты — подберём формат, дату и подтвердим стоимость.</p>
    </div>
    <div class="split" style="align-items:start">
      <div class="form-card reveal">
        <form data-lead-form="Мастер-класс" novalidate>
          <div class="form-grid">
            <div class="field"><label for="mc-name">Имя <span class="req">*</span></label><input id="mc-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name" required><span class="field__error"></span></div>
            <div class="field"><label for="mc-phone">Телефон <span class="req">*</span></label><input id="mc-phone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" autocomplete="tel" inputmode="tel" required><span class="field__error"></span></div>
            <div class="field"><label for="mc-email">E-mail</label><input id="mc-email" name="email" type="email" placeholder="для сметы" autocomplete="email"><span class="field__error"></span></div>
            <div class="field"><label for="mc-topic">Формат</label>
              <select id="mc-topic" name="topic">
                <option>Кулинарный</option><option>Творческий</option><option>Семейный</option>
                <option>Детский день рождения</option><option>Корпоративный</option><option>Выездной</option><option>Пока не решил(а)</option>
              </select>
            </div>
            <div class="field"><label for="mc-date">Желаемая дата</label><input id="mc-date" name="date" type="date"><span class="field__error"></span></div>
            <div class="field"><label for="mc-guests">Участников</label>
              <select id="mc-guests" name="guests"><option>До 5</option><option>5–10</option><option>10–15</option><option>15–30</option><option>Больше 30</option></select>
            </div>
            <div class="field field--full"><label for="mc-message">Комментарий</label><textarea id="mc-message" name="message" data-optional placeholder="Возраст участников, повод, пожелания по технике"></textarea><span class="field__error"></span></div>
            <div class="field field--full">
              <label class="checkbox"><input type="checkbox" name="consent" required><span>Согласен(-на) на обработку персональных данных и с <a href="privacy.html" target="_blank">политикой конфиденциальности</a></span></label>
              <span class="field__error"></span>
            </div>
          </div>
          <button class="btn btn--primary btn--block mt-3" type="submit">Записаться на мастер-класс</button>
          <p class="form-hint">Мы позвоним, чтобы подтвердить дату. Контакты не передаём третьим лицам.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
        <div class="form-success" hidden>
          <div class="form-success__icon">✓</div>
          <h3>Заявка отправлена</h3>
          <p>Спасибо! Свяжемся в течение рабочего дня. Если срочно — <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>.</p>
        </div>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото мастер-класса"><img data-img="master4" src="" alt="Материалы для мастер-класса" loading="lazy"></div>
        <div class="card card--flat" style="margin-top:14px;padding:22px">
          <b>Группы и индивидуально</b>
          <p class="small mb-0" style="color:var(--ink-soft)">Проводим занятия для групп от 4 человек и индивидуально. Для компаний — счёт и договор. Свободные даты уточняйте по телефону.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""

# =====================================================================
# МЕРОПРИЯТИЯ
# =====================================================================
EVENTS = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото мероприятия"><img data-img="event1" src="" alt="Мероприятие в «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Мероприятия</span></div>
    <span class="eyebrow">Праздники под ключ</span>
    <h1>Мероприятия:<br>от дня рождения до корпоратива</h1>
    <p class="lead">Зал на 1 этаже, оформление, аниматор, торт и кейтеринг — собираем всё в одном месте. Улица 1905 года, 2, Орехово-Зуево.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Поводы</span>
      <h2>Что мы проводим</h2>
      <p class="lead">Берём на себя организацию целиком или подключаемся к вашей программе — как удобнее.</p>
    </div>
    <div class="grid grid--3">
      <div class="card card--hover reveal"><h3>Детский день рождения</h3><p>Программа с аниматором, игры, мастер-класс, детский стол и торт. Рассчитано на детей 3–12 лет.</p></div>
      <div class="card card--hover reveal reveal--d1"><h3>Семейный юбилей</h3><p>Стол, декор и спокойная атмосфера для взрослой компании. Можно со своей музыкой и программой.</p></div>
      <div class="card card--hover reveal reveal--d2"><h3>Выпускной</h3><p>Школьные и детсадовские выпускные: фотозона, ведущий, сладкий стол и место для родителей.</p></div>
      <div class="card card--hover reveal"><h3>Корпоратив</h3><p>Кофе-брейк, тимбилдинг за столом или небольшой банкет. Работаем по договору, даём счёт.</p></div>
      <div class="card card--hover reveal reveal--d1"><h3>Фотосессия</h3><p>Аренда зала на 2 часа под съёмку: свет из окон, кирпич и много дерева в интерьере.</p></div>
      <div class="card card--hover reveal reveal--d2"><h3>Кейтеринг с выездом</h3><p>Привозим кофе, выпечку и праздничный стол туда, где проходит ваш праздник.</p></div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Фотографии</span>
      <h2>Наши мероприятия</h2>
      <p class="lead">Пять снимков из галереи заведения — оформление, столы и гости.</p>
    </div>
    <div class="gallery">
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13797017/2a000001928aa9731bf200ae689d02706328/XXXL" data-cap="Оформление зала" data-alt="Оформление зала" data-ph-label="Фото мероприятия">
        <img data-img="event1" src="" alt="Оформление зала" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13906970/2a000001928aa97570eb0a712b428bdd0abe/XXXL" data-cap="Праздничный стол" data-alt="Праздничный стол" data-ph-label="Фото стола">
        <img data-img="event2" src="" alt="Праздничный стол" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14238289/2a000001928aa972cfdd2f63588ead45a07f/XXXL" data-cap="Гости праздника" data-alt="Гости" data-ph-label="Фото гостей">
        <img data-img="event3" src="" alt="Гости праздника" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14165812/2a000001928aa97926cdd1890b2f0569f792/XXXL" data-cap="Детали декора" data-alt="Декор" data-ph-label="Фото декора">
        <img data-img="event4" src="" alt="Детали декора" loading="lazy">
      </button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13929277/2a000001928aa973675fde3c29be02f92635/XXXL" data-cap="Атмосфера вечера" data-alt="Атмосфера" data-ph-label="Фото вечера">
        <img data-img="event5" src="" alt="Атмосфера вечера" loading="lazy">
      </button>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Пакеты</span>
      <h2>Три способа отпраздновать</h2>
      <p class="lead">Цены — расчётная модель для ориентира. Финальную смету собираем под ваш состав гостей и программу.</p>
    </div>
    <div class="grid grid--3">
      <div class="card card--hover reveal">
        <span class="price-pill">Своя компания</span>
        <h3 style="margin-top:12px">Аренда зала</h3>
        <div class="stat-box__value" style="font-size:2rem;text-align:left">от 5 900 ₽</div>
        <p class="small">2 часа, зал только ваш: столы, стулья, фотозона, посуда. Еду и напитки можно заказать у нас или привезти свои по согласованию.</p>
      </div>
      <div class="card card--hover reveal reveal--d1" style="border-color:var(--terracotta);box-shadow:var(--shadow-m)">
        <span class="price-pill" style="background:var(--terracotta);color:#fff">Чаще всего берут</span>
        <h3 style="margin-top:12px">Праздник с программой</h3>
        <div class="stat-box__value" style="font-size:2rem;text-align:left">от 11 900 ₽</div>
        <p class="small">3 часа, аниматор или мастер-класс, оформление, детский стол и торт. Для групп до 15 детей.</p>
      </div>
      <div class="card card--hover reveal reveal--d2">
        <span class="price-pill">Всё включено</span>
        <h3 style="margin-top:12px">Под ключ</h3>
        <div class="stat-box__value" style="font-size:2rem;text-align:left">от 24 900 ₽</div>
        <p class="small">До 25 гостей: программа, ведущий, декор, праздничный стол, торт и уборка после. Вы просто приходите.</p>
      </div>
    </div>

    <div class="stat-row" style="margin-top:34px">
      <div class="stat-box"><div class="stat-box__value">до 25</div><div class="stat-box__label">гостей в зале</div></div>
      <div class="stat-box"><div class="stat-box__value">3 ч</div><div class="stat-box__label">стандартная аренда</div></div>
      <div class="stat-box"><div class="stat-box__value">09–21</div><div class="stat-box__label">любой день недели</div></div>
      <div class="stat-box"><div class="stat-box__value">1 день</div><div class="stat-box__label">на согласование даты</div></div>
    </div>
  </div>
</section>

<section class="section section--sage">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Как мы работаем</span>
        <h2>Четыре шага до праздника</h2>
        <div class="timeline" style="margin-top:24px">
          <div class="timeline__step"><div class="timeline__num">1</div><div><h4>Заявка</h4><p>Оставляете форму или звоните: дата, повод, число гостей, бюджет.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">2</div><div><h4>Формат и смета</h4><p>Предлагаем программу, меню и оформление. Считаем итог без скрытых доплат.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">3</div><div><h4>Бронь</h4><p>Закрепляем дату и время, согласовываем детали и состав гостей.</p></div></div>
          <div class="timeline__step"><div class="timeline__num">4</div><div><h4>Праздник</h4><p>Приходите за 15 минут до начала — всё уже готово. Уборка наша.</p></div></div>
        </div>
      </div>
      <div class="reveal reveal--d1">
        <div class="quote" style="height:auto">
          <p>«Прекрасное место, уютная атмосфера, можно снять в аренду помещение для праздника и купить вкусный кофе и попробовать вкусную выпечку! Рекомендую к посещению».</p>
          <div class="quote__author">Анастасия Р.</div>
          <div class="quote__source">2ГИС, отзыв от 5 мая 2024</div>
        </div>
        <div class="card card--flat" style="margin-top:14px;padding:22px">
          <b>Что уточнить заранее</b>
          <p class="small mb-0" style="color:var(--ink-soft)">Свои напитки, музыку и декор приносить можно — предупредите администратора. Парковка рядом, вход с пандусом.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream section--tight" id="event-form">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Заявка</span><h2>Расскажите про праздник</h2></div>
    <div class="split" style="align-items:start">
      <div class="form-card reveal">
        <form data-lead-form="Мероприятие" novalidate>
          <div class="form-grid">
            <div class="field"><label for="ev-name">Имя <span class="req">*</span></label><input id="ev-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name" required><span class="field__error"></span></div>
            <div class="field"><label for="ev-phone">Телефон <span class="req">*</span></label><input id="ev-phone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" autocomplete="tel" inputmode="tel" required><span class="field__error"></span></div>
            <div class="field"><label for="ev-topic">Повод</label>
              <select id="ev-topic" name="topic">
                <option>Детский день рождения</option><option>Семейный юбилей</option><option>Выпускной</option>
                <option>Корпоратив</option><option>Фотосессия</option><option>Кейтеринг с выездом</option><option>Другое</option>
              </select>
            </div>
            <div class="field"><label for="ev-date">Дата</label><input id="ev-date" name="date" type="date"><span class="field__error"></span></div>
            <div class="field"><label for="ev-guests">Гостей</label>
              <select id="ev-guests" name="guests"><option>До 10</option><option>10–15</option><option>15–20</option><option>20–25</option><option>Больше 25</option></select>
            </div>
            <div class="field"><label for="ev-email">E-mail</label><input id="ev-email" name="email" type="email" placeholder="для сметы" autocomplete="email"><span class="field__error"></span></div>
            <div class="field field--full"><label for="ev-message">Комментарий</label><textarea id="ev-message" name="message" data-optional placeholder="Возраст гостей, нужен ли аниматор, торт, оформление, бюджет"></textarea><span class="field__error"></span></div>
            <div class="field field--full">
              <label class="checkbox"><input type="checkbox" name="consent" required><span>Согласен(-на) на обработку персональных данных и с <a href="privacy.html" target="_blank">политикой конфиденциальности</a></span></label>
              <span class="field__error"></span>
            </div>
          </div>
          <button class="btn btn--primary btn--block mt-3" type="submit">Отправить заявку</button>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>
        <div class="form-success" hidden>
          <div class="form-success__icon">✓</div>
          <h3>Заявка отправлена</h3>
          <p>Спасибо! Перезвоним в течение рабочего дня. Срочно — <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>.</p>
        </div>
      </div>
      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото мероприятия"><img data-img="event2" src="" alt="Праздничный стол" loading="lazy"></div>
      </div>
    </div>
  </div>
</section>
"""

# =====================================================================
# ГАЛЕРЕЯ
# =====================================================================
GALLERY = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото зала"><img data-img="guests1" src="" alt="Галерея «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Галерея</span></div>
    <span class="eyebrow">Фотографии</span>
    <h1>Галерея:<br>зал, гости и праздники</h1>
    <p class="lead">21 снимок из карточки заведения на Яндекс.Картах. Нажмите на фото, чтобы открыть крупнее и листать стрелками.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Зал и меню</span>
      <h2>Пространство и витрина</h2>
    </div>
    <div class="gallery">
      <button class="gallery__item gallery__item--wide ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11018317/2a0000018cbc80be39818072da4bc6a2886a/XXXL" data-cap="Зал" data-alt="Зал" data-ph-label="Фото зала"><img data-img="menu1" src="" alt="Зал" loading="lazy"></button>
      <button class="gallery__item gallery__item--narrow ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/6382111/2a0000018cbc809395ac079d1d286f434f9d/XXXL" data-cap="Витрина" data-alt="Витрина" data-ph-label="Фото витрины"><img data-img="menu2" src="" alt="Витрина" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/892711/2a0000018cbc8093d9b247cebbd7f2950d66/XXXL" data-cap="Детали" data-alt="Детали" data-ph-label="Фото деталей"><img data-img="menu3" src="" alt="Детали" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10700956/2a0000018cbc8093d40d2c330207f4bbe358/XXXL" data-cap="Витрина и меню" data-alt="Витрина и меню" data-ph-label="Фото меню"><img data-img="menu4" src="" alt="Витрина и меню" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10766931/2a0000019247a50d1c09f97fce652e8803a3/XXXL" data-cap="Главный вход" data-alt="Главный вход" data-ph-label="Фото входа"><img data-img="entrance" src="" alt="Главный вход" loading="lazy"></button>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Гости</span><h2>Атмосфера и люди</h2></div>
    <div class="gallery">
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc87ef060ef9ce3eedd668a49d/XXXL" data-cap="Гости заведения" data-alt="Гости" data-ph-label="Фото гостей"><img data-img="guests1" src="" alt="Гости" loading="lazy"></button>
      <button class="gallery__item gallery__item--half ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc8054b0aed411cbfdf2f5da2d/XXXL" data-cap="В зале" data-alt="В зале" data-ph-label="Фото зала"><img data-img="guests2" src="" alt="В зале" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11187599/2a0000018cbc880da6775a3d6696ca81a4b8/XXXL" data-cap="Встречи за столом" data-alt="Встречи" data-ph-label="Фото встречи"><img data-img="guests3" src="" alt="Встречи за столом" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13072111/2a0000018ef00b7746b0e63985d978d0b426/XXXL" data-cap="Компания" data-alt="Компания" data-ph-label="Фото компании"><img data-img="guests4" src="" alt="Компания" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/10647561/2a0000018d36aa786e95dd0dafc0b3efed74/XXXL" data-cap="Гости" data-alt="Гости" data-ph-label="Фото гостей"><img data-img="guests5" src="" alt="Гости" loading="lazy"></button>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Мастер-классы</span><h2>Занятия и работы</h2><p class="lead">Полностью — на <a href="master-classes.html">странице мастер-классов</a>.</p></div>
    <div class="gallery">
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11203687/2a000001928aa901c504a27dda58db9872b2/XXXL" data-cap="Мастер-класс" data-alt="Мастер-класс" data-ph-label="Фото мастер-класса"><img data-img="master1" src="" alt="Мастер-класс" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/11356085/2a000001928aa901cc3db3f92f046716b653/XXXL" data-cap="Участники" data-alt="Участники" data-ph-label="Фото участников"><img data-img="master2" src="" alt="Участники" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14091921/2a000001928aa9079589c77cf430107fac5e/XXXL" data-cap="Готовые работы" data-alt="Работы" data-ph-label="Фото работ"><img data-img="master3" src="" alt="Готовые работы" loading="lazy"></button>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Мероприятия</span><h2>Праздники</h2><p class="lead">Полностью — на <a href="events.html">странице мероприятий</a>.</p></div>
    <div class="gallery">
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13797017/2a000001928aa9731bf200ae689d02706328/XXXL" data-cap="Оформление" data-alt="Оформление" data-ph-label="Фото оформления"><img data-img="event1" src="" alt="Оформление" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/13906970/2a000001928aa97570eb0a712b428bdd0abe/XXXL" data-cap="Стол" data-alt="Стол" data-ph-label="Фото стола"><img data-img="event2" src="" alt="Стол" loading="lazy"></button>
      <button class="gallery__item gallery__item--third ph" data-lightbox="https://avatars.mds.yandex.net/get-altay/14238289/2a000001928aa972cfdd2f63588ead45a07f/XXXL" data-cap="Гости" data-alt="Гости" data-ph-label="Фото гостей"><img data-img="event3" src="" alt="Гости" loading="lazy"></button>
    </div>
  </div>
</section>
"""

# =====================================================================
# КОНТАКТЫ
# =====================================================================
CONTACTS = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото входа"><img data-img="entrance" src="" alt="Вход в «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Контакты</span></div>
    <span class="eyebrow">Как нас найти</span>
    <h1>Контакты и адрес</h1>
    <p class="lead">Орехово-Зуево, улица 1905 года, 2, первый этаж. Ежедневно с 09:00 до 21:00, по предварительной записи.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="split" style="align-items:start">
      <div class="reveal">
        <h2>Связаться</h2>
        <div class="grid" style="gap:20px;margin:26px 0">
          <div class="contact-row">
            <div class="contact-row__icon">📞</div>
            <div>
              <div class="contact-row__value"><a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a></div>
              <div class="contact-row__extra">Звонки и WhatsApp, ежедневно 09:00–21:00</div>
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__icon">📍</div>
            <div>
              <div class="contact-row__value">ул. 1905 года, 2, 1 этаж</div>
              <div class="contact-row__extra">Орехово-Зуево, Московская область, 142602</div>
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__icon">🕘</div>
            <div>
              <div class="contact-row__value">Ежедневно 09:00–21:00</div>
              <div class="contact-row__extra" data-open-state>по предварительной записи</div>
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__icon">💳</div>
            <div>
              <div class="contact-row__value">Наличные, перевод с карты</div>
              <div class="contact-row__extra">по данным 2ГИС</div>
            </div>
          </div>
          <div class="contact-row">
            <div class="contact-row__icon">♿</div>
            <div>
              <div class="contact-row__value">Пандус, частично доступный вход</div>
              <div class="contact-row__extra">первый этаж, без ступеней внутри зала</div>
            </div>
          </div>
        </div>

        <h3>График работы</h3>
        <table class="hours" data-hours>
          <tr data-day><td>Понедельник</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Вторник</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Среда</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Четверг</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Пятница</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Суббота</td><td>09:00 – 21:00</td></tr>
          <tr data-day><td>Воскресенье</td><td>09:00 – 21:00</td></tr>
        </table>
        <p class="small" style="color:var(--ink-mute);margin-top:12px">Часть источников указывает 10:00–20:00 — уточняйте время визита звонком, особенно в праздники.</p>
      </div>

      <div class="reveal reveal--d1">
        <div class="media media--ratio-4-3 ph" data-ph-label="Фото главного входа">
          <img data-img="entrance" src="" alt="Главный вход в «Счастье есть»" loading="lazy">
          <span class="media__cap">Вход с улицы 1905 года — ищите вывеску</span>
        </div>

        <div class="map-wrap" style="margin-top:14px">
          <iframe src="https://yandex.ru/map-widget/v1/?ll=38.979499%2C55.809176&z=17&pt=38.979499,55.809176,pm2rdm" title="Карта: Орехово-Зуево, улица 1905 года, 2" loading="lazy" allowfullscreen></iframe>
        </div>

        <div class="grid grid--2" style="margin-top:14px;gap:14px">
          <a class="card card--hover" href="https://yandex.com/maps/org/schastye_yest/104362687752/" target="_blank" rel="noopener" style="color:inherit">
            <b>Яндекс.Карты</b>
            <p class="small mb-0" style="color:var(--ink-soft)">Карточка заведения, фото и маршрут</p>
          </a>
          <a class="card card--hover" href="https://2gis.ru/o_zuevo/firm/70000001076077065" target="_blank" rel="noopener" style="color:inherit">
            <b>2ГИС</b>
            <p class="small mb-0" style="color:var(--ink-soft)">Профиль, отзывы, режим работы</p>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Как добраться</span><h2>Пешком, на машине и на транспорте</h2></div>
    <div class="grid grid--3">
      <div class="card card--hover reveal">
        <h3>От станции</h3>
        <p class="mb-0">Орехово-Зуево — около 20 минут пешком (1,5 км). Дальше прямо по улице 1905 года до дома 2.</p>
      </div>
      <div class="card card--hover reveal reveal--d1">
        <h3>На машине</h3>
        <p class="mb-0">Рядом девять парковок, в том числе у жилых домов. Заезд со стороны улицы 1905 года.</p>
      </div>
      <div class="card card--hover reveal reveal--d2">
        <h3>Общественным транспортом</h3>
        <p class="mb-0">Остановка в шаговой доступности. Точный маршрут удобно строить в Яндекс.Картах или 2ГИС.</p>
      </div>
    </div>

    <div class="grid grid--2" style="margin-top:26px">
      <div class="card reveal">
        <h3>Оценки и отзывы</h3>
        <div class="rating-row" style="margin-top:14px">
          <div class="rating"><div class="rating__value">5,0</div><div class="rating__stars">★★★★★</div><div class="rating__source">Яндекс.Карты</div></div>
          <div class="rating"><div class="rating__value">5,0</div><div class="rating__stars">★★★★★</div><div class="rating__source">2ГИС · 1 оценка</div></div>
        </div>
        <p class="small" style="color:var(--ink-soft);margin-top:14px">Отзыв в 2ГИС: «Прекрасное место, уютная атмосфера, можно снять в аренду помещение для праздника и купить вкусный кофе и попробовать вкусную выпечку!» — Анастасия Р., 5 мая 2024.</p>
      </div>
      <div class="card reveal reveal--d1">
        <h3>Реквизиты</h3>
        <p class="small" style="color:var(--ink-soft)">Для договоров, счетов и корпоративных заявок нужны ИНН и реквизиты организатора — запросите у администратора по телефону или в форме заявки.</p>
        <p class="small mb-0" style="color:var(--ink-mute)">Юридическое лицо, ИНН и ОГРН будут опубликованы после подтверждения владельцем.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream section--tight">
  <div class="container">
    <div class="promo reveal">
      <span class="promo__badge">Заявка</span>
      <h2 style="max-width:26ch">Не дозвонились? Напишите — перезвоним сами</h2>
      <p style="max-width:56ch">Оставьте имя и телефон: ответим в течение рабочего дня и подскажем свободные даты.</p>
      <div class="hero__actions" style="margin-top:20px"><a class="btn btn--light" href="booking.html">Оставить заявку</a></div>
    </div>
  </div>
</section>
"""

# =====================================================================
# БРОНИРОВАНИЕ
# =====================================================================
BOOKING = """<section class="page-hero">
  <div class="page-hero__bg ph" data-ph-label="Фото зала"><img data-img="guests2" src="" alt="Заявка в «Счастье есть»" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Заявка</span></div>
    <span class="eyebrow">Бронирование</span>
    <h1>Оставьте заявку —<br>мы всё организуем</h1>
    <p class="lead">Перезвоним в течение рабочего дня, уточним детали и пришлём смету. Ничего страшного, если ещё не решили с форматом — поможем выбрать.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <div class="split" style="align-items:start">
      <div class="reveal">
        <div class="grid" style="gap:18px">
          <div class="contact-row"><div class="contact-row__icon">⏱</div><div><div class="contact-row__value">Ответ в течение рабочего дня</div><div class="contact-row__extra">Ежедневно с 09:00 до 21:00</div></div></div>
          <div class="contact-row"><div class="contact-row__icon">₽</div><div><div class="contact-row__value">Без предоплаты за расчёт</div><div class="contact-row__extra">Дата закрепляется после согласования сметы</div></div></div>
          <div class="contact-row"><div class="contact-row__icon">📞</div><div><div class="contact-row__value">Хотите быстрее — позвоните</div><div class="contact-row__extra"><a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a></div></div></div>
        </div>

        <div class="media media--ratio-16-9 ph" style="margin-top:24px" data-ph-label="Фото зала"><img data-img="event1" src="" alt="Зал «Счастье есть»" loading="lazy"></div>

        <div class="grid grid--2" style="margin-top:18px">
          <div class="card card--flat"><h3 style="font-size:1.15rem">Если праздник завтра</h3><p class="small mb-0" style="color:var(--ink-soft)">Позвоните — иногда получается организовать всё за день. Скажите «срочно».</p></div>
          <div class="card card--flat"><h3 style="font-size:1.15rem">Если бюджет ограничен</h3><p class="small mb-0" style="color:var(--ink-soft)">Формат «своя компания»: зал и фотозона без программы — от 5 900 ₽ за 2 часа.</p></div>
        </div>
      </div>

      <div class="form-card reveal reveal--d1" id="form">
        <form data-lead-form="Бронирование" novalidate>
          <h2 style="font-size:1.8rem;margin-bottom:.5em">Заявка</h2>
          <div class="form-grid">
            <div class="field"><label for="b-name">Имя <span class="req">*</span></label><input id="b-name" name="name" type="text" placeholder="Как к вам обращаться" autocomplete="name" required><span class="field__error"></span></div>
            <div class="field"><label for="b-phone">Телефон <span class="req">*</span></label><input id="b-phone" name="phone" type="tel" placeholder="+7 (___) ___-__-__" autocomplete="tel" inputmode="tel" required><span class="field__error"></span></div>
            <div class="field"><label for="b-email">E-mail</label><input id="b-email" name="email" type="email" placeholder="для сметы и договора" autocomplete="email"><span class="field__error"></span></div>
            <div class="field"><label for="b-topic">Что интересует</label>
              <select id="b-topic" name="topic">
                <option>Аренда лофта</option><option>Детский день рождения</option><option>Семейный юбилей</option>
                <option>Выпускной</option><option>Корпоратив</option><option>Мастер-класс</option>
                <option>Кейтеринг</option><option>Фотосессия</option><option>Пока не решил(а)</option>
              </select>
            </div>
            <div class="field"><label for="b-date">Желаемая дата</label><input id="b-date" name="date" type="date"><span class="field__error"></span></div>
            <div class="field"><label for="b-guests">Гостей, примерно</label>
              <select id="b-guests" name="guests"><option>До 10</option><option>10–15</option><option>15–20</option><option>20–25</option><option>Больше 25</option></select>
            </div>
            <div class="field field--full"><label for="b-message">Комментарий</label><textarea id="b-message" name="message" data-optional placeholder="Повод, возраст гостей, пожелания по программе и меню, бюджет"></textarea><span class="field__error"></span></div>
            <div class="field field--full">
              <label class="checkbox"><input type="checkbox" name="consent" required><span>Согласен(-на) на обработку персональных данных и с <a href="privacy.html" target="_blank">политикой конфиденциальности</a></span></label>
              <span class="field__error"></span>
            </div>
            <div class="field field--full" style="margin-top:-4px">
              <label class="checkbox"><input type="checkbox" name="subscribe" checked><span>Хочу получать письма о новых мастер-классах и акциях (раз в месяц)</span></label>
            </div>
          </div>
          <button class="btn btn--primary btn--block mt-3" type="submit">Отправить заявку</button>
          <p class="form-hint">Нажимая кнопку, вы соглашаетесь с обработкой персональных данных. Мы не передаём контакты третьим лицам.</p>
          <div class="form-status" role="status" aria-live="polite"></div>
        </form>

        <div class="form-success" hidden>
          <div class="form-success__icon">✓</div>
          <h3>Заявка отправлена</h3>
          <p>Спасибо! Перезвоним в течение рабочего дня. Если нужно срочно — <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>.</p>
          <a class="btn btn--ghost" href="index.html">Вернуться на главную</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""

PRIVACY = """<section class="page-hero" style="padding:clamp(40px,6vw,64px) 0">
  <div class="page-hero__inner container">
    <div class="breadcrumbs"><a href="index.html">Главная</a><span>/</span><span>Политика</span></div>
    <span class="eyebrow">Документы</span>
    <h1 style="font-size:clamp(1.9rem,3.6vw,2.8rem)">Политика конфиденциальности</h1>
    <p class="lead">Шаблон для сайта «Счастье есть». Перед публикацией замените реквизиты и проверьте текст у юриста.</p>
  </div>
</section>

<section class="section section--cream">
  <div class="container" style="max-width:820px">
    <h2>1. Общие положения</h2>
    <p>Настоящая политика определяет порядок обработки и защиты персональных данных посетителей сайта лофт-пространства и кофейни «Счастье есть», расположенного по адресу: Московская область, г. Орехово-Зуево, ул. 1905 года, 2.</p>
    <p>Оператор персональных данных: <em>[наименование ИП/ООО, ИНН, ОГРН — заполнить]</em>.</p>

    <h2>2. Какие данные собираются</h2>
    <p>Имя, телефон, адрес электронной почты, дата и параметры мероприятия, комментарий, отметка о согласии, а также технические данные (IP, cookie, страница обращения) — если подключена аналитика.</p>

    <h2>3. Цели обработки</h2>
    <p>Обратная связь по заявке, подготовка сметы и договора, подтверждение бронирования, информирование об акциях и мастер-классах при отдельном согласии.</p>

    <h2>4. Передача третьим лицам</h2>
    <p>Данные не передаются третьим лицам, кроме случаев, предусмотренных законом, и сервисов, обеспечивающих работу сайта (хостинг, CRM, почтовый сервис) — в объёме, необходимом для обработки заявки.</p>

    <h2>5. Сроки и удаление</h2>
    <p>Данные хранятся до достижения целей обработки или до отзыва согласия. Отозвать согласие можно письмом на <em>[e-mail — заполнить]</em> или по телефону <a data-phone data-phone-text href="tel:+79163526995">+7 (916) 352-69-95</a>.</p>

    <h2>6. Cookie</h2>
    <p>Сайт может использовать cookie для запоминания настроек и аналитики. Их можно отключить в браузере — часть функций при этом может работать иначе.</p>

    <h2>7. Изменения</h2>
    <p>Актуальная версия политики всегда опубликована на этой странице. Дата обновления: <em>[дата — заполнить]</em>.</p>

    <p style="margin-top:28px"><a class="btn btn--ghost" href="index.html">Вернуться на главную</a></p>
  </div>
</section>
"""

NOT_FOUND = """<section class="section section--cream" style="min-height:60vh;display:grid;place-items:center">
  <div class="container" style="text-align:center">
    <span class="eyebrow" style="justify-content:center">404</span>
    <h1>Такой страницы нет</h1>
    <p class="lead" style="margin:0 auto 26px">Возможно, ссылка устарела. Начните с главной или посмотрите меню и мастер-классы.</p>
    <div class="hero__actions" style="justify-content:center">
      <a class="btn btn--primary" href="index.html">На главную</a>
      <a class="btn btn--ghost" href="contacts.html">Контакты</a>
    </div>
  </div>
</section>
"""

if __name__ == "__main__":
    os.makedirs(SITE, exist_ok=True)
    page("index.html",
         "Счастье есть — лофт-пространство, кофейня и мастер-классы в Орехово-Зуево",
         "«Счастье есть» — лофт-пространство и кофейня в Орехово-Зуево на улице 1905 года, 2. Кофе и домашняя выпечка, мастер-классы, детские праздники, аренда лофта и кейтеринг. Ежедневно 09:00–21:00.",
         "index.html", INDEX)
    page("menu.html",
         "Меню — кофе, выпечка, завтраки и десерты · «Счастье есть»",
         "Меню кофейни «Счастье есть» в Орехово-Зуево: кофе на профессиональной кофемашине, домашняя выпечка, завтраки, десерты и торты на заказ, кейтеринг с выездом.",
         "menu.html", MENU)
    page("master-classes.html",
         "Мастер-классы в Орехово-Зуево · «Счастье есть»",
         "Кулинарные и творческие мастер-классы для детей, семей и взрослых в лофт-пространстве «Счастье есть»: день рождения, корпоратив, выездные занятия. Орехово-Зуево, ул. 1905 года, 2.",
         "master-classes.html", MASTER)
    page("events.html",
         "Мероприятия и праздники под ключ · «Счастье есть»",
         "Детские дни рождения, семейные юбилеи, выпускные и корпоративы в лофт-пространстве «Счастье есть»: зал, аниматор, оформление, кейтеринг. Орехово-Зуево, ул. 1905 года, 2.",
         "events.html", EVENTS)
    page("gallery.html",
         "Галерея — зал, гости, мастер-классы и праздники · «Счастье есть»",
         "21 фотография лофт-пространства «Счастье есть» в Орехово-Зуево: зал и витрина, гости, мастер-классы, оформление праздников и главный вход.",
         "gallery.html", GALLERY)
    page("contacts.html",
         "Контакты и адрес · «Счастье есть», Орехово-Зуево",
         "Контакты лофт-пространства «Счастье есть»: Орехово-Зуево, ул. 1905 года, 2, телефон +7 (916) 352-69-95, ежедневно 09:00–21:00. Карта, схема проезда, оценки и отзывы.",
         "contacts.html", CONTACTS)
    page("booking.html",
         "Оставить заявку · «Счастье есть»",
         "Оставьте заявку на праздник, аренду лофта, мастер-класс или кейтеринг в «Счастье есть». Перезвоним в течение рабочего дня. Орехово-Зуево, ул. 1905 года, 2.",
         "booking.html", BOOKING)
    page("privacy.html",
         "Политика конфиденциальности · «Счастье есть»",
         "Политика обработки персональных данных сайта лофт-пространства «Счастье есть». Шаблон, требует заполнения реквизитов оператора.",
         "", PRIVACY)
    page("404.html",
         "Страница не найдена · «Счастье есть»",
         "Страница не найдена.",
         "", NOT_FOUND)
    print("Готово.")
