const { chromium } = require('/home/claude/web/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const ctx = await b.newContext({viewport:{width:1366,height:900}, permissions:['clipboard-read','clipboard-write']});
  const p = await ctx.newPage();
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file:///mnt/user-data/outputs/pidurdusmaa-pagelive.html');
  await p.waitForTimeout(1800);
  // teekond: auto, mõõt, pind, arvuta
  await p.selectOption('[data-f=make]','Volkswagen'); await p.waitForTimeout(250);
  await p.selectOption('[data-f=model]','Golf'); await p.waitForTimeout(250);
  const yr = await p.$$eval('[data-f=year] option', o=>o.map(x=>x.value).filter(Boolean));
  await p.selectOption('[data-f=year]', yr[0]); await p.waitForTimeout(400);
  await p.click('[data-cond=snow]'); await p.waitForTimeout(200);
  await p.click('[data-go]'); await p.waitForTimeout(1200);
  await p.click('[data-tab=valik]'); await p.waitForTimeout(300);
  await p.click('#p-valik [data-ct=main][data-v=safe]'); await p.waitForTimeout(800);
  // rehvide leht + otsing + filter
  await p.goto('file:///mnt/user-data/outputs/pidurdusmaa-pagelive.html?p=%2Fvordle-rehve%2F');
  await p.waitForTimeout(1600);
  await p.fill('[data-q]','michelin'); await p.waitForTimeout(1600);
  const brands = await p.$$eval('[data-brand] option', o=>o.map(x=>x.value).filter(Boolean));
  if (brands.length) { await p.selectOption('[data-brand]', brands[0]); await p.waitForTimeout(700); }
  const add = await p.$('[data-add]'); if (add) { await add.click(); await p.waitForTimeout(400); }
  // paneel
  await p.click('.fb-fab'); await p.waitForTimeout(400);
  console.log('paneel:', await p.isVisible('.fb-ovl'), '|', await p.textContent('[data-fb-cnt]'));
  console.log('---- kokkuvõte ----');
  console.log(await p.textContent('[data-fb-sum]'));
  await p.fill('[data-fb-txt]','Autovalik on ok, aga talvel tundus number suur.');
  await p.click('[data-fb-copy]'); await p.waitForTimeout(500);
  console.log('teade:', await p.textContent('[data-fb-msg]'));
  const clip = await p.evaluate(()=>navigator.clipboard.readText());
  console.log('---- lõikelaud (algus) ----'); console.log(clip.split('\n').slice(0,26).join('\n'));
  await p.keyboard.press('Escape'); await p.waitForTimeout(300);
  console.log('sulgus:', !(await p.isVisible('.fb-ovl')), 'vead:', errs);
  await b.close();
})();
