"""Compare the core urology armamentarium against library.csv and write gaps.csv.

Run:  python3 urology-library/build_gaps.py
Each core item lists keywords; an item is 'have' if any library row mentions one.
Priority: core = needed in most urology practice; secondary = specialist or less common.
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))

CORE = [
 # system, kind, item, examples in India (web, 2026-11), keywords, priority
 ("Kidney and upper tract","device","PCNL nephroscope (standard and mini)","Richard Wolf / Karl Storz nephroscopes via Stark Urology (listings)",["nephroscope","pcnl"],"core"),
 ("Kidney and upper tract","device","Nephrostomy catheter (pigtail / Malecot)","Devon pigtail PCN; Nidhi Malecot; Blueneem PCN",["nephrostomy","pcn "],"core"),
 ("Kidney and upper tract","device","Ureteral access sheath","Rocamed Bi-Flex EVO; Blueneem access sheath",["access sheath","sheath"],"core"),
 ("Stones","device","Semi-rigid ureteroscope","Indoview (not found online); Stryker, Olympus",["semi-rigid","semi rigid","ureteroscope"],"core"),
 ("Stones","device","Flexible ureteroscope (digital or reusable)","Indoscope Sleek; Onli8; LithoVue",["flexible","indoscope","onli8"],"core"),
 ("Stones","device","Holmium laser lithotripsy","Potent HP / XP / HZ; Allengers BLAZE; Status Astra-35",["holmium"],"core"),
 ("Stones","device","Thulium fibre laser","Quantino 75 W; Potent Pulsed Master; Make in India Lasers",["thulium"],"core"),
 ("Stones","device","Pneumatic lithotripter","Status Calculiclast; Nidhi LITH Digi",["lithotripter","lithotripsy"],"core"),
 ("Stones","device","Stone retrieval basket","Devon helical; Kobot (Rocamed); Nidhi nitinol",["basket"],"core"),
 ("Stones","device","Double-J ureteral stent","Devon; Nidhi; Blueneem",["stent","double"],"core"),
 ("Stones","device","Hydrostatic / irrigation pump","Nidhi Easy Flow 823; Status Hydromat",["pump","irrigation"],"core"),
 ("Stones","drug","Tamsulosin (medical expulsive therapy)","URISE-D / Tamday-D are combos (web)",["tamsulosin"],"core"),
 ("Stones","drug","Potassium citrate (stone prevention)","Not checked online",["potassium citrate"],"core"),
 ("Stones","drug","Allopurinol / thiazide (metabolic stone prevention)","Not checked online",["allopurinol","thiazide"],"secondary"),
 ("Ureter and bladder","device","Rigid or flexible cystoscope","Indoscope; Nidhi cystoscope sheath; Potent",["cysto"],"core"),
 ("Ureter and bladder","device","Urodynamic system","Nexam Pro (Laborie); Potent; Status UroComp-2000",["urodynamic"],"core"),
 ("Ureter and bladder","device","Uroflowmeter","Nidhi Flow 814 / 8130 / 8150; Status FlowComp; Origin OriUFM",["uroflow","flowcomp","flow 81"],"core"),
 ("Ureter and bladder","device","Urinary drainage catheter (Foley / CIC)","Devon CIC catheter; Blueneem",["catheter","cic"],"core"),
 ("Ureter and bladder","drug","Solifenacin (OAB antimuscarinic)","SOLIES 10 (JOHNLEE); many generics",["solifenacin"],"core"),
 ("Ureter and bladder","drug","Oxybutynin / tolterodine / fesoterodine","Tolterodine-tamsulosin combos seen online",["oxybutynin","tolterodine","fesoterodine"],"core"),
 ("Ureter and bladder","drug","Mirabegron (beta-3 agonist)","Lupin (US launch, per news); India brands",["mirabegron"],"core"),
 ("Ureter and bladder","drug","Vibegron","MSN Laboratories Phase III approval (CDSCO, 2025)",["vibegron"],"secondary"),
 ("Ureter and bladder","drug","Desmopressin (nocturia)","Not checked online",["desmopressin"],"secondary"),
 ("Bladder cancer","drug","BCG for intravesical immunotherapy","Onco-BCG (SII); Onco BCG (Cipla, per listings)",["bcg"],"core"),
 ("Bladder cancer","drug","Mitomycin C (intravesical)","Not found online",["mitomycin"],"core"),
 ("Prostate","drug","Finasteride (5-alpha reductase inhibitor)","Finax (Dr Reddy's)",["finasteride"],"core"),
 ("Prostate","drug","Dutasteride (5-ARI)","Combos only (Rapilif D, URISE-D)",["dutasteride"],"core"),
 ("Prostate","drug","Tadalafil (BPH and ED)","Combos (Alfusin T); standalone not recorded",["tadalafil"],"core"),
 ("Prostate","drug","Alfuzosin / silodosin (alpha-blockers)","Alfusin T; Rapilif D; Rapaflo generics",["alfuzosin","silodosin"],"core"),
 ("Prostate","device","Bipolar TURP working element","Alan Bipolar TURP (Maruthi); Nidhi resectoscope",["turp","resectoscope","bipolar"],"core"),
 ("Prostate","device","HoLEP laser","Potent HP / Allengers / Boston Scientific MOSES (web)",["holmium","holep"],"core"),
 ("Prostate","device","GreenLight 532 nm photoselective laser","Boston Scientific XPS 180 W (global page)",["greenlight","photoselective"],"secondary"),
 ("Prostate","device","Water-vapour therapy (Rezum)","Hospital pages (Patel, Fortis Mohali)",["rezum"],"secondary"),
 ("Prostate","device","Prostate minimally invasive implant (UroLift)","Teleflex UroLift India (Jan 2023)",["urolift"],"core"),
 ("Prostate","device","Prostate biopsy (TRUS and MRI fusion)","Eigen Artemis (V.P Impex)",["artemis","biopsy","fusion"],"core"),
 ("Prostate","device","Prostate morcellator","Biorad TOMI; Allengers Dynacut",["morcell","tomi","dynacut"],"secondary"),
 ("Prostate cancer","drug","Bicalutamide (anti-androgen)","Caluran CP 50 mg (Sun)",["bicalutamide","caluran","caulran"],"core"),
 ("Prostate cancer","drug","Abiraterone (CYP17 inhibitor)","Zelgor 250 mg (Sun); cheaper generics",["abiraterone","zelgor"],"core"),
 ("Prostate cancer","drug","Enzalutamide","Obnyx (Zydus); Bdenza (BDR)",["enzalutamide"],"core"),
 ("Prostate cancer","drug","Apalutamide","Apatide (BDR, first generic)",["apalutamide"],"core"),
 ("Prostate cancer","drug","Darolutamide","No Indian brand found",["darolutamide"],"secondary"),
 ("Prostate cancer","drug","GnRH: degarelix (antagonist)","Degapride (Sun)",["degarelix","degapride"],"core"),
 ("Prostate cancer","drug","GnRH agonists (leuprolide, goserelin)","Not checked online",["leuprolide","goserelin"],"core"),
 ("Prostate cancer","drug","Docetaxel (chemotherapy)","Not checked online",["docetaxel"],"secondary"),
 ("Kidney cancer","drug","Tyrosine kinase inhibitors and immunotherapy (sunitinib, pazopanib, nivolumab)","Not checked online",["sunitinib","pazopanib","nivolumab","cabozantinib"],"secondary"),
 ("Erectile dysfunction","drug","Sildenafil","Not recorded",["sildenafil"],"core"),
 ("Erectile dysfunction","drug","Tadalafil (ED)","Alfusin T combo; standalone not recorded",["tadalafil"],"core"),
 ("Erectile dysfunction","drug","Alprostadil (intracavernosal)","Not checked online",["alprostadil"],"secondary"),
 ("Erectile dysfunction","device","Inflatable penile prosthesis","AMS 700 (Boston Scientific)",["ams 700","penile"],"core"),
 ("Incontinence","device","Artificial urinary sphincter","AMS 800 (Boston Scientific)",["ams 800","sphincter"],"core"),
 ("Incontinence","device","Synthetic sling (midurethral / male)","Lotus Freedom transobturator",["sling","freedom"],"core"),
 ("Incontinence","device","Sacral neuromodulation","Medtronic InterStim X",["interstim","sacral"],"core"),
 ("Incontinence","device","Pelvic floor biofeedback","Status Biofeedback device",["biofeedback"],"secondary"),
 ("Infection","drug","Nitrofurantoin / fosfomycin (uncomplicated UTI)","Not recorded",["nitrofurantoin","fosfomycin"],"core"),
 ("Infection","drug","Fluoroquinolones and cephalosporins (complicated UTI)","Not recorded",["ciprofloxacin","levofloxacin","cefixime"],"core"),
 ("Andrology","drug","Testosterone (replacement)","Not recorded",["testosterone"],"secondary"),
 ("Surgery general","device","Laparoscopic instruments","Shree Surgical (listing only)",["laparoscop","instrument"],"core"),
 ("Surgery general","device","Electrosurgical unit and cautery","Alan cautery (Maruthi)",["cautery","electrosurg","diathermy","alan"],"core"),
 ("Surgery general","device","Endoscopic video system and camera","e-lite (Biorad); Indocam; Status",["video","e-lite","indocam"],"core"),
 ("Surgery general","device","Cold light source","Nidhi LED light source",["light source","cold light"],"core"),
 ("Surgery general","device","Sterilisation and tray system","Endosys; Ambal (IT, not device)",["tray","sterili"],"core"),
 ("Surgery general","device","Robotic surgical system","da Vinci: 180+ systems in India (web)",["robot","da vinci","davinci"],"secondary"),
 ("Diagnostics","device","Bladder scanner / urological ultrasound","Not recorded",["bladder scan","ultrasound"],"secondary"),
]

rows = list(csv.DictReader(open(os.path.join(HERE,'library.csv'),encoding='utf-8')))
def hay(r):
    return " ".join([r.get('name',''),r.get('product_line',''),r.get('use_indication',''),r.get('notes',''),r.get('manufacturer_company','')]).lower()
out=[]
for system,kind,item,examples,kws,prio in CORE:
    matches=[r['id'] for r in rows if any(k.lower() in hay(r) for k in kws)]
    out.append([system,kind,item,examples,prio,"have" if matches else "gap",";".join(matches[:6]),"web search 2026-11-20 / core knowledge"])
with open(os.path.join(HERE,'gaps.csv'),'w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(["system","kind","item","examples_india","priority","status","matched_ids","source"])
    w.writerows(out)
gap=[o for o in out if o[5]=="gap"]
print(f"{len(out)} core items: {len(out)-len(gap)} have, {len(gap)} gap ({sum(1 for o in gap if o[4]=='core')} core gaps)")
