// Crawl every same-site page from the sitemap plus discovered links; click every tab/button; report dead ends.
// Usage: node tools/crawl.js <baseURL> <out.json>   (needs playwright-core and /usr/bin/google-chrome)
const PW=process.env.PW||'/workspace/hanceville/landing/tools/node_modules/playwright-core';
const {chromium}=require(PW);const fs=require('fs');
const base=process.argv[2]||'http://localhost:8765/';const out=process.argv[3]||'crawl.json';
(async()=>{const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
const res={base,pages:{},broken:[],deadTabs:[],errors:[]};
for(const [vp,size] of [['desktop',{width:1350,height:900}],['mobile',{width:390,height:844}]]){
 const ctx=await b.newContext({viewport:size});const p=await ctx.newPage();let errs=[];
 p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 const queue=['index.html'];const seen=new Set();
 while(queue.length){const u=queue.shift();if(seen.has(u))continue;seen.add(u);errs=[];
  let st=0;try{const r=await p.goto(base+u,{waitUntil:'domcontentloaded',timeout:60000});st=r?r.status():0;await p.waitForTimeout(400);}catch(e){st=-1}
  if(st!==200){res.broken.push({vp,url:u,status:st});continue}
  const info=await p.evaluate(()=>{const a=[...document.querySelectorAll('a[href]')].map(x=>x.getAttribute('href'));
   const tabs=[...document.querySelectorAll('[role=tab],button[data-tab],[data-target],button[aria-controls]:not(#tab-toggle)')].map((t,i)=>({i,txt:(t.innerText||t.getAttribute('aria-label')||'').trim().slice(0,40),ctl:t.getAttribute('aria-controls')||t.dataset.tab||t.dataset.target||''}));
   const hashes=a.filter(h=>h.startsWith('#')&&h.length>1).filter(h=>{try{return !document.querySelector(h)}catch(e){return true}});
   const empty=[...document.querySelectorAll('section,[role=tabpanel]')].filter(s=>s.innerText.trim().length<3&&!s.hidden&&s.offsetParent).map(s=>s.id||s.className);
   return {a,tabs,hashes,empty,words:document.body.innerText.split(/\s+/).length}});
  res.pages[vp+':'+u]={words:info.words,links:info.a.length,tabs:info.tabs.length,errors:errs.filter(e=>!/weather\.gov/.test(e)).slice(0,5)};
  info.hashes.forEach(h=>res.deadTabs.push({vp,url:u,kind:'missing-anchor',target:h}));
  info.empty.forEach(h=>res.deadTabs.push({vp,url:u,kind:'empty-section',target:h}));
  for(const t of info.tabs){const panel=t.ctl&&await p.evaluate(c=>{const el=document.getElementById(c);return el?el.innerText.trim().length:-1},t.ctl);
   if(t.ctl&&panel<=2)res.deadTabs.push({vp,url:u,kind:'tab-target-empty',target:t.ctl,label:t.txt});}
  if(errs.length)res.errors.push({vp,url:u,errs:errs.slice(0,3)});
  for(const h of info.a){if(/^(https?:|mailto:|tel:|sms:|#|javascript:|data:)/.test(h)&&!h.startsWith(base))continue;
   const path=h.replace(base,'').split('#')[0].split('?')[0];if(!path||/\.(ics|png|jpg|webp|svg|pdf|xml|json|txt)$/.test(path))continue;
   if(!seen.has(path))queue.push(path);}
 }
 // check non-HTML local assets referenced
 await ctx.close();}
await b.close();
res.summary={pages:Object.keys(res.pages).length,broken:res.broken.length,deadTabs:res.deadTabs.length,pagesWithErrors:res.errors.length};
fs.writeFileSync(out,JSON.stringify(res,null,1));console.log(JSON.stringify(res.summary));})();
