const { chromium } = require('/home/claude/web/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await (await b.newContext({viewport:{width:430,height:880},deviceScaleFactor:2})).newPage();
  await p.goto('file:///mnt/user-data/outputs/pidurdusmaa-pagelive.html'); await p.waitForTimeout(1800);
  await p.selectOption('[data-f=make]','Volkswagen'); await p.waitForTimeout(250);
  await p.selectOption('[data-f=model]','Golf'); await p.waitForTimeout(250);
  const yr = await p.$$eval('[data-f=year] option', o=>o.map(x=>x.value).filter(Boolean));
  await p.selectOption('[data-f=year]', yr[0]); await p.waitForTimeout(300);
  await p.click('[data-cond=snow]'); await p.click('[data-go]'); await p.waitForTimeout(1200);
  await p.click('.fb-fab'); await p.waitForTimeout(300);
  await p.click('.fb-box details summary'); await p.waitForTimeout(300);
  await p.screenshot({path:'/tmp/prev/panel.png'});
  await b.close();
})();
