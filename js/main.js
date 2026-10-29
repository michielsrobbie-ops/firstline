// First Line – navigatie, formulieren (FormSubmit) en galerij-lightbox.
// FormSubmit: inzendingen gaan naar events@firstlinekranevo.com (voorlopig, campagne-adres); de eerste inzending vraagt een activatie via mail.
(function () {
  // Mobiel menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Teksten per taal
  var lang = (document.documentElement.lang || 'bg').slice(0, 2);
  var T = {
    bg: { fill: 'Моля, попълнете полето', sending: 'Изпращане…', ok: 'Запитването е изпратено. Ще се свържем с Вас.', err: 'Запитването не беше изпратено. Опитайте отново или ни се обадете на 088 686 1001.' },
    en: { fill: 'Please fill in', sending: 'Sending…', ok: 'Your enquiry has been sent. We will get back to you.', err: 'Your enquiry was not sent. Please try again or call us on +359 88 686 1001.' },
    ru: { fill: 'Пожалуйста, заполните поле', sending: 'Отправка…', ok: 'Запрос отправлен. Мы свяжемся с вами.', err: 'Запрос не отправлен. Попробуйте ещё раз или позвоните нам: +359 88 686 1001.' }
  }[lang] || null;
  if (!T) T = { fill: 'Моля, попълнете полето', sending: 'Изпращане…', ok: 'Запитването е изпратено.', err: 'Грешка.' };

  // Повод vooraf kiezen via ?povod=svatba / firmeno / masa (werkt in alle talen via data-key)
  var reason = document.getElementById('c-reason');
  if (reason) {
    var p = new URLSearchParams(location.search).get('povod');
    if (p) {
      Array.prototype.forEach.call(reason.options, function (o, i) {
        if (o.getAttribute('data-key') === p) reason.selectedIndex = i;
      });
    }
  }

  // Formulieren
  document.querySelectorAll('form[data-form]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var button = form.querySelector('button[type="submit"]');

    function setStatus(text, kind) {
      status.textContent = text;
      status.className = 'form-status' + (kind ? ' ' + kind : '');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstInvalid = null;
      form.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.checkValidity();
        el.classList.toggle('invalid', !ok);
        el.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !firstInvalid) firstInvalid = el;
      });
      if (firstInvalid) {
        var label = form.querySelector('label[for="' + firstInvalid.id + '"]');
        var name = label ? label.childNodes[0].textContent.trim() : '';
        setStatus(T.fill + ' „' + name + '“.', 'err');
        firstInvalid.focus();
        return;
      }

      button.disabled = true;
      setStatus(T.sending);
      fetch(form.action, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
        .then(function (res) {
          if (!res.ok) throw new Error('send failed');
          form.reset();
          setStatus(T.ok, 'ok');
        })
        .catch(function () {
          setStatus(T.err, 'err');
        })
        .finally(function () { button.disabled = false; });
    });
  });

  // Lightbox galerij
  var dialog = document.querySelector('.lightbox');
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-lightbox]'));
  if (dialog && links.length && typeof dialog.showModal === 'function') {
    var img = dialog.querySelector('img');
    var index = 0;
    function show(i) {
      index = (i + links.length) % links.length;
      var thumb = links[index].querySelector('img');
      img.src = links[index].getAttribute('href');
      img.alt = thumb ? thumb.alt : '';
    }
    links.forEach(function (a, i) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        show(i);
        dialog.showModal();
      });
    });
    dialog.querySelector('.lb-close').addEventListener('click', function () { dialog.close(); });
    dialog.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    dialog.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog || e.target.classList.contains('lightbox-inner')) dialog.close();
    });
    dialog.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
  }
})();
