const { chromium } = require('/home/claude/web/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await (await b.newContext({viewport:{width:1366,height:900}})).newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('http://localhost:8080/'); await p.waitForTimeout(1200);
  const before = await p.$eval('#tulemus', e=>e.hidden); console.log('tulemus peidus enne vajutust:', before);
  await p.click('[data-go]'); await p.waitForTimeout(300); console.log('ilma autota teade:', await p.isVisible('[data-go-msg]'));
  await p.click('[data-go-default]'); await p.waitForTimeout(400);
  await p.click('[data-r-toggle]');
  let n=0, bad=0;
  for (const car of [null, ['Volkswagen','Passat'], ['Škoda','Octavia']]) {
    if (car) { await p.selectOption('[data-calc] [data-f=make]', car[0]); await p.selectOption('[data-calc] [data-f=model]', car[1]);
      const y = await p.$$eval('[data-calc] [data-f=year] option', o=>o.map(x=>x.value).filter(Boolean)); await p.selectOption('[data-calc] [data-f=year]', y[0]); await p.waitForTimeout(200); }
    for (const c of ['wet','dry','snow','ice']) for (const sp of [50,80]) {
      await p.click(`[data-cond=${c}]`);
      await p.$eval('#f-speed', (el,v)=>{el.value=v; el.dispatchEvent(new Event('input'));}, sp);
      await p.waitForTimeout(150);
      const stale = await p.$eval('[data-go]', e=>e.textContent);
      await p.click('[data-go]'); await p.waitForTimeout(300);
      const cnt = await p.$$eval('.mbar', x=>x.length);
      for (let i=0;i<Math.min(cnt,4);i++) {
        const rs = await p.$$('.mbar'); await rs[i].click(); await p.waitForTimeout(60);
        const r = await p.evaluate(()=>({big:document.querySelector('[data-r-big]').textContent, big2:document.querySelector('[data-r-big2]').textContent,
          mbar:(document.querySelector('.mbar[aria-pressed=true] .v')||{}).textContent, bar:(document.querySelector('.bar[aria-pressed=true] .bd')||{}).textContent,
          range:document.querySelector('[data-r-range]').textContent, sp:document.querySelector('#f-speed').value, num:document.querySelector('[data-f=speednum]').value}));
        n++;
        const ok = r.mbar && r.mbar.replace(' m','')===r.big && r.big2===r.big && r.bar && r.bar.replace(' m','')===r.big && r.range===r.sp+' km/h → 0 km/h' && r.num===r.sp;
        if (!ok) { bad++; console.log('BAD', c, sp, JSON.stringify(r)); }
      }
    }
  }
  console.log('kontrollitud', n, 'vigu', bad, 'JS vead', JSON.stringify(errs));
  await b.close();
})();
