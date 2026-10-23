// First Line – navigatie, formulieren (FormSubmit) en galerij-lightbox.
// FormSubmit: de eerste inzending naar kranevo.firstline@gmail.com vraagt een activatie via mail.
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

  // Повод vooraf kiezen via ?povod=svatba / firmeno
  var reason = document.getElementById('c-reason');
  if (reason) {
    var p = new URLSearchParams(location.search).get('povod');
    var map = { svatba: 'Сватба', firmeno: 'Фирмено тържество', masa: 'Маса в ресторанта' };
    if (p && map[p]) reason.value = map[p];
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
        setStatus('Моля, попълнете полето „' + (label ? label.textContent.trim() : '') + '“.', 'err');
        firstInvalid.focus();
        return;
      }

      button.disabled = true;
      setStatus('Изпращане…');
      fetch(form.action, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
        .then(function (res) {
          if (!res.ok) throw new Error('send failed');
          form.reset();
          setStatus('Запитването е изпратено. Ще се свържем с Вас.', 'ok');
        })
        .catch(function () {
          setStatus('Запитването не беше изпратено. Опитайте отново или ни се обадете на 088 686 1001.', 'err');
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
