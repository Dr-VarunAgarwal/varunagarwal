"""Build the personal reference centre: drugs and prices, procedure cost estimator,
devices, companies and contacts, as one self-contained HTML page.

Run:  python3 urology-library/build_reference.py
Output: urology-library/reference/index.html  (open in a browser, works offline)
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

data = {
    "products": load("library.csv"),
    "pricing": load("pricing.csv"),
    "procedures": load("procedures.csv"),
    "manufacturers": load("manufacturers.csv"),
    "contacts": load("contacts.csv"),
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Urology Reference Centre</title>
<style>
:root{
  --paper:#faf7f2; --card:#ffffff; --ink:#1f2328; --muted:#6b6f76; --line:#e7e1d6;
  --accent:#1f5f5b; --accent-soft:#e3f0ee; --gold:#b08a3e; --warn:#a8632b; --ok:#2f7a4f; --shadow:0 1px 2px rgba(31,35,40,.06),0 8px 24px rgba(31,35,40,.06);
  --serif:Georgia,"Iowan Old Style","Palatino Linotype",serif; --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){ --paper:#14171a; --card:#1d2227; --ink:#e9e6df; --muted:#9aa1a9; --line:#2c3339;
    --accent:#7fc4bd; --accent-soft:#1f3432; --gold:#d4b06a; --warn:#e0a06a; --ok:#7fcf9d; --shadow:none; }
}
:root[data-theme="dark"]{ --paper:#14171a; --card:#1d2227; --ink:#e9e6df; --muted:#9aa1a9; --line:#2c3339;
  --accent:#7fc4bd; --accent-soft:#1f3432; --gold:#d4b06a; --warn:#e0a06a; --ok:#7fcf9d; --shadow:none; }
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans)}
.wrap{display:grid;grid-template-columns:230px 1fr;min-height:100vh}
@media(max-width:860px){.wrap{grid-template-columns:1fr}aside{position:static!important;height:auto!important}}
aside{position:sticky;top:0;height:100vh;padding:26px 18px;border-right:1px solid var(--line);background:var(--card)}
.brand{font:700 20px/1.2 var(--serif);margin:0 0 4px}
.tag{color:var(--muted);font-size:12px;margin-bottom:22px}
nav button{display:flex;width:100%;text-align:left;gap:10px;align-items:center;border:0;background:none;color:var(--ink);padding:9px 10px;border-radius:8px;cursor:pointer;font:inherit}
nav button:hover{background:var(--accent-soft)}
nav button.on{background:var(--accent);color:#fff}
nav .n{margin-left:auto;font-size:12px;opacity:.7}
.side-foot{position:absolute;bottom:18px;left:18px;right:18px;font-size:12px;color:var(--muted)}
main{padding:30px clamp(18px,4vw,48px) 60px;max-width:1180px}
header.top{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:22px}
h1{font:700 30px/1.15 var(--serif);margin:0;letter-spacing:-.01em}
h2{font:600 20px/1.3 var(--serif);margin:26px 0 10px}
.lead{color:var(--muted);margin:4px 0 0}
.search{flex:1;min-width:220px;display:flex;gap:8px;margin-left:auto}
.search input{flex:1;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);font:inherit}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px}
button.btn{border:1px solid var(--line);background:var(--card);color:var(--ink);padding:9px 14px;border-radius:999px;cursor:pointer;font:inherit}
button.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;box-shadow:var(--shadow)}
.card .k{font:italic 13px var(--serif);color:var(--gold);text-transform:uppercase;letter-spacing:.08em}
.card h3{font:600 17px/1.3 var(--serif);margin:4px 0 6px}
.card p{margin:6px 0 0;color:var(--muted);font-size:14px}
.stat b{display:block;font:700 28px var(--serif);color:var(--accent)}
.stat span{color:var(--muted);font-size:13px}
.pill{display:inline-block;font-size:11px;padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted);margin-right:4px;white-space:nowrap}
.pill.web-verified{color:var(--ok);border-color:var(--ok)}.pill.unverified{color:var(--warn);border-color:var(--warn)}
.pill.from-source{color:var(--accent);border-color:var(--accent)}
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}
th{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);background:var(--accent-soft);cursor:pointer;position:sticky;top:0}
tr:last-child td{border-bottom:0}
tr.row{cursor:pointer}tr.row:hover td{background:var(--accent-soft)}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.est{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow);margin-bottom:18px}
.est h3{font:600 19px var(--serif);margin:0 0 4px}
.fields{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin:12px 0}
.fields label{font-size:12px;color:var(--muted);display:block;margin-bottom:3px}
.fields input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);font:inherit}
.result{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
.result div{background:var(--accent-soft);padding:12px 16px;border-radius:12px;min-width:170px}
.result b{display:block;font:700 22px var(--serif);color:var(--accent)}
.result span{font-size:12px;color:var(--muted)}
.note{font-size:13px;color:var(--muted);margin-top:8px}
.warn{color:var(--warn)}
.detail{position:fixed;inset:0;background:rgba(0,0,0,.35);display:none;align-items:center;justify-content:center;padding:20px;z-index:9}
.detail.open{display:flex}
.sheet{background:var(--card);color:var(--ink);max-width:640px;width:100%;max-height:86vh;overflow:auto;border-radius:18px;padding:26px;box-shadow:0 20px 60px rgba(0,0,0,.3)}
.sheet dl{display:grid;grid-template-columns:150px 1fr;gap:6px 14px;margin:14px 0 0}
.sheet dt{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.05em}
.sheet dd{margin:0;word-break:break-word}
.hidden{display:none!important}
@media print{aside,.search,.noprint{display:none!important}.wrap{display:block}main{padding:0}body{background:#fff;color:#000}.card,table,.est{box-shadow:none}}
</style></head>
<body>
<div class="wrap">
  <aside>
    <p class="brand">Urology<br>Reference Centre</p>
    <div class="tag">Personal archive · drugs, devices, costs, contacts</div>
    <nav id="nav">
      <button data-v="home" class="on">Overview</button>
      <button data-v="drugs">Drugs &amp; prices <span class="n" id="nDrugs"></span></button>
      <button data-v="procs">Procedure costs <span class="n" id="nProcs"></span></button>
      <button data-v="devices">Devices <span class="n" id="nDev"></span></button>
      <button data-v="companies">Companies <span class="n" id="nCo"></span></button>
      <button data-v="contacts">Contacts <span class="n" id="nCt"></span></button>
    </nav>
    <div class="side-foot">Private. Contains personal contact details.<br><button class="btn noprint" id="themeBtn" style="margin-top:8px;padding:5px 10px;font-size:12px">Toggle theme</button></div>
  </aside>
  <main>
    <header class="top">
      <div><h1 id="title">Overview</h1><p class="lead" id="sub"></p></div>
      <div class="search"><input id="q" type="search" placeholder="Search drugs, devices, companies, people…"></div>
      <button class="btn noprint" id="printBtn">Print</button>
    </header>
    <section id="v-home"></section>
    <section id="v-drugs" class="hidden"></section>
    <section id="v-procs" class="hidden"></section>
    <section id="v-devices" class="hidden"></section>
    <section id="v-companies" class="hidden"></section>
    <section id="v-contacts" class="hidden"></section>
  </main>
</div>
<div class="detail" id="detail" onclick="if(event.target.id==='detail')closeDetail()"><div class="sheet" id="sheet"></div></div>
<script>
const D = __PAYLOAD__;
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const inr = n => (n===''||n==null||isNaN(+n)) ? '–' : '₹' + Math.round(+n).toLocaleString('en-IN');
const lakh = n => (n===''||n==null||isNaN(+n)) ? '–' : '₹' + (+n/100000).toFixed(2).replace(/\.?0+$/,'') + ' L';
const pill = v => v ? `<span class="pill ${esc(v)}">${esc(v)}</span>` : '';
const drugs = D.products.filter(p => p.category === 'drug');
const devices = D.products.filter(p => p.category !== 'drug');
const q = () => $('q').value.trim().toLowerCase();
const hit = (o, fields) => { const s = q(); return !s || fields.map(f => o[f] || '').join(' ').toLowerCase().includes(s); };
const PAGES = {home:'Overview', drugs:'Drugs & prices', procs:'Procedure costs', devices:'Devices', companies:'Companies', contacts:'Contacts'};
let view = 'home';

function show(v){
  view = v;
  document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  ['home','drugs','procs','devices','companies','contacts'].forEach(x => $('v-'+x).classList.toggle('hidden', x !== v));
  $('title').textContent = PAGES[v];
  render(v);
}

function render(v){
  if(v==='home') renderHome();
  if(v==='drugs') renderDrugs();
  if(v==='procs') renderProcs();
  if(v==='devices') renderDevices();
  if(v==='companies') renderCompanies();
  if(v==='contacts') renderContacts();
}

function renderHome(){
  const cos = D.manufacturers.length, ppl = D.contacts.length;
  const s = q();
  if(s){
    const d = drugs.filter(p=>hit(p,['name','manufacturer_company','use_indication','notes']));
    const dv = devices.filter(p=>hit(p,['name','manufacturer_company','use_indication','notes']));
    const co = D.manufacturers.filter(m=>hit(m,['name','product_categories','notes']));
    const ct = D.contacts.filter(c=>hit(c,['person_name','organization','role_title','notes','email']));
    const cards = (arr, fn) => arr.length ? `<div class="grid">${arr.map(fn).join('')}</div>` : '<p class="lead">None.</p>';
    $('sub').textContent = `Results for “${$('q').value}”`;
    $('v-home').innerHTML = `<h2>Drugs (${d.length})</h2>${cards(d, cardDrug)}<h2>Devices (${dv.length})</h2>${cards(dv, cardDevice)}<h2>Companies (${co.length})</h2>${cards(co, cardCo)}<h2>People (${ct.length})</h2>${cards(ct, cardPerson)}`;
    return;
  }
  $('sub').textContent = 'Your archive at a glance. Use the search box to find anything.';
  const priced = D.pricing.length;
  $('v-home').innerHTML = `
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(170px,1fr));margin-bottom:8px">
      <div class="card stat"><b>${drugs.length}</b><span>drugs</span></div>
      <div class="card stat"><b>${devices.length}</b><span>devices &amp; other items</span></div>
      <div class="card stat"><b>${D.procedures.length}</b><span>procedures costed</span></div>
      <div class="card stat"><b>${priced}</b><span>price points</span></div>
      <div class="card stat"><b>${cos}</b><span>companies</span></div>
      <div class="card stat"><b>${ppl}</b><span>contacts</span></div>
    </div>
    <h2>Quick start</h2>
    <div class="grid">
      <div class="card" style="cursor:pointer" onclick="show('drugs')"><div class="k">Reference</div><h3>Drugs &amp; prices</h3><p>Rep quotes next to web retail prices, with the basis for each.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('procs')"><div class="k">Estimate</div><h3>Procedure costs</h3><p>Adjust device cost, units and margin to estimate what a patient pays.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('devices')"><div class="k">Catalogue</div><h3>Devices</h3><p>Lasers, ureteroscopes, sheaths, stones, urodynamics and more.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('companies')"><div class="k">Vendors</div><h3>Companies</h3><p>Who makes or distributes what, and where to reach them.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('contacts')"><div class="k">People</div><h3>Contacts</h3><p>Every rep and manager you have met, with direct lines.</p></div>
    </div>
    <p class="note">Prices are rep quotes or web retail listings and change often. Check the basis shown before quoting a patient.</p>`;
}

function cardDrug(p){
  const pr = D.pricing.filter(x => x.product_id === p.id);
  const best = pr[0];
  return `<div class="card" style="cursor:pointer" onclick="openItem('${esc(p.id)}')">
    <div class="k">${esc(p.manufacturer_company)}</div><h3>${esc(p.name)}</h3>
    <p>${esc((p.use_indication||'').slice(0,110))}</p>
    <p style="margin-top:10px">${best ? `<b style="color:var(--accent)">${inr(best.price_inr)}</b> <span class="note">${esc(best.price_note||'')}</span>` : '<span class="note">No price yet</span>'}</p>
    <div style="margin-top:8px">${pill(p.verification_status)}</div></div>`;
}
function cardDevice(p){
  return `<div class="card" style="cursor:pointer" onclick="openItem('${esc(p.id)}')">
    <div class="k">${esc(p.category)} · ${esc(p.manufacturer_company)}</div><h3>${esc(p.name)}</h3>
    <p>${esc((p.use_indication||'').slice(0,120))}</p><div style="margin-top:8px">${pill(p.verification_status)}</div></div>`;
}
function cardCo(m){
  const n = D.products.filter(p => (p.manufacturer_company||'').toLowerCase().slice(0,10) === (m.name||'').toLowerCase().slice(0,10)).length;
  return `<div class="card" style="cursor:pointer" onclick="openCo('${esc(m.id)}')">
    <div class="k">${esc(m.type)}</div><h3>${esc(m.name)}</h3>
    <p>${esc([m.city,m.country].filter(Boolean).join(', '))}</p>
    <p>${esc((m.product_categories||'').slice(0,110))}</p>
    <div style="margin-top:8px">${pill(m.verification_status)} <span class="note">${n} product${n===1?'':'s'}</span></div></div>`;
}
function cardPerson(c){
  return `<div class="card"><div class="k">${esc(c.organization)}</div><h3>${esc(c.person_name||'(name not on card)')}</h3>
    <p>${esc(c.role_title)}</p><p>${esc(c.phone)}</p><p>${esc(c.email)}</p></div>`;
}

function renderDrugs(){
  const rows = drugs.filter(p => hit(p,['name','manufacturer_company','use_indication','notes','product_line']));
  $('sub').textContent = `${rows.length} drug${rows.length===1?'':'s'}. Click a row for details. Prices show the basis for each figure.`;
  const pricesFor = id => D.pricing.filter(x => x.product_id === id);
  let body = '';
  rows.forEach(p => {
    const pr = pricesFor(p.id);
    if(!pr.length){
      body += `<tr class="row" onclick="openItem('${esc(p.id)}')"><td><b>${esc(p.name)}</b><div class="note">${esc(p.manufacturer_company)}</div></td><td colspan="3" class="note">No price recorded</td><td>${pill(p.verification_status)}</td></tr>`;
      return;
    }
    pr.forEach((x,i) => {
      body += `<tr class="row" onclick="openItem('${esc(p.id)}')">
        <td>${i===0?`<b>${esc(p.name)}</b><div class="note">${esc(p.manufacturer_company)}</div>`:''}</td>
        <td>${esc(x.price_note||x.pack)}</td>
        <td class="num"><b>${inr(x.price_inr)}</b></td>
        <td>${esc(x.price_type||'')}</td>
        <td>${i===0?pill(p.verification_status):''}</td></tr>`;
    });
  });
  $('v-drugs').innerHTML = `<table><tr><th>Drug</th><th>Pack / basis</th><th class="num">Price</th><th>Price type</th><th>Status</th></tr>${body || '<tr><td colspan="5">Nothing matches.</td></tr>'}</table>
    <p class="note">Rep quotes are what reps told you. Web MRP is retail. Check each before quoting a patient.</p>`;
}

function renderProcs(){
  $('sub').textContent = 'Change the inputs to estimate what a patient might pay. Figures from your notes and web sources.';
  const cards = D.procedures.map((p,i) => {
    const dev = p.device_cost_inr !== '' ? +p.device_cost_inr : 0;
    const defUnits = /UroLift/i.test(p.procedure) ? 4 : 1;
    return `<div class="est" id="est-${i}">
      <h3>${esc(p.procedure)} ${pill(p.verification_status)}</h3>
      <div class="note">${esc(p.units_note)} · Basis: ${esc(p.basis)}</div>
      <div class="fields">
        <div><label>Units (implants or guns)</label><input type="number" min="0" value="${defUnits}" data-f="units"></div>
        <div><label>Device cost per unit (₹)</label><input type="number" min="0" value="${dev}" data-f="dev"></div>
        <div><label>Other costs (₹, surgeon, stay, OT)</label><input type="number" min="0" value="0" data-f="other"></div>
        <div><label>Margin (%)</label><input type="number" min="0" value="0" data-f="margin"></div>
      </div>
      <div class="result">
        <div><b>${lakh(p.patient_total_low_inr)} – ${lakh(p.patient_total_high_inr)}</b><span>Source range (patient total)</span></div>
        <div><b data-out="calc">–</b><span>Your calculation (units × device + other, plus margin)</span></div>
      </div>
      <p class="note">${esc(p.notes)}</p>
    </div>`;
  }).join('');
  $('v-procs').innerHTML = cards || '<p class="lead">No procedures yet.</p>';
  document.querySelectorAll('#v-procs .est').forEach(card => {
    const upd = () => {
      const g = f => +(card.querySelector(`[data-f="${f}"]`).value || 0);
      const total = (g('units')*g('dev') + g('other')) * (1 + g('margin')/100);
      card.querySelector('[data-out="calc"]').textContent = inr(total);
    };
    card.querySelectorAll('input').forEach(i => i.addEventListener('input', upd)); upd();
  });
}

function renderDevices(){
  const rows = devices.filter(p => hit(p,['name','manufacturer_company','use_indication','notes','category']));
  $('sub').textContent = `${rows.length} item${rows.length===1?'':'s'}, grouped by company.`;
  const groups = {};
  rows.forEach(p => (groups[p.manufacturer_company||'Unknown'] = groups[p.manufacturer_company||'Unknown'] || []).push(p));
  $('v-devices').innerHTML = Object.keys(groups).sort().map(g => `
    <h2>${esc(g)} <span class="note">· ${groups[g].length}</span></h2>
    <div class="grid">${groups[g].map(cardDevice).join('')}</div>`).join('') || '<p class="lead">Nothing matches.</p>';
}

function renderCompanies(){
  const rows = D.manufacturers.filter(m => hit(m,['name','product_categories','notes','city','country']));
  $('sub').textContent = `${rows.length} compan${rows.length===1?'y':'ies'}. Click for details and contacts.`;
  $('v-companies').innerHTML = `<div class="grid">${rows.map(cardCo).join('')}</div>`;
}
function renderContacts(){
  const rows = D.contacts.filter(c => hit(c,['person_name','organization','role_title','notes','email','phone']));
  $('sub').textContent = `${rows.length} contact${rows.length===1?'':'s'}. Phone and email are stored locally.`;
  $('v-contacts').innerHTML = `<table><tr><th>Name</th><th>Role</th><th>Organisation</th><th>Phone</th><th>Email</th></tr>
    ${rows.map(c=>`<tr><td><b>${esc(c.person_name||'—')}</b></td><td>${esc(c.role_title)}</td><td>${esc(c.organization)}</td><td>${esc(c.phone)}</td><td>${esc(c.email)}</td></tr>`).join('')}</table>`;
}

function openItem(id){
  const p = D.products.find(x => x.id === id); if(!p) return;
  const pr = D.pricing.filter(x => x.product_id === id);
  const fields = [['Category','category'],['Company','manufacturer_company'],['Product line','product_line'],['Country','country_of_origin'],['Use / indication','use_indication'],['Key specs','key_specs'],['Regulatory (as found)','regulatory_status'],['Source link','regulatory_source'],['Notes','notes'],['Status','verification_status']];
  $('sheet').innerHTML = `<div class="k" style="font:italic 13px var(--serif);color:var(--gold);text-transform:uppercase;letter-spacing:.08em">${esc(p.id)}</div>
    <h2 style="margin:4px 0 0">${esc(p.name)}</h2>
    ${pr.length ? `<h3 style="font:600 15px var(--sans);margin:14px 0 4px">Prices</h3>${pr.map(x=>`<div>${inr(x.price_inr)} <span class="note">· ${esc(x.price_note||x.pack)} · ${esc(x.price_type||'')}</span></div>`).join('')}` : ''}
    <dl>${fields.map(([l,k])=>p[k]?`<dt>${l}</dt><dd>${/^https?:/.test(p[k])?`<a href="${esc(p[k])}" target="_blank" rel="noopener">${esc(p[k].slice(0,70))}</a>`:esc(p[k])}</dd>`:'').join('')}</dl>
    <p style="margin-top:18px"><button class="btn" onclick="closeDetail()">Close</button></p>`;
  $('detail').classList.add('open');
}
function openCo(id){
  const m = D.manufacturers.find(x => x.id === id); if(!m) return;
  const ppl = D.contacts.filter(c => (c.organization||'').toLowerCase().slice(0,10) === (m.name||'').toLowerCase().slice(0,10));
  const prods = D.products.filter(p => (p.manufacturer_company||'').toLowerCase().slice(0,10) === (m.name||'').toLowerCase().slice(0,10));
  $('sheet').innerHTML = `<div style="font:italic 13px var(--serif);color:var(--gold);text-transform:uppercase;letter-spacing:.08em">${esc(m.id)} · ${esc(m.type)}</div>
    <h2 style="margin:4px 0 0">${esc(m.name)}</h2>
    <dl><dt>Location</dt><dd>${esc([m.city,m.country].filter(Boolean).join(', '))}</dd><dt>Website</dt><dd>${esc(m.website)}</dd><dt>India presence</dt><dd>${esc(m.india_presence)}</dd><dt>Categories</dt><dd>${esc(m.product_categories)}</dd><dt>Notes</dt><dd>${esc(m.notes)}</dd></dl>
    <h3 style="font:600 15px var(--sans);margin:16px 0 4px">Products (${prods.length})</h3>${prods.map(p=>`<div><a href="#" onclick="openItem('${esc(p.id)}');return false">${esc(p.name)}</a></div>`).join('')||'<div class="note">None linked</div>'}
    <h3 style="font:600 15px var(--sans);margin:16px 0 4px">People (${ppl.length})</h3>${ppl.map(c=>`<div><b>${esc(c.person_name||'(no name)')}</b> · ${esc(c.role_title)}<br>${esc(c.phone)} · ${esc(c.email)}</div>`).join('')||'<div class="note">None linked</div>'}
    <p style="margin-top:18px"><button class="btn" onclick="closeDetail()">Close</button></p>`;
  $('detail').classList.add('open');
}
function closeDetail(){ $('detail').classList.remove('open'); }
window.show = show; window.openItem = openItem; window.openCo = openCo; window.closeDetail = closeDetail;

document.querySelectorAll('#nav button').forEach(b => b.onclick = () => show(b.dataset.v));
$('q').addEventListener('input', () => render(view === 'home' || q() ? 'home' : view));
$('printBtn').onclick = () => window.print();
$('themeBtn').onclick = () => {
  const r = document.documentElement; const dark = r.dataset.theme === 'dark' || (!r.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
  r.dataset.theme = dark ? 'light' : 'dark';
};
document.addEventListener('keydown', e => { if(e.key === 'Escape') closeDetail(); });
$('nDrugs').textContent = drugs.length; $('nDev').textContent = devices.length; $('nProcs').textContent = D.procedures.length;
$('nCo').textContent = D.manufacturers.length; $('nCt').textContent = D.contacts.length;
show('home');
</script></body></html>
"""

out_dir = os.path.join(HERE, "reference")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML.replace("__PAYLOAD__", payload))
print("wrote", out, {k: len(v) for k, v in data.items()})
