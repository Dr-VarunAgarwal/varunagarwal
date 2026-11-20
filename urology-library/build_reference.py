"""Build the personal reference centre: drugs and prices, procedure cost estimator,
devices, companies and contacts, as one self-contained HTML page.

Run:  python3 urology-library/build_reference.py
Output: urology-library/reference/index.html  (open in a browser, works offline)
"""
import csv, json, os, re

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
    "gaps": load("gaps.csv"),
    "classification": load("classification.csv"),
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
ICON_DIR = os.path.join(HERE, "reference", "assets", "tabler-icons")

def icon_inner(name):
    """Return the inner SVG markup of a Tabler outline icon (MIT, see assets README)."""
    path = os.path.join(ICON_DIR, name + ".svg")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    inner = src[src.index(">", src.index("<svg")) + 1 : src.rindex("</svg>")]
    return inner.strip()

def icon_html(name, cls="ic"):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, icon_inner(name)))

def fill_icons(html):
    return re.sub(r"\[\[icon:([a-z-]+)\]\]", lambda m: icon_html(m.group(1)), html)


HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Urology Reference Centre</title>
<style>
:root{
  --paper:#f3f7f7; --card:#ffffff; --ink:#0f2a2e; --muted:#5b7477; --line:#d6e3e4;
  --accent:#0b6f7a; --accent-soft:#e2f1f2; --gold:#2f8f86; --warn:#b8641c; --ok:#17825a; --shadow:0 1px 2px rgba(15,42,46,.05),0 10px 30px rgba(15,42,46,.06);
  --sans:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; --serif:var(--sans); --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){ --paper:#0b1517; --card:#102023; --ink:#dff3f2; --muted:#8fb3b3; --line:#1d3a3e;
    --accent:#5fd0cc; --accent-soft:#12333a; --gold:#7fd9c9; --warn:#f0a35c; --ok:#6fe0a6; --shadow:none; }
}
:root[data-theme="dark"]{ --paper:#0b1517; --card:#102023; --ink:#dff3f2; --muted:#8fb3b3; --line:#1d3a3e;
  --accent:#5fd0cc; --accent-soft:#12333a; --gold:#7fd9c9; --warn:#f0a35c; --ok:#6fe0a6; --shadow:none; }
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 var(--sans)}
.wrap{min-height:100vh}
.bar{position:sticky;top:0;z-index:8;background:color-mix(in srgb,var(--card) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar-in{display:flex;align-items:center;gap:14px;max-width:1180px;margin:0 auto;padding:10px clamp(14px,3vw,30px)}
.brand-s{display:flex;align-items:center;gap:8px;font:600 14px var(--sans);text-transform:uppercase;letter-spacing:.1em;white-space:nowrap}
.brand-s .ic{width:18px;height:18px;color:var(--accent)}
.bar nav{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;flex:1;min-width:0}
.bar nav::-webkit-scrollbar{display:none}
.bar nav button{display:flex;align-items:center;gap:6px;border:0;background:none;color:var(--muted);padding:7px 10px;border-radius:999px;cursor:pointer;font:500 13px var(--sans);white-space:nowrap}
.bar nav button:hover{color:var(--ink);background:var(--accent-soft)}
.bar nav button.on{color:var(--accent);background:var(--accent-soft);font-weight:600}
.bar nav .ic{width:16px;height:16px;flex:0 0 16px;color:currentColor}
.bar nav .n{font:600 10px var(--mono);color:var(--muted);background:var(--paper);border-radius:999px;padding:1px 6px;font-style:normal}
.bar-tools{display:flex;gap:6px;flex:0 0 auto}
.iconbtn{width:36px;height:36px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);display:grid;place-items:center;cursor:pointer}
.iconbtn .ic{width:18px;height:18px}
.iconbtn:hover{border-color:var(--accent);color:var(--accent)}
.setg{padding:12px 0;border-top:1px solid var(--line)}
.setl{font:600 12px var(--sans);text-transform:uppercase;letter-spacing:.1em;color:var(--accent);margin-bottom:8px}
.seg{display:flex;gap:6px;flex-wrap:wrap}
.opt{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:6px 12px;cursor:pointer}
.opt:has(input:checked){background:var(--accent);color:#fff;border-color:var(--accent)}
.opt input{accent-color:var(--accent)}
.tog{display:flex;gap:8px;align-items:center;cursor:pointer}
.tog input{accent-color:var(--accent);width:16px;height:16px}
body.large{font-size:17px}
body.hide-pii .pii{display:none!important}

.tag{color:var(--muted);font-size:12px;margin-bottom:22px}
nav button{display:flex;width:100%;text-align:left;gap:10px;align-items:center;border:0;background:none;color:var(--ink);padding:9px 10px;border-radius:8px;cursor:pointer;font:inherit}
nav button:hover{background:var(--accent-soft)}
nav button.on{background:var(--accent);color:#fff;box-shadow:0 0 0 1px var(--accent)}
nav .n{margin-left:auto;font-size:12px;opacity:.7}
main{padding:26px clamp(14px,4vw,48px) 60px;max-width:1180px;margin:0 auto;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:44px 44px;background-position:-1px -1px;background-blend-mode:normal}
main>*{position:relative}
header.top{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:22px}
h1{font:600 26px/1.15 var(--sans);margin:0;letter-spacing:-.01em}
h2{font:600 13px/1.3 var(--sans);margin:26px 0 10px;text-transform:uppercase;letter-spacing:.12em;color:var(--accent)}
.lead{color:var(--muted);margin:4px 0 0}
.search{flex:1;min-width:220px;display:flex;gap:8px;margin-left:auto}
.search input{flex:1;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);font:inherit}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px}
button.btn{border:1px solid var(--line);background:var(--card);color:var(--ink);padding:9px 14px;border-radius:999px;cursor:pointer;font:inherit}
button.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.card .k{font:600 11px var(--sans);color:var(--gold);text-transform:uppercase;letter-spacing:.12em}
.card h3{font:600 16px/1.3 var(--sans);margin:4px 0 6px}
.card p{margin:6px 0 0;color:var(--muted);font-size:14px}
.stat b{display:block;font:600 28px var(--mono);color:var(--accent)}
.stat span{color:var(--muted);font-size:13px}
.pill{display:inline-block;font-size:11px;padding:2px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted);margin-right:4px;white-space:nowrap}
.pill.web-verified{color:var(--ok);border-color:var(--ok)}.pill.unverified{color:var(--warn);border-color:var(--warn)}
.pill.from-source{color:var(--accent);border-color:var(--accent)}
table{width:100%;border-collapse:separate;border-spacing:0;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}
th{font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);background:var(--accent-soft);cursor:pointer;position:sticky;top:0;font-weight:600}
tr:last-child td{border-bottom:0}
tr.row{cursor:pointer}tr.row:hover td{background:var(--accent-soft)}
td.num{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.est{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow);margin-bottom:18px}
.est h3{font:600 17px var(--sans);margin:0 0 4px}
.fields{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin:12px 0}
.fields label{font-size:12px;color:var(--muted);display:block;margin-bottom:3px}
.fields input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);font:inherit}
.result{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
.result div{background:var(--accent-soft);padding:12px 16px;border-radius:12px;min-width:170px}
.result b{display:block;font:600 20px var(--mono);color:var(--accent)}
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
.tray{position:fixed;left:50%;bottom:18px;transform:translate(-50%,140%);display:flex;gap:12px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 10px 8px 18px;box-shadow:0 12px 40px rgba(0,0,0,.18);transition:transform .25s ease;z-index:7}
.tray.show{transform:translate(-50%,0)}
.tablewrap{overflow-x:auto;border-radius:14px}
table.cmp td.lab{font:600 11px var(--sans);text-transform:uppercase;letter-spacing:.1em;color:var(--accent);white-space:nowrap;width:150px}
table.cmp th{min-width:200px;text-transform:none;letter-spacing:0;font-size:13px;color:var(--ink)}
input[type=checkbox]{accent-color:var(--accent);width:16px;height:16px}
.hero{display:flex;align-items:center;justify-content:space-between;gap:20px;background:linear-gradient(120deg,var(--accent-soft),var(--card) 70%);border:1px solid var(--line);border-radius:16px;padding:22px 26px;margin-bottom:18px;box-shadow:var(--shadow);overflow:hidden}

.ic{width:18px;height:18px;flex:0 0 18px;vertical-align:-4px;color:var(--accent)}
nav button .ic{color:inherit;opacity:.9;width:17px;height:17px;flex:0 0 17px}
.card .k .ic{width:14px;height:14px;flex:0 0 14px;vertical-align:-2px;margin-right:2px}
.card.stat .ic{width:22px;height:22px;margin-bottom:6px;color:var(--gold)}
.brand .ic{width:20px;height:20px;vertical-align:-4px;color:var(--accent)}
@media print{.bar,.search,.noprint{display:none!important}main{padding:0}body{background:#fff;color:#000}.card,table,.est{box-shadow:none}}
</style></head>
<body>
<div class="wrap">
  <header class="bar noprint">
    <div class="bar-in">
      <div class="brand-s">[[icon:medical-cross]]<span>Urology Reference</span></div>
      <nav id="nav">
        <button data-v="home" class="on" title="Overview">[[icon:heartbeat]]<span>Overview</span></button>
        <button data-v="drugs" title="Drugs and prices">[[icon:pill]]<span>Drugs</span><i class="n" id="nDrugs"></i></button>
        <button data-v="procs" title="Procedure costs">[[icon:report-medical]]<span>Procedures</span><i class="n" id="nProcs"></i></button>
        <button data-v="devices" title="Devices">[[icon:microscope]]<span>Devices</span><i class="n" id="nDev"></i></button>
        <button data-v="companies" title="Companies">[[icon:hospital]]<span>Companies</span><i class="n" id="nCo"></i></button>
        <button data-v="groups" title="Group by generic or type">[[icon:sitemap]]<span>Groups</span></button>
      <button data-v="compare" title="Compare selected items">[[icon:git-compare]]<span>Compare</span><i class="n" id="nCmp"></i></button>
      <button data-v="gaps" title="Gaps">[[icon:checklist]]<span>Gaps</span><i class="n" id="nGap"></i></button>
      <button data-v="contacts" title="Contacts">[[icon:nurse]]<span>Contacts</span><i class="n" id="nCt"></i></button>
      </nav>
      <div class="bar-tools">
        <button class="iconbtn" id="modeBtn" title="Day or night" aria-label="Switch day or night">[[icon:sun]]</button>
        <button class="iconbtn" id="setBtn" title="Settings" aria-label="Settings">[[icon:settings]]</button>
      </div>
    </div>
  </header>
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
    <section id="v-groups" class="hidden"></section>
    <section id="v-compare" class="hidden"></section>
    <section id="v-gaps" class="hidden"></section>
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
const PAGES = {home:'Overview', drugs:'Drugs & prices', procs:'Procedure costs', devices:'Devices', companies:'Companies', gaps:'Gaps in the database', groups:'Group and compare', compare:'Compare', contacts:'Contacts'};
let view = 'home';

function show(v){
  view = v;
  document.querySelectorAll('#nav button').forEach(b => b.classList.toggle('on', b.dataset.v === v));
  ['home','drugs','procs','devices','companies','groups','compare','gaps','contacts'].forEach(x => $('v-'+x).classList.toggle('hidden', x !== v));
  $('title').textContent = PAGES[v];
  render(v);
}

function render(v){
  if(v==='home') renderHome();
  if(v==='drugs') renderDrugs();
  if(v==='procs') renderProcs();
  if(v==='devices') renderDevices();
  if(v==='companies') renderCompanies();
  if(v==='groups') renderGroups();
  if(v==='compare') renderCompare();
  if(v==='gaps') renderGaps();
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
    <div class="hero">
      <div><div class="k">Urology · Operating theatre</div><h2 style="margin:6px 0 4px;font-size:22px;text-transform:none;letter-spacing:0;color:var(--ink)">Drugs, devices and costs, in one place</h2>
      <p class="lead">Rep quotes, web checks and procedure estimates for your urology work.</p></div>
      </div>
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(170px,1fr));margin-bottom:8px">
      <div class="card stat">[[icon:pill]]<b>${drugs.length}</b><span>drugs</span></div>
      <div class="card stat">[[icon:microscope]]<b>${devices.length}</b><span>devices &amp; other items</span></div>
      <div class="card stat">[[icon:report-medical]]<b>${D.procedures.length}</b><span>procedures costed</span></div>
      <div class="card stat">[[icon:droplet]]<b>${priced}</b><span>price points</span></div>
      <div class="card stat">[[icon:hospital]]<b>${cos}</b><span>companies</span></div>
      <div class="card stat">[[icon:nurse]]<b>${ppl}</b><span>contacts</span></div>
    </div>
    <h2>Quick start</h2>
    <div class="grid">
      <div class="card" style="cursor:pointer" onclick="show('drugs')"><div class="k">[[icon:pill]] Reference</div><h3>Drugs &amp; prices</h3><p>Rep quotes next to web retail prices, with the basis for each.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('procs')"><div class="k">[[icon:report-medical]] Estimate</div><h3>Procedure costs</h3><p>Adjust device cost, units and margin to estimate what a patient pays.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('devices')"><div class="k">[[icon:microscope]] Catalogue</div><h3>Devices</h3><p>Lasers, ureteroscopes, sheaths, stones, urodynamics and more.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('companies')"><div class="k">[[icon:hospital]] Vendors</div><h3>Companies</h3><p>Who makes or distributes what, and where to reach them.</p></div>
      <div class="card" style="cursor:pointer" onclick="show('contacts')"><div class="k">[[icon:nurse]] People</div><h3>Contacts</h3><p>Every rep and manager you have met, with direct lines.</p></div>
    </div>
    <p class="note">Prices are rep quotes or web retail listings and change often. Check the basis shown before quoting a patient.</p>`;
}

function cardDrug(p){
  const pr = D.pricing.filter(x => x.product_id === p.id);
  const best = pr[0];
  return `<div class="card" style="cursor:pointer" onclick="openItem('${esc(p.id)}')">
    <div class="k">[[icon:pill]] ${esc(p.manufacturer_company)}</div><h3>${esc(p.name)}</h3>
    <p>${esc((p.use_indication||'').slice(0,110))}</p>
    <p style="margin-top:10px">${best ? `<b style="color:var(--accent)">${inr(best.price_inr)}</b> <span class="note">${esc(best.price_note||'')}</span>` : '<span class="note">No price yet</span>'}</p>
    <div style="margin-top:8px">${pill(p.verification_status)}</div></div>`;
}
function cardDevice(p){
  return `<div class="card" style="cursor:pointer" onclick="openItem('${esc(p.id)}')">
    <div class="k">[[icon:microscope]] ${esc(p.category)} · ${esc(p.manufacturer_company)}</div><h3>${esc(p.name)}</h3>
    <p>${esc((p.use_indication||'').slice(0,120))}</p><div style="margin-top:8px">${pill(p.verification_status)}</div></div>`;
}
function cardCo(m){
  const n = D.products.filter(p => (p.manufacturer_company||'').toLowerCase().slice(0,10) === (m.name||'').toLowerCase().slice(0,10)).length;
  return `<div class="card" style="cursor:pointer" onclick="openCo('${esc(m.id)}')">
    <div class="k">[[icon:hospital]] ${esc(m.type)}</div><h3>${esc(m.name)}</h3>
    <p>${esc([m.city,m.country].filter(Boolean).join(', '))}</p>
    <p>${esc((m.product_categories||'').slice(0,110))}</p>
    <div style="margin-top:8px">${pill(m.verification_status)} <span class="note">${n} product${n===1?'':'s'}</span></div></div>`;
}
function cardPerson(c){
  return `<div class="card"><div class="k">${esc(c.organization)}</div><h3>${esc(c.person_name||'(name not on card)')}</h3>
    <p>${esc(c.role_title)}</p><p class="pii">${esc(c.phone)}</p><p class="pii">${esc(c.email)}</p></div>`;
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

// ---- grouping and comparison ----
const CMP = new Set();
let groupMode = 'generic';
const byId = id => D.products.find(p => p.id === id);
const priceRange = id => {
  const pr = D.pricing.filter(x => x.product_id === id).map(x => +x.price_inr).filter(n => !isNaN(n));
  if(!pr.length) return null;
  return {min: Math.min(...pr), max: Math.max(...pr), n: pr.length};
};
const priceText = id => {
  const r = priceRange(id); if(!r) return '–';
  return r.min === r.max ? inr(r.min) : `${inr(r.min)} – ${inr(r.max)}`;
};
function groupsOf(kind){
  const map = {};
  D.classification.filter(c => kind === 'generic' ? c.group_kind === 'generic' : c.group_kind === 'device_type')
    .forEach(c => { (map[c.group_name] = map[c.group_name] || []).push(c.product_id); });
  return Object.entries(map).map(([name, ids]) => ({name, items: ids.map(byId).filter(Boolean)}))
    .sort((a,b) => a.name.localeCompare(b.name));
}
function toggleCmp(id, on){
  if(on === undefined) on = !CMP.has(id);
  on ? CMP.add(id) : CMP.delete(id);
  updateTray();
}
window.toggleCmp = toggleCmp;
function updateTray(){
  $('nCmp').textContent = CMP.size ? CMP.size : '';
  let t = $('tray');
  if(!t){ t = document.createElement('div'); t.id = 'tray'; t.className = 'tray noprint'; document.body.appendChild(t); }
  t.classList.toggle('show', CMP.size > 0);
  t.innerHTML = `<span><b>${CMP.size}</b> selected</span>
    <button class="btn primary" onclick="show('compare')">Compare</button>
    <button class="btn" onclick="CMP.clear();updateTray();if(view==='compare'||view==='groups')render(view)">Clear</button>`;
}
function renderGroups(){
  $('sub').textContent = groupMode === 'generic'
    ? 'Drugs grouped by active ingredient. Tick items to compare them across vendors.'
    : 'Devices grouped by type. Tick items to compare them across vendors.';
  const seg = `<div class="seg" style="margin-bottom:14px"><button class="btn ${groupMode==='generic'?'primary':''}" onclick="groupMode='generic';renderGroups()">Drugs by generic</button><button class="btn ${groupMode==='device'?'primary':''}" onclick="groupMode='device';renderGroups()">Devices by type</button></div>`;
  const groups = groupsOf(groupMode).filter(g => hit({name:g.name}, ['name']) || g.items.some(p => hit(p,['name','manufacturer_company','use_indication'])));
  const body = groups.map(g => {
    const items = g.items.filter(p => hit(p,['name','manufacturer_company','use_indication','notes']) || hit({name:g.name},['name']));
    return `<h2>${esc(g.name)} <span class="note">· ${items.length} vendor${items.length===1?'':'s'}</span></h2>
    <table><tr><th style="width:36px"></th><th>Product</th><th>Company</th><th class="num">Price</th><th>Status</th></tr>
    ${items.map(p => `<tr class="row"><td><input type="checkbox" ${CMP.has(p.id)?'checked':''} onclick="event.stopPropagation();toggleCmp('${esc(p.id)}',this.checked)"></td>
      <td onclick="openItem('${esc(p.id)}')"><b>${esc(p.name)}</b></td><td>${esc(p.manufacturer_company)}</td>
      <td class="num">${priceText(p.id)}</td><td>${pill(p.verification_status)}</td></tr>`).join('')}
    </table>`;
  }).join('');
  $('v-groups').innerHTML = seg + (body || '<p class="lead">Nothing matches.</p>');
}
function renderCompare(){
  const items = [...CMP].map(byId).filter(Boolean);
  $('sub').textContent = items.length ? `${items.length} item${items.length===1?'':'s'} side by side.` : 'Nothing selected yet.';
  if(!items.length){ $('v-compare').innerHTML = '<p class="lead">Tick items in Groups or Drugs to compare them here.</p>'; return; }
  const rows = [
    ['Company', p => esc(p.manufacturer_company)],
    ['Category', p => esc(p.category)],
    ['Use / indication', p => esc(p.use_indication)],
    ['Key specs', p => esc(p.key_specs)],
    ['Price (rep quote and web)', p => priceText(p.id) + (priceRange(p.id) && priceRange(p.id).n>1 ? '<div class="note">' + D.pricing.filter(x=>x.product_id===p.id).map(x=>`${esc(x.price_note||x.pack)}: ${inr(x.price_inr)}`).join('<br>') + '</div>' : '')],
    ['Regulatory (as found)', p => esc(p.regulatory_status)],
    ['Status', p => pill(p.verification_status)],
    ['Notes', p => esc(p.notes)],
  ];
  $('v-compare').innerHTML = `<div class="tablewrap"><table class="cmp"><tr><th></th>${items.map(p=>`<th><a href="#" onclick="openItem('${esc(p.id)}');return false">${esc(p.name)}</a><div><button class="btn" style="padding:3px 8px;font-size:11px" onclick="toggleCmp('${esc(p.id)}',false);renderCompare()">Remove</button></div></th>`).join('')}</tr>
    ${rows.map(([l,f]) => `<tr><td class="lab">${l}</td>${items.map(p=>`<td>${f(p)}</td>`).join('')}</tr>`).join('')}</table></div>`;
}

function renderGaps(){
  const G = D.gaps;
  const rows = G.filter(g => hit(g,['system','item','examples_india','kind']));
  const have = G.filter(g=>g.status==='have').length, gap = G.filter(g=>g.status==='gap').length;
  $('sub').textContent = `${have} of ${G.length} core items covered. ${gap} gaps to fill, ordered by system.`;
  const systems = [...new Set(rows.map(g=>g.system))];
  $('v-gaps').innerHTML = `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(180px,1fr));margin-bottom:6px">
      <div class="card stat"><b>${G.length}</b><span>core items checked</span></div>
      <div class="card stat"><b style="color:var(--ok)">${have}</b><span>covered in your database</span></div>
      <div class="card stat"><b style="color:var(--warn)">${gap}</b><span>gaps</span></div></div>`
    + systems.map(sys => {
        const items = rows.filter(g=>g.system===sys);
        const sg = items.filter(g=>g.status==='gap').length;
        return `<h2>${esc(sys)} <span class="note">· ${items.length-sg}/${items.length} covered</span></h2>
        <table><tr><th>Item</th><th>Type</th><th>Examples found online</th><th>Priority</th><th>Status</th></tr>
        ${items.map(g=>`<tr><td><b>${esc(g.item)}</b></td><td>${esc(g.kind)}</td><td>${esc(g.examples_india)}</td><td>${esc(g.priority)}</td><td>${g.status==='have'?'<span class="pill web-verified">covered</span>':'<span class="pill unverified">gap</span>'}</td></tr>`).join('')}
        </table>`;}).join('') || '<p class="lead">Nothing matches.</p>';
}

function renderContacts(){
  const rows = D.contacts.filter(c => hit(c,['person_name','organization','role_title','notes','email','phone']));
  $('sub').textContent = `${rows.length} contact${rows.length===1?'':'s'}. Phone and email are stored locally.`;
  $('v-contacts').innerHTML = `<table><tr><th>Name</th><th>Role</th><th>Organisation</th><th>Phone</th><th>Email</th></tr>
    ${rows.map(c=>`<tr><td><b>${esc(c.person_name||'—')}</b></td><td>${esc(c.role_title)}</td><td>${esc(c.organization)}</td><td class="pii">${esc(c.phone)}</td><td class="pii">${esc(c.email)}</td></tr>`).join('')}</table>`;
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
    <h3 style="font:600 15px var(--sans);margin:16px 0 4px">People (${ppl.length})</h3>${ppl.map(c=>`<div><b>${esc(c.person_name||'(no name)')}</b> · ${esc(c.role_title)}<br><span class="pii">${esc(c.phone)} · ${esc(c.email)}</span></div>`).join('')||'<div class="note">None linked</div>'}
    <p style="margin-top:18px"><button class="btn" onclick="closeDetail()">Close</button></p>`;
  $('detail').classList.add('open');
}
function closeDetail(){ $('detail').classList.remove('open'); }
window.show = show; window.openItem = openItem; window.openCo = openCo; window.closeDetail = closeDetail;

document.querySelectorAll('#nav button').forEach(b => b.onclick = () => show(b.dataset.v));
$('q').addEventListener('input', () => render(view === 'home' || q() ? 'home' : view));
$('printBtn').onclick = () => window.print();
const KEY = 'urref-settings';
const DEFAULTS = {theme:'system', contacts:true, large:false};
function loadSettings(){ try { return Object.assign({}, DEFAULTS, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch(e) { return {...DEFAULTS}; } }
function saveSettings(st){ try { localStorage.setItem(KEY, JSON.stringify(st)); } catch(e) {} }
let settings = loadSettings();
function applySettings(){
  const r = document.documentElement;
  if (settings.theme === 'system') delete r.dataset.theme; else r.dataset.theme = settings.theme;
  document.body.classList.toggle('hide-pii', !settings.contacts);
  document.body.classList.toggle('large', !!settings.large);
  const dark = settings.theme === 'dark' || (settings.theme === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
  $('modeBtn').innerHTML = dark ? MOON : SUN;
  $('modeBtn').title = dark ? 'Switch to day' : 'Switch to night';
}
const SUN = `__SUN__`, MOON = `__MOON__`;
$('modeBtn').onclick = () => {
  const r = document.documentElement;
  const dark = r.dataset.theme === 'dark' || (!r.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
  settings.theme = dark ? 'light' : 'dark'; saveSettings(settings); applySettings();
};
function openSettings(){
  const opt = (name, val, label) => `<label class="opt"><input type="radio" name="${name}" value="${val}" ${settings[name]===val?'checked':''}> ${label}</label>`;
  $('sheet').innerHTML = `<div class="k" style="font:600 11px var(--sans);color:var(--gold);text-transform:uppercase;letter-spacing:.12em">Settings</div>
    <h2 style="margin:4px 0 14px;font-size:20px;text-transform:none;letter-spacing:0;color:var(--ink)">Appearance and display</h2>
    <div class="setg"><div class="setl">Day or night</div>
      <div class="seg">${opt('theme','system','Match device')}${opt('theme','light','Day')}${opt('theme','dark','Night')}</div></div>
    <div class="setg"><div class="setl">Contact details</div>
      <label class="tog"><input type="checkbox" id="setContacts" ${settings.contacts?'checked':''}> Show phone numbers and emails</label>
      <div class="note">Turn off to hide personal details when you share your screen.</div></div>
    <div class="setg"><div class="setl">Text size</div>
      <label class="tog"><input type="checkbox" id="setLarge" ${settings.large?'checked':''}> Larger text</label></div>
    <p style="margin-top:20px;display:flex;gap:8px;justify-content:space-between;flex-wrap:wrap">
      <button class="btn" id="setReset">Reset to defaults</button>
      <button class="btn primary" onclick="closeDetail()">Done</button></p>`;
  $('detail').classList.add('open');
  document.querySelectorAll('#sheet input[name="theme"]').forEach(i => i.onchange = () => { settings.theme = i.value; saveSettings(settings); applySettings(); });
  $('setContacts').onchange = e => { settings.contacts = e.target.checked; saveSettings(settings); applySettings(); };
  $('setLarge').onchange = e => { settings.large = e.target.checked; saveSettings(settings); applySettings(); };
  $('setReset').onclick = () => { settings = {...DEFAULTS}; saveSettings(settings); applySettings(); openSettings(); };
}
$('setBtn').onclick = openSettings;
applySettings();
matchMedia('(prefers-color-scheme: dark)').addEventListener && matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applySettings);
document.addEventListener('keydown', e => { if(e.key === 'Escape') closeDetail(); });
$('nDrugs').textContent = drugs.length; $('nDev').textContent = devices.length; $('nProcs').textContent = D.procedures.length;
$('nCo').textContent = D.manufacturers.length; updateTray(); $('nCt').textContent = D.contacts.length; $('nGap').textContent = D.gaps.filter(g=>g.status==='gap').length;
show('home');
</script></body></html>
"""

out_dir = os.path.join(HERE, "reference")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "index.html")
with open(out, "w", encoding="utf-8") as f:
    page = HTML.replace("__PAYLOAD__", payload).replace("__SUN__", icon_html("sun")).replace("__MOON__", icon_html("moon")).replace("__GEAR__", icon_html("settings"))
    f.write(fill_icons(page))
print("wrote", out, {k: len(v) for k, v in data.items()})
