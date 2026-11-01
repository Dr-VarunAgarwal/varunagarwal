"""Build a self-contained, navigable HTML dashboard from the CSV files in this folder.

Run from anywhere:  python3 urology-library/build_dashboard.py
Output: urology-library/dashboard/index.html  (open in a browser; no server needed)
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    with open(os.path.join(HERE, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

data = {
    "products": load("library.csv"),
    "manufacturers": load("manufacturers.csv"),
    "contacts": load("contacts.csv"),
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Urology Resource Library</title>
<style>
:root{--ink:#1d2733;--muted:#66727f;--line:#e3e8ee;--bg:#f6f8fb;--card:#fff;--accent:#2b6cb0;
--ok:#2f855a;--warn:#b7791f;--bad:#a0aec0}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
header{background:#fff;border-bottom:1px solid var(--line);padding:14px 22px;position:sticky;top:0;z-index:5}
h1{font-size:18px;margin:0 0 8px}
nav.tabs{display:flex;gap:6px;flex-wrap:wrap}
nav.tabs button{border:1px solid var(--line);background:#fff;padding:6px 12px;border-radius:999px;cursor:pointer;font:inherit}
nav.tabs button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:center}
.toolbar input,.toolbar select{padding:6px 9px;border:1px solid var(--line);border-radius:6px;font:inherit;background:#fff}
.toolbar input{min-width:240px}
main{padding:18px 22px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-bottom:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.card b{display:block;font-size:22px}.card span{color:var(--muted);font-size:12px}
.bars{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin-bottom:16px}
.bar{display:grid;grid-template-columns:150px 1fr 40px;gap:8px;align-items:center;margin:5px 0;cursor:pointer}
.bar .track{background:#edf2f7;border-radius:4px;height:10px;overflow:hidden}
.bar .fill{height:100%;background:var(--accent)}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:16px}
@media(max-width:1000px){.layout{grid-template-columns:1fr}}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{text-align:left;padding:8px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f0f4f9;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);cursor:pointer;position:sticky;top:0}
tr.row{cursor:pointer}tr.row:hover{background:#f5f9ff}tr.sel{background:#e6f0fb}
.pill{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.pill.web-verified{color:var(--ok);border-color:#9ae6b4}.pill.from-source{color:var(--accent);border-color:#bee3f8}
.pill.unverified{color:var(--warn);border-color:#fbd38d}
aside{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;position:sticky;top:120px;max-height:calc(100vh - 140px);overflow:auto}
aside h2{font-size:16px;margin:0 0 6px}aside dl{display:grid;grid-template-columns:110px 1fr;gap:4px 10px;margin:8px 0 0}
aside dt{color:var(--muted);font-size:12px}aside dd{margin:0;word-break:break-word}
.hint{color:var(--muted);font-size:13px}
.cmp label{display:inline-flex;gap:4px;align-items:center;margin-right:8px;font-size:12px;color:var(--muted)}
.cmpbar{margin:10px 0;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
button.btn{border:1px solid var(--accent);background:#fff;color:var(--accent);padding:5px 10px;border-radius:6px;cursor:pointer;font:inherit}
.compare{overflow:auto}
.compare td:first-child{color:var(--muted);font-size:12px;white-space:nowrap;width:130px}
a{color:var(--accent)}
</style></head>
<body>
<header>
  <h1>Urology Resource Library</h1>
  <nav class="tabs" id="tabs">
    <button data-tab="overview" class="on">Overview</button>
    <button data-tab="products">Products</button>
    <button data-tab="compare">Compare</button>
    <button data-tab="manufacturers">Manufacturers</button>
    <button data-tab="contacts">Contacts</button>
  </nav>
  <div class="toolbar" id="toolbar">
    <input id="q" type="search" placeholder="Search name, company, use, notes...">
    <select id="fCat"><option value="">All categories</option></select>
    <select id="fVer"><option value="">Any verification</option><option>web-verified</option><option>from-source</option><option>unverified</option></select>
    <select id="fCo"><option value="">All companies</option></select>
    <span class="hint" id="count"></span>
  </div>
</header>
<main>
  <section id="view-overview"></section>
  <section id="view-products" hidden>
    <div class="layout">
      <div><table id="tProducts"></table></div>
      <aside id="detail"><h2>Select a product</h2><p class="hint">Click a row to see its details, source and verification notes.</p></aside>
    </div>
  </section>
  <section id="view-compare" hidden>
    <div class="cmpbar"><span class="hint">Tick products in the Products tab (or here), then compare side by side.</span>
      <button class="btn" id="clearCmp">Clear selection</button></div>
    <div id="cmpArea" class="compare"></div>
  </section>
  <section id="view-manufacturers" hidden>
    <div class="layout">
      <div><table id="tMakers"></table></div>
      <aside id="makerDetail"><h2>Select a company</h2><p class="hint">Click a row to see contact and product details.</p></aside>
    </div>
  </section>
  <section id="view-contacts" hidden><table id="tContacts"></table></section>
</main>
<script>
const DATA = __PAYLOAD__;
const state = {tab:'overview', sort:{}, cmp:new Set(), sel:null, selMaker:null};
const $ = id => document.getElementById(id);
const esc = s => String(s??'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const cats = [...new Set(DATA.products.map(p=>p.category))].sort();
const cos = [...new Set(DATA.products.map(p=>p.manufacturer_company))].filter(Boolean).sort();
cats.forEach(c=>$('fCat').insertAdjacentHTML('beforeend',`<option>${esc(c)}</option>`));
cos.forEach(c=>$('fCo').insertAdjacentHTML('beforeend',`<option>${esc(c)}</option>`));

function match(row, fields){
  const q=$('q').value.trim().toLowerCase();
  if(q && !fields.map(f=>row[f]||'').join(' ').toLowerCase().includes(q)) return false;
  return true;
}
function filteredProducts(){
  return DATA.products.filter(p=>match(p,['name','manufacturer_company','product_line','use_indication','notes','key_specs'])
    && (!$('fCat').value || p.category===$('fCat').value)
    && (!$('fVer').value || p.verification_status===$('fVer').value)
    && (!$('fCo').value || p.manufacturer_company===$('fCo').value));
}
function sortRows(rows, key){
  const dir = state.sort[key]==='asc'?-1:1; state.sort[key] = dir===1?'asc':'desc';
  return rows;
}
function sortBy(rows, col, tab){
  const k=tab+':'+col; const asc = state.sort[k]!=='asc'; state.sort[k]=asc?'asc':'desc';
  return [...rows].sort((a,b)=>String(a[col]||'').localeCompare(String(b[col]||''),undefined,{numeric:true}) * (asc?1:-1));
}
function pill(v){ return `<span class="pill ${esc(v)}">${esc(v||'')}</span>`; }

function renderOverview(){
  const P=DATA.products, M=DATA.manufacturers, C=DATA.contacts;
  const byCat={}; P.forEach(p=>byCat[p.category]=(byCat[p.category]||0)+1);
  const byVer={}; P.forEach(p=>byVer[p.verification_status]=(byVer[p.verification_status]||0)+1);
  const max=Math.max(...Object.values(byCat),1);
  const bars = Object.entries(byCat).sort((a,b)=>b[1]-a[1]).map(([k,v])=>
    `<div class="bar" data-cat="${esc(k)}"><span>${esc(k)}</span><div class="track"><div class="fill" style="width:${v/max*100}%"></div></div><b>${v}</b></div>`).join('');
  const verBars = Object.entries(byVer).map(([k,v])=>`<div>${pill(k)} ${v}</div>`).join('');
  $('view-overview').innerHTML = `
    <div class="cards">
      <div class="card"><b>${P.length}</b><span>products and items</span></div>
      <div class="card"><b>${M.length}</b><span>manufacturers and distributors</span></div>
      <div class="card"><b>${C.length}</b><span>contacts</span></div>
      <div class="card"><b>${cats.length}</b><span>categories</span></div>
    </div>
    <div class="bars"><b>By category</b> <span class="hint">(click a bar to filter)</span>${bars}</div>
    <div class="bars"><b>Verification status</b><div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:6px">${verBars}</div>
      <p class="hint" style="margin:10px 0 0">unverified = from a brochure or listing only; check before relying on it.</p></div>`;
  $('view-overview').querySelectorAll('.bar').forEach(el=>el.onclick=()=>{ $('fCat').value=el.dataset.cat; show('products'); });
}

function renderProducts(){
  const rows = filteredProducts();
  $('count').textContent = rows.length+' of '+DATA.products.length+' items';
  const cols=[['name','Product'],['category','Category'],['manufacturer_company','Company'],['use_indication','Use'],['verification_status','Status']];
  $('tProducts').innerHTML = `<tr><th></th>${cols.map(([c,l])=>`<th data-col="${c}">${l}</th>`).join('')}</tr>` +
    rows.map(p=>`<tr class="row ${state.sel===p.id?'sel':''}" data-id="${esc(p.id)}">
      <td><input type="checkbox" class="cmpbox" data-id="${esc(p.id)}" ${state.cmp.has(p.id)?'checked':''}></td>
      <td><b>${esc(p.name)}</b></td><td>${esc(p.category)}</td><td>${esc(p.manufacturer_company)}</td>
      <td>${esc(p.use_indication).slice(0,140)}</td><td>${pill(p.verification_status)}</td></tr>`).join('');
  $('tProducts').querySelectorAll('th[data-col]').forEach(th=>th.onclick=()=>{
    const sorted=sortBy(rows, th.dataset.col, 'p'); renderTableRows(sorted);});
  $('tProducts').querySelectorAll('tr.row').forEach(tr=>tr.onclick=e=>{
    if(e.target.classList.contains('cmpbox')) return;
    state.sel=tr.dataset.id; showDetail(tr.dataset.id); renderProducts();});
  $('tProducts').querySelectorAll('.cmpbox').forEach(cb=>cb.onchange=()=>{
    cb.checked?state.cmp.add(cb.dataset.id):state.cmp.delete(cb.dataset.id); $('count').textContent+=` · ${state.cmp.size} to compare`;});
}
function renderTableRows(rows){ // used for sorting
  const cols=[['name','Product'],['category','Category'],['manufacturer_company','Company'],['use_indication','Use'],['verification_status','Status']];
  const head = $('tProducts').querySelector('tr').outerHTML;
  $('tProducts').innerHTML = head + rows.map(p=>`<tr class="row ${state.sel===p.id?'sel':''}" data-id="${esc(p.id)}">
      <td><input type="checkbox" class="cmpbox" data-id="${esc(p.id)}" ${state.cmp.has(p.id)?'checked':''}></td>
      <td><b>${esc(p.name)}</b></td><td>${esc(p.category)}</td><td>${esc(p.manufacturer_company)}</td>
      <td>${esc(p.use_indication).slice(0,140)}</td><td>${pill(p.verification_status)}</td></tr>`).join('');
  $('tProducts').querySelectorAll('th[data-col]').forEach(th=>th.onclick=()=>renderTableRows(sortBy(rows, th.dataset.col,'p')));
  $('tProducts').querySelectorAll('tr.row').forEach(tr=>tr.onclick=e=>{ if(e.target.classList.contains('cmpbox')) return;
    state.sel=tr.dataset.id; showDetail(tr.dataset.id); renderTableRows(rows);});
  $('tProducts').querySelectorAll('.cmpbox').forEach(cb=>cb.onchange=()=>{cb.checked?state.cmp.add(cb.dataset.id):state.cmp.delete(cb.dataset.id);});
}
const FIELDS=[['category','Category'],['product_line','Product line'],['manufacturer_company','Company'],['country_of_origin','Country'],['use_indication','Use / indication'],['key_specs','Key specs'],['regulatory_status','Regulatory (as found)'],['regulatory_source','Source link'],['source_type','Source type'],['source_ref','Source ref'],['date_scanned','Date added'],['verification_status','Verification'],['notes','Notes']];
function showDetail(id){
  const p=DATA.products.find(x=>x.id===id); if(!p) return;
  const co=DATA.manufacturers.find(m=>m.name && m.name.toLowerCase().includes((p.manufacturer_company||'').toLowerCase().slice(0,12)));
  $('detail').innerHTML = `<h2>${esc(p.name)}</h2><div>${pill(p.verification_status)} <span class="hint">${esc(p.id)}</span></div>
    <dl>${FIELDS.map(([k,l])=>p[k]?`<dt>${l}</dt><dd>${/^https?:/.test(p[k])?`<a href="${esc(p[k])}" target="_blank" rel="noopener">${esc(p[k].slice(0,60))}</a>`:esc(p[k])}</dd>`:'').join('')}</dl>
    ${co?`<p style="margin-top:12px"><b>Company:</b> ${esc(co.name)} · ${esc(co.city||'')} ${esc(co.country||'')}</p>`:''}
    <p><button class="btn" onclick="toggleCmp('${esc(p.id)}')">${state.cmp.has(p.id)?'Remove from compare':'Add to compare'}</button></p>`;
}
window.toggleCmp=id=>{ state.cmp.has(id)?state.cmp.delete(id):state.cmp.add(id); showDetail(id); };

function renderCompare(){
  const items = DATA.products.filter(p=>state.cmp.has(p.id));
  if(!items.length){ $('cmpArea').innerHTML='<p class="hint">Nothing selected yet. Tick products in the Products tab.</p>'; return; }
  const rows = FIELDS.filter(([k])=>k!=='source_ref' && k!=='date_scanned');
  $('cmpArea').innerHTML = `<table><tr><th></th>${items.map(p=>`<th>${esc(p.name)}</th>`).join('')}</tr>` +
    rows.map(([k,l])=>`<tr><td>${l}</td>${items.map(p=>`<td>${/^https?:/.test(p[k]||'')?`<a href="${esc(p[k])}" target="_blank">link</a>`:esc(p[k]||'')}</td>`).join('')}</tr>`).join('') + '</table>';
}

function renderMakers(){
  const rows=DATA.manufacturers.filter(m=>match(m,['name','product_categories','notes','city','country']));
  $('count').textContent = rows.length+' companies';
  const cols=[['name','Company'],['type','Type'],['country','Country'],['city','City'],['product_categories','Product categories'],['verification_status','Status']];
  const draw=list=>{ $('tMakers').innerHTML=`<tr>${cols.map(([c,l])=>`<th data-col="${c}">${l}</th>`).join('')}</tr>`+
    list.map(m=>`<tr class="row ${state.selMaker===m.id?'sel':''}" data-id="${esc(m.id)}"><td><b>${esc(m.name)}</b></td><td>${esc(m.type)}</td><td>${esc(m.country)}</td><td>${esc(m.city)}</td><td>${esc(m.product_categories).slice(0,120)}</td><td>${pill(m.verification_status)}</td></tr>`).join('');
    $('tMakers').querySelectorAll('th').forEach(th=>th.onclick=()=>draw(sortBy(rows,th.dataset.col,'m')));
    $('tMakers').querySelectorAll('tr.row').forEach(tr=>tr.onclick=()=>{state.selMaker=tr.dataset.id; showMaker(tr.dataset.id); draw(list);});
  }; draw(rows);
}
function showMaker(id){
  const m=DATA.manufacturers.find(x=>x.id===id);
  const prods=DATA.products.filter(p=>p.manufacturer_company && m.name && (m.name.toLowerCase().includes(p.manufacturer_company.toLowerCase().slice(0,10))||p.manufacturer_company.toLowerCase().includes(m.name.toLowerCase().slice(0,10))));
  const ppl=DATA.contacts.filter(c=>c.organization && m.name && (m.name.toLowerCase().includes(c.organization.toLowerCase().slice(0,10))||c.organization.toLowerCase().includes(m.name.toLowerCase().slice(0,10))));
  $('makerDetail').innerHTML=`<h2>${esc(m.name)}</h2><div>${pill(m.verification_status)}</div>
   <dl><dt>Type</dt><dd>${esc(m.type)}</dd><dt>Location</dt><dd>${esc(m.city)} ${esc(m.country)}</dd><dt>Website</dt><dd>${esc(m.website)}</dd><dt>India presence</dt><dd>${esc(m.india_presence)}</dd><dt>Notes</dt><dd>${esc(m.notes)}</dd></dl>
   <h3 style="font-size:14px">Products (${prods.length})</h3>${prods.map(p=>`<div><a href="#" onclick="openProduct('${esc(p.id)}');return false">${esc(p.name)}</a></div>`).join('')||'<span class="hint">none linked by name</span>'}
   <h3 style="font-size:14px">Contacts (${ppl.length})</h3>${ppl.map(c=>`<div><b>${esc(c.person_name||'(no name)')}</b> ${esc(c.role_title)}<br>${esc(c.phone)}<br>${esc(c.email)}</div>`).join('')||'<span class="hint">none linked</span>'}`;
}
window.openProduct=id=>{ state.sel=id; show('products'); showDetail(id); };

function renderContacts(){
  const rows=DATA.contacts.filter(c=>match(c,['person_name','role_title','organization','notes','email','phone','specialty_or_product_focus']));
  $('count').textContent = rows.length+' contacts';
  const cols=[['person_name','Name'],['role_title','Role'],['organization','Organisation'],['phone','Phone'],['email','Email'],['address','Address'],['notes','Notes']];
  const draw=list=>{ $('tContacts').innerHTML=`<tr>${cols.map(([c,l])=>`<th data-col="${c}">${l}</th>`).join('')}</tr>`+
    list.map(c=>`<tr>${cols.map(([k])=>`<td>${k==='email'?esc(c[k]):esc(c[k])}</td>`).join('')}</tr>`).join('');
    $('tContacts').querySelectorAll('th').forEach(th=>th.onclick=()=>draw(sortBy(rows,th.dataset.col,'c')));
  }; draw(rows);
}

function show(tab){
  state.tab=tab;
  document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('on',b.dataset.tab===tab));
  ['overview','products','compare','manufacturers','contacts'].forEach(t=>$('view-'+t).hidden=(t!==tab));
  $('toolbar').style.display = (tab==='overview'||tab==='compare')?'none':'flex';
  $('count').textContent='';
  if(tab==='overview') renderOverview();
  if(tab==='products') renderProducts();
  if(tab==='compare') renderCompare();
  if(tab==='manufacturers') renderMakers();
  if(tab==='contacts') renderContacts();
}
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>show(b.dataset.tab));
['q','fCat','fVer','fCo'].forEach(id=>$(id).addEventListener('input',()=>show(state.tab)));
$('clearCmp').onclick=()=>{state.cmp.clear(); renderCompare();};
show('overview');
</script></body></html>
"""

out = os.path.join(HERE, "dashboard", "index.html")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML.replace("__PAYLOAD__", payload))
print("wrote", out, "products:", len(data["products"]), "makers:", len(data["manufacturers"]), "contacts:", len(data["contacts"]))
