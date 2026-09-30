// Collection viewer: swaps the large image and caption, keeps thumbnails in sync.
(function () {
  var root = document.querySelector('[data-viewer]');
  if (!root) return;
  var items = JSON.parse(root.querySelector('[data-items]').textContent);
  var art = root.querySelector('.collection-art');
  var title = root.querySelector('[data-title]');
  var desc = root.querySelector('[data-description]');
  var note = root.querySelector('[data-note]');
  var counter = root.querySelector('[data-counter]');
  var prev = root.querySelector('[data-prev]');
  var next = root.querySelector('[data-next]');
  var strip = root.querySelector('.thumbnail-row');
  var thumbs = root.querySelectorAll('.art-thumbnail');
  var selected = 0;
  var pad = function (n) { return String(n).padStart(2, '0'); };

  function show(i) {
    if (i < 0 || i >= items.length) return;
    selected = i;
    var item = items[i];
    art.src = '../' + item.src;
    art.width = item.width;
    art.height = item.height;
    art.alt = item.description + (item.totalViews > 1 ? ' — view ' + item.view : '');
    title.textContent = item.title;
    desc.textContent = item.description;
    note.textContent = 'Provisional title' +
      (item.totalViews > 1 ? ' · View ' + item.view + ' of ' + item.totalViews : '');
    counter.textContent = pad(i + 1) + ' / ' + pad(items.length);
    prev.disabled = i === 0;
    next.disabled = i === items.length - 1;
    thumbs.forEach(function (t, j) {
      t.classList.toggle('is-selected', j === i);
      t.setAttribute('aria-pressed', j === i ? 'true' : 'false');
    });
    var b = thumbs[i];
    var left = b.offsetLeft - strip.offsetLeft;
    if (left < strip.scrollLeft || left + b.offsetWidth > strip.scrollLeft + strip.clientWidth) {
      strip.scrollLeft = left - strip.clientWidth / 2 + b.offsetWidth / 2;
    }
  }

  prev.addEventListener('click', function () { show(selected - 1); });
  next.addEventListener('click', function () { show(selected + 1); });
  thumbs.forEach(function (t) {
    t.addEventListener('click', function () { show(Number(t.dataset.index)); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(selected - 1);
    if (e.key === 'ArrowRight') show(selected + 1);
  });
})();
