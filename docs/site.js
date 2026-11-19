// Local-only Gazette filtering. No analytics, network calls, storage or cookies.
(() => {
  const filters = [...document.querySelectorAll('[data-gazette-filter]')];
  const field = document.querySelector('#notice-search');
  const list = [...document.querySelectorAll('[data-notice]')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#notice-empty');
  if (!filters.length || !field || !list.length) return;
  let category = 'all';
  function update() {
    const query = field.value.trim().toLocaleLowerCase();
    let visible = 0;
    list.forEach(item => {
      const matchesGroup = category === 'all' || item.dataset.category === category;
      const matchesText = !query || (item.textContent || '').toLocaleLowerCase().includes(query);
      item.hidden = !(matchesGroup && matchesText);
      if (!item.hidden) visible++;
    });
    if (count) count.textContent = visible + ' notice' + (visible === 1 ? '' : 's') + ' shown';
    if (empty) empty.hidden = visible !== 0;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.gazetteFilter;
    filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    update();
  }));
  field.addEventListener('input', update);
  update();
})();
