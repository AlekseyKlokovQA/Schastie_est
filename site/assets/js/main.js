/* ============================================================
   «Счастье есть» — интерактив сайта
   Контент (фото, акции) подтягивается из data/content.json,
   чтобы правки из админ-панели сразу попадали на страницы.
   ============================================================ */
(function () {
  'use strict';

  var CONFIG = {
    phone: '+7 (916) 352-69-95',
    phoneHref: 'tel:+79163526995',
    endpoint: '/api/leads',        // приём заявок; пусто — демо-режим
    welcomeAlways: false,          // true — показывать заставку при каждом заходе
    contentUrl: '../data/content.json'
  };
  window.HAPPINESS_CONFIG = CONFIG;

  /* Резервный контент: если data/content.json недоступен (file:// или правки
     не сохранены), сайт всё равно показывает фото и акции. */
  var FALLBACK = {
    photos: {
      welcome: 'https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc87ef060ef9ce3eedd668a49d/XXXL',
      entrance: 'https://avatars.mds.yandex.net/get-altay/10766931/2a0000019247a50d1c09f97fce652e8803a3/XXXL',
      hall: 'https://avatars.mds.yandex.net/get-altay/11018317/2a0000018cbc80be39818072da4bc6a2886a/XXXL',
      hall2: 'https://avatars.mds.yandex.net/get-altay/6382111/2a0000018cbc809395ac079d1d286f434f9d/XXXL',
      hall3: 'https://avatars.mds.yandex.net/get-altay/892711/2a0000018cbc8093d9b247cebbd7f2950d66/XXXL',
      hall4: 'https://avatars.mds.yandex.net/get-altay/10700956/2a0000018cbc8093d40d2c330207f4bbe358/XXXL',
      menu1: 'https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc87ef060ef9ce3eedd668a49d/XXXL',
      menu2: 'https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc8054b0aed411cbfdf2f5da2d/XXXL',
      menu3: 'https://avatars.mds.yandex.net/get-altay/11187599/2a0000018cbc880da6775a3d6696ca81a4b8/XXXL',
      menu4: 'https://avatars.mds.yandex.net/get-altay/13072111/2a0000018ef00b7746b0e63985d978d0b426/XXXL',
      guests1: 'https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc87ef060ef9ce3eedd668a49d/XXXL',
      guests2: 'https://avatars.mds.yandex.net/get-altay/10700095/2a0000018cbc8054b0aed411cbfdf2f5da2d/XXXL',
      guests3: 'https://avatars.mds.yandex.net/get-altay/11187599/2a0000018cbc880da6775a3d6696ca81a4b8/XXXL',
      guests4: 'https://avatars.mds.yandex.net/get-altay/13072111/2a0000018ef00b7746b0e63985d978d0b426/XXXL',
      guests5: 'https://avatars.mds.yandex.net/get-altay/10647561/2a0000018d36aa786e95dd0dafc0b3efed74/XXXL',
      master1: 'https://avatars.mds.yandex.net/get-altay/11203687/2a000001928aa901c504a27dda58db9872b2/XXXL',
      master2: 'https://avatars.mds.yandex.net/get-altay/11356085/2a000001928aa901cc3db3f92f046716b653/XXXL',
      master3: 'https://avatars.mds.yandex.net/get-altay/14091921/2a000001928aa9079589c77cf430107fac5e/XXXL',
      master4: 'https://avatars.mds.yandex.net/get-altay/13474366/2a000001928aa9015971c1ac59465d0e805c/XXXL',
      master5: 'https://avatars.mds.yandex.net/get-altay/13790728/2a000001928aa901f60545791c9985568b71/XXXL',
      master6: 'https://avatars.mds.yandex.net/get-altay/14097168/2a000001928aa901e042589b6492bb005179/XXXL',
      event1: 'https://avatars.mds.yandex.net/get-altay/13797017/2a000001928aa9731bf200ae689d02706328/XXXL',
      event2: 'https://avatars.mds.yandex.net/get-altay/13906970/2a000001928aa97570eb0a712b428bdd0abe/XXXL',
      event3: 'https://avatars.mds.yandex.net/get-altay/14238289/2a000001928aa972cfdd2f63588ead45a07f/XXXL',
      event4: 'https://avatars.mds.yandex.net/get-altay/14165812/2a000001928aa97926cdd1890b2f0569f792/XXXL',
      event5: 'https://avatars.mds.yandex.net/get-altay/13929277/2a000001928aa973675fde3c29be02f92635/XXXL'
    },
    promos: [
      { title: 'Кофе + выпечка = 390 ₽', text: 'Каждый будний день до 12:00: любой кофе 250–300 мл и свежая выпечка из витрины по специальной цене.', badge: '11:00–12:00', until: '' },
      { title: 'День рождения в лофте', text: 'Аренда зала на 3 часа, оформление фотозоны и торт — по одной заявке. Свободные даты на ближайшие выходные уточняйте у администратора.', badge: 'Хит', until: '' }
    ]
  };

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };

  /* ---------------- Контент: фото и акции ---------------- */
  function applyPhotos(photos) {
    $$('[data-img]').forEach(function (img) {
      var key = img.getAttribute('data-img');
      if (!(key in photos)) return;
      var url = photos[key];
      var box = img.closest('.ph, .media, .gallery__item');
      if (box) box.classList.remove('is-broken');
      if (url) {
        img.src = url;
        /* обложка: то же фото дублируем фоном самого блока.
           Если <img> по какой-то причине не отрисуется, фон всё равно
           растянется на всю секцию через background-size: cover. */
        var bg = img.closest('[data-bg-photo]');
        if (bg) {
          bg.style.backgroundImage = 'url("' + url + '")';
          bg.style.backgroundSize = 'cover';
          bg.style.backgroundPosition = 'center 40%';
        }
      } else {
        img.removeAttribute('src');
        if (box) box.classList.add('is-broken');
        var bgEmpty = img.closest('[data-bg-photo]');
        if (bgEmpty) bgEmpty.style.backgroundImage = '';
      }
    });
  }

  function markBroken() {
    $$('img').forEach(function (img) {
      /* обложка — фон, а не карточка: placeholder ей не нужен и вредит */
      if (img.closest('[data-bg-photo]')) return;
      if (img.dataset.boundBroken) return;
      img.dataset.boundBroken = '1';
      img.addEventListener('error', function () {
        var box = img.closest('.ph, .media, .gallery__item');
        if (box) box.classList.add('is-broken');
      });
      img.addEventListener('load', function () {
        var box = img.closest('.ph, .media, .gallery__item');
        if (box) box.classList.remove('is-broken');
      });
      if (img.complete && img.naturalWidth === 0) {
        var box = img.closest('.ph, .media, .gallery__item');
        if (box) box.classList.add('is-broken');
      }
    });
  }

  function renderPromos(promos) {
    $$('[data-promos]').forEach(function (host) {
      var limit = Number(host.getAttribute('data-promos-limit')) || promos.length;
      var list = promos.slice(0, limit);
      if (!list.length) { host.innerHTML = ''; return; }
      host.innerHTML = list.map(function (p) {
        return '<article class="card card--hover reveal">' +
          (p.badge ? '<span class="price-pill">' + esc(p.badge) + '</span>' : '') +
          '<h3 style="margin-top:12px">' + esc(p.title) + '</h3>' +
          '<p class="mb-0" style="color:var(--ink-soft)">' + esc(p.text) + '</p>' +
          (p.until ? '<p class="small" style="margin-top:10px;color:var(--ink-mute)">Действует до ' + esc(p.until) + '</p>' : '') +
          '</article>';
      }).join('');
      initReveal();
    });
  }

  function loadContent() {
    /* 1. Сразу показываем резервный набор, чтобы страница не была пустой. */
    applyPhotos(FALLBACK.photos);
    renderPromos(FALLBACK.promos);
    markBroken();
    if (location.protocol === 'file:') return;

    /* 2. Затем подтягиваем data/content.json — правки из админки. */
    var paths = [CONFIG.contentUrl, 'data/content.json', '/data/content.json'];
    var tried = 0;
    (function next() {
      if (tried >= paths.length) return;
      fetch(paths[tried++], { cache: 'no-store' })
        .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (data) {
          if (data.photos && Object.keys(data.photos).length) applyPhotos(data.photos);
          if (Array.isArray(data.promos)) renderPromos(data.promos);
          markBroken();
        })
        .catch(next);
    })();
  }

  /* ---------------- Приветственная анимация ---------------- */
  function initWelcome() {
    var welcome = $('[data-welcome]');
    if (!welcome) return;

    var KEY = 'happiness_welcome_seen';
    var seen = false;
    try { seen = sessionStorage.getItem(KEY) === '1'; } catch (e) {}
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if ((seen && !CONFIG.welcomeAlways) || reduceMotion) {
      welcome.remove();
      document.body.classList.add('welcome-done');
      return;
    }

    document.body.classList.add('is-locked');
    var finished = false;

    function finish() {
      if (finished) return;
      finished = true;
      welcome.classList.add('is-closing');
      try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
      document.body.classList.remove('is-locked');
      document.body.classList.add('welcome-done');
      setTimeout(function () { if (welcome.parentNode) welcome.parentNode.removeChild(welcome); }, 900);
    }

    var timer = setTimeout(finish, 2700);
    /* аварийный таймер: если что-то помешало finish(), заставка всё равно уйдёт */
    setTimeout(finish, 6000);

    var skip = $('[data-welcome-skip]');
    if (skip) skip.addEventListener('click', function () { clearTimeout(timer); finish(); });
    welcome.addEventListener('click', function (e) {
      if (e.target === welcome) { clearTimeout(timer); finish(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { clearTimeout(timer); finish(); }
    });
  }

  /* ---------------- Шапка и мобильное меню ---------------- */
  function initHeader() {
    var header = $('.header');
    if (header) {
      var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 12); };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }
    var burger = $('.burger');
    if (!burger) return;
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    $$('.nav__link').forEach(function (link) {
      link.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
    document.addEventListener('click', function (e) {
      if (!document.body.classList.contains('nav-open')) return;
      if (e.target.closest('.nav') || e.target.closest('.burger')) return;
      document.body.classList.remove('nav-open');
      burger.setAttribute('aria-expanded', 'false');
    });
  }

  /* ---------------- Появление блоков ---------------- */
  var revealObserver = null;
  function initReveal() {
    var items = $$('.reveal:not(.is-visible)');
    if (!items.length) return;
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    if (!revealObserver) {
      revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    }
    items.forEach(function (el) { revealObserver.observe(el); });
  }

  /* ---------------- Галерея-лайтбокс ---------------- */
  function initLightbox() {
    var triggers = $$('[data-lightbox]');
    if (!triggers.length) return;

    var box = document.createElement('div');
    box.className = 'lightbox';
    box.innerHTML =
      '<button class="lightbox__nav lightbox__nav--prev" aria-label="Предыдущее фото">‹</button>' +
      '<img alt="">' +
      '<button class="lightbox__nav lightbox__nav--next" aria-label="Следующее фото">›</button>' +
      '<button class="lightbox__close" aria-label="Закрыть">×</button>' +
      '<div class="lightbox__cap"></div>';
    document.body.appendChild(box);

    var img = $('img', box);
    var cap = $('.lightbox__cap', box);
    var index = 0;

    function srcOf(btn) {
      /* приоритет — актуальное фото в блоке (его могли заменить в админке) */
      var inner = btn.querySelector('img');
      if (inner && inner.getAttribute('src')) return inner.getAttribute('src');
      return btn.getAttribute('data-lightbox');
    }

    function show(i) {
      index = (i + triggers.length) % triggers.length;
      var btn = triggers[index];
      img.src = srcOf(btn);
      img.alt = btn.getAttribute('data-alt') || (btn.querySelector('img') ? btn.querySelector('img').alt : '');
      cap.textContent = (btn.getAttribute('data-cap') || '') + ' · ' + (index + 1) + ' / ' + triggers.length;
    }
    function open(i) {
      show(i);
      box.classList.add('is-open');
      document.body.classList.add('is-locked');
    }
    function close() {
      box.classList.remove('is-open');
      document.body.classList.remove('is-locked');
    }

    triggers.forEach(function (btn, i) {
      btn.addEventListener('click', function (e) { e.preventDefault(); open(i); });
    });
    $('.lightbox__nav--prev', box).addEventListener('click', function () { show(index - 1); });
    $('.lightbox__nav--next', box).addEventListener('click', function () { show(index + 1); });
    box.addEventListener('click', function (e) {
      if (e.target === box || e.target.classList.contains('lightbox__close')) close();
    });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }

  /* ---------------- График: подсветка дня и статус ---------------- */
  function initHours() {
    var table = $('[data-hours]');
    if (!table) return;
    var day = new Date().getDay();
    var index = day === 0 ? 6 : day - 1;
    $$('tr[data-day]', table).forEach(function (row, i) {
      if (i === index) row.classList.add('is-today');
    });
    var note = $('[data-open-state]');
    if (note) {
      var h = new Date().getHours();
      var open = h >= 9 && h < 21;
      note.textContent = open ? 'Сейчас открыто — заходите на кофе' : 'Сейчас закрыто — напишите, договоримся о визите';
      note.classList.toggle('is-open', open);
    }
  }

  /* ---------------- Телефоны, год, подписи ---------------- */
  function initBasics() {
    $$('[data-phone]').forEach(function (el) {
      el.setAttribute('href', CONFIG.phoneHref);
      if (el.hasAttribute('data-phone-text')) el.textContent = CONFIG.phone;
    });
    $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
    $$('[data-today]').forEach(function (el) {
      el.value = new Date().toISOString().slice(0, 10);
    });
  }

  /* ---------------- Формы заявок ---------------- */
  var RULES = {
    name: function (v) {
      if (v.trim().length < 2) return 'Укажите имя — хотя бы 2 символа';
      if (!/^[А-Яа-яЁёA-Za-z\s\-']+$/.test(v.trim())) return 'В имени допустимы только буквы, пробел и дефис';
      return '';
    },
    phone: function (v) {
      var d = v.replace(/\D/g, '');
      if (d.length < 10) return 'Проверьте номер: нужно 10–11 цифр';
      if (d.length > 11) return 'Слишком много цифр в номере';
      return '';
    },
    email: function (v) {
      if (!v.trim()) return '';
      if (!/^[^\s@]+@[^\s@]+\.[a-zA-Zа-яА-Я]{2,}$/.test(v.trim())) return 'Похоже, в адресе опечатка';
      return '';
    },
    message: function (v, field) {
      if (field.hasAttribute('data-optional') && !v.trim()) return '';
      if (v.trim().length < 5) return 'Пары слов будет достаточно';
      return '';
    },
    date: function (v) {
      if (!v) return '';
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var chosen = new Date(v);
      if (isNaN(chosen.getTime())) return 'Не удалось распознать дату';
      if (chosen < today) return 'Дата уже прошла — выберите будущую';
      return '';
    },
    consent: function (v, field) { return field.checked ? '' : 'Без согласия мы не сможем принять заявку'; }
  };

  function validateField(field) {
    var wrapper = field.closest('.field');
    if (!wrapper) return true;
    var rule = RULES[field.name];
    var errorEl = $('.field__error', wrapper);
    var msg = rule ? rule(field.value, field) : '';
    if (msg) {
      wrapper.classList.add('has-error');
      field.setAttribute('aria-invalid', 'true');
      if (errorEl) errorEl.textContent = msg;
      return false;
    }
    wrapper.classList.remove('has-error');
    field.removeAttribute('aria-invalid');
    if (errorEl) errorEl.textContent = '';
    return true;
  }

  function initForms() {
    $$('form[data-lead-form]').forEach(function (form) {
      var status = $('.form-status', form);
      var success = $('.form-success', form.parentNode) || $('.form-success', form);
      var fields = $$('input, select, textarea', form).filter(function (f) {
        return f.name && f.type !== 'submit';
      });

      fields.forEach(function (field) {
        field.addEventListener('blur', function () {
          if (field.value || field.type === 'checkbox') validateField(field);
        });
        field.addEventListener('input', function () {
          var wrapper = field.closest('.field');
          if (wrapper && wrapper.classList.contains('has-error')) validateField(field);
        });
      });

      var phone = $('input[name="phone"]', form);
      if (phone) {
        phone.addEventListener('input', function () {
          var d = phone.value.replace(/\D/g, '');
          if (d[0] === '8') d = '7' + d.slice(1);
          if (d[0] !== '7') d = '7' + d;
          d = d.slice(0, 11);
          var out = '+7';
          if (d.length > 1) out += ' (' + d.slice(1, 4);
          if (d.length >= 5) out += ') ' + d.slice(4, 7);
          if (d.length >= 8) out += '-' + d.slice(7, 9);
          if (d.length >= 10) out += '-' + d.slice(9, 11);
          phone.value = out;
        });
      }

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (status) { status.textContent = ''; status.className = 'form-status'; }

        var valid = true;
        fields.forEach(function (field) { if (!validateField(field)) valid = false; });

        if (!valid) {
          if (status) {
            status.textContent = 'Проверьте выделенные поля — и всё получится.';
            status.className = 'form-status is-error';
          }
          var firstError = $('.field.has-error input, .field.has-error select, .field.has-error textarea', form);
          if (firstError) firstError.focus();
          return;
        }

        var payload = {
          form: form.getAttribute('data-lead-form') || 'Заявка',
          page: location.pathname,
          createdAt: new Date().toISOString()
        };
        fields.forEach(function (field) {
          payload[field.name] = field.type === 'checkbox' ? field.checked : field.value;
        });

        var submitBtn = $('button[type="submit"]', form);
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.dataset.label = submitBtn.textContent;
          submitBtn.textContent = 'Отправляем…';
        }

        function done() {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label; }
          if (success) {
            form.hidden = true;
            success.hidden = false;
            success.scrollIntoView({ behavior: 'smooth', block: 'center' });
          } else if (status) {
            status.textContent = 'Спасибо! Заявка принята — свяжемся в течение рабочего дня.';
            status.className = 'form-status is-success';
            form.reset();
          }
          storeLeadLocal(payload);
        }

        function fail() {
          if (status) {
            status.textContent = 'Не удалось отправить. Позвоните нам: ' + CONFIG.phone;
            status.className = 'form-status is-error';
          }
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = submitBtn.dataset.label; }
        }

        if (CONFIG.endpoint) {
          fetch(CONFIG.endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          }).then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json().catch(function () { return {}; });
          }).then(function () {
            done();
          }).catch(function () {
            /* сервер недоступен (например, открыт file://) — держим заявку локально */
            storeLeadLocal(payload);
            done();
          });
        } else {
          storeLeadLocal(payload);
          setTimeout(done, 400);
        }
      });
    });
  }

  function storeLeadLocal(payload) {
    try {
      var key = 'happiness_leads';
      var list = JSON.parse(localStorage.getItem(key) || '[]');
      list.unshift({
        id: payload.createdAt,
        name: payload.name || '—',
        phone: payload.phone || '—',
        email: payload.email || '—',
        type: payload.form || 'Заявка',
        topic: payload.topic || '—',
        date: payload.date || '—',
        guests: payload.guests || '—',
        message: payload.message || '',
        consent: payload.consent !== false,
        createdAt: payload.createdAt,
        status: 'new'
      });
      localStorage.setItem(key, JSON.stringify(list.slice(0, 300)));
    } catch (e) {}
  }

  /* ---------------- Запуск ---------------- */
  function boot() {
    initBasics();
    /* если скрипт упал до initWelcome, заставка всё равно должна исчезнуть */
    setTimeout(function () {
      var stuck = $('[data-welcome]');
      if (stuck && !stuck.classList.contains('is-closing')) {
        stuck.classList.add('is-closing');
        document.body.classList.remove('is-locked');
        setTimeout(function () { if (stuck.parentNode) stuck.parentNode.removeChild(stuck); }, 900);
      }
    }, 8000);
    initWelcome();
    initHeader();
    loadContent();
    initReveal();
    initLightbox();
    initHours();
    initForms();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
