// 쇼츠 타임라인 엔진: setTime(t)가 t초 시점의 화면을 결정적으로 그린다 (render.py가 프레임마다 호출).
// - .beat[data-d]   : 가운데 비주얼, 순서대로 재생 (d = 길이 초)
// - .cap            : 같은 순번의 자막
// - .pop[data-at]   : 비트 시작 후 at초에 튀어나오는 요소
// - [data-type]     : 비트 시작 후 data-at초부터 글자가 타이핑되는 요소
// - [data-grow]     : 비트 시작 후 data-at초부터 width가 0 → data-grow(%)로 늘어나는 요소
// - [data-rot]      : "from,to" 각도로 회전 (게이지 바늘 등)
(() => {
  const clamp = (x) => Math.max(0, Math.min(1, x));
  const easeOut = (x) => 1 - Math.pow(1 - clamp(x), 3);
  const back = (x) => { x = clamp(x); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };

  const beats = [...document.querySelectorAll('.beat')];
  const caps = [...document.querySelectorAll('.cap')];
  let acc = 0;
  const starts = beats.map((b) => { const s = acc; acc += parseFloat(b.dataset.d); return s; });
  window.TOTAL = acc;

  document.querySelectorAll('[data-type]').forEach((el) => { el.dataset.full = el.textContent; });

  window.setTime = (t) => {
    const bar = document.querySelector('.progress > div');
    if (bar) bar.style.width = `${clamp(t / acc) * 100}%`;

    beats.forEach((b, i) => {
      const local = t - starts[i];
      const on = local >= 0 && local < parseFloat(b.dataset.d);
      const cap = caps[i];
      if (!on) { b.style.opacity = 0; if (cap) cap.style.opacity = 0; return; }

      const e = easeOut(local / 0.35);
      b.style.opacity = e;
      b.style.transform = `translateY(${(1 - e) * 60}px) scale(${0.94 + 0.06 * back(local / 0.4)})`;
      if (cap) {
        cap.style.opacity = clamp(local / 0.12);
        cap.style.transform = `scale(${0.86 + 0.14 * back(local / 0.22)})`;
      }

      b.querySelectorAll('.pop').forEach((el) => {
        const p = (local - parseFloat(el.dataset.at || 0)) / 0.3;
        el.style.opacity = clamp(p * 1.4);
        el.style.transform = `translateY(${(1 - easeOut(p)) * 30}px) scale(${0.8 + 0.2 * back(p)})`;
      });
      b.querySelectorAll('[data-type]').forEach((el) => {
        const cps = parseFloat(el.dataset.cps || 22);
        const n = Math.floor(Math.max(0, local - parseFloat(el.dataset.at || 0)) * cps);
        const full = el.dataset.full;
        el.textContent = full.slice(0, n);
        el.classList.toggle('typing', n < full.length && n > 0);
      });
      b.querySelectorAll('[data-grow]').forEach((el) => {
        const p = easeOut((local - parseFloat(el.dataset.at || 0)) / 0.6);
        el.style.width = `${p * parseFloat(el.dataset.grow)}%`;
      });
      b.querySelectorAll('[data-rot]').forEach((el) => {
        const [a, z] = el.dataset.rot.split(',').map(Number);
        const p = back((local - parseFloat(el.dataset.at || 0)) / 0.9);
        el.style.transform = `rotate(${a + (z - a) * p}deg)`;
      });
    });
  };
  window.setTime(0);
})();
