(function () {
  var form      = document.querySelector('.ctc-form');
  var toast     = document.getElementById('ctc-toast');
  var toastMsg  = document.getElementById('ctc-toast-msg');
  var container = document.getElementById('turnstile-container');
  var btn       = document.querySelector('.ctc-submit');

  if (!form || !toast || !toastMsg || !container || !btn) return;

  var SITE_KEY   = container.getAttribute('data-sitekey') || '';
  var origHTML   = btn.innerHTML;
  var widgetId   = null;
  var toastTimer = null;

  function showToast(msg, isError) {
    toastMsg.textContent = msg;
    toast.querySelector('i').className = isError
      ? 'bi bi-exclamation-circle-fill'
      : 'bi bi-check-circle-fill';
    toast.classList.toggle('ctc-toast--error', isError);
    toast.classList.toggle('ctc-toast--success', !isError);
    toast.classList.add('ctc-toast--visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.classList.remove('ctc-toast--visible');
    }, 5000);
  }

  function cleanup() {
    if (widgetId !== null && window.turnstile) {
      turnstile.remove(widgetId);
      widgetId = null;
    }
    container.classList.remove('ctc-turnstile-wrap--visible');
    btn.disabled = false;
    btn.innerHTML = origHTML;
  }

  btn.addEventListener('click', function () {
    if (!form.reportValidity()) return;
    if (!window.turnstile) {
      showToast('Security check unavailable. Please try again.', true);
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Verifying...';
    container.classList.add('ctc-turnstile-wrap--visible');

    widgetId = turnstile.render(container, {
      sitekey: SITE_KEY,
      theme: 'dark',

      callback: function (token) {
        // Read .value directly — new FormData(form) misses iOS autofilled values
        var data = new FormData();
        data.set('contact_form', '1');
        data.set('name',    form.querySelector('[name="name"]').value);
        data.set('email',   form.querySelector('[name="email"]').value);
        data.set('subject', form.querySelector('[name="subject"]').value);
        data.set('message', form.querySelector('[name="message"]').value);
        data.set('cf-turnstile-response', token);

        var fetchDone   = false;
        var fetchResult = null;

        fetch(form.action, {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
          body: data
        })
          .then(function (r) { return r.json(); })
          .then(function (r) { fetchResult = r; fetchDone = true; })
          .catch(function ()  { fetchResult = { ok: false }; fetchDone = true; });

        var secs = 3;
        btn.textContent = secs + '...';

        var tick = setInterval(function () {
          secs -= 1;
          if (secs > 0) {
            btn.textContent = secs + '...';
          } else {
            clearInterval(tick);
            var finish = function () {
              cleanup();
              if (fetchResult && fetchResult.ok) {
                form.reset();
                showToast('Your message has been sent successfully!', false);
              } else {
                var msg = (fetchResult && fetchResult.msg) || 'Something went wrong. Please try again.';
                showToast(msg, true);
              }
            };
            if (fetchDone) {
              finish();
            } else {
              var poll = setInterval(function () {
                if (fetchDone) { clearInterval(poll); finish(); }
              }, 50);
            }
          }
        }, 1000);
      },

      'error-callback': function () {
        cleanup();
        showToast('Security check failed. Please try again.', true);
      },

      'expired-callback': function () {
        cleanup();
      }
    });
  });
}());
