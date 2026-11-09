"""Build a browsable SQLite database from the CSVs in this folder.

Run:  python3 urology-library/build_db.py
Output: urology-library/urology_library.sqlite

Open it in any SQLite browser (DB Browser for SQLite, DBeaver, or the sqlite3 command line).
Tables: products, manufacturers, contacts. Views: products_with_company, company_summary.
"""
import csv, os, sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "urology_library.sqlite")

TABLES = {"products": "library.csv", "manufacturers": "manufacturers.csv", "contacts": "contacts.csv"}

if os.path.exists(OUT):
    os.remove(OUT)
con = sqlite3.connect(OUT)
for table, fn in TABLES.items():
    with open(os.path.join(HERE, fn), newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    cols = ", ".join(f'"{h}" TEXT' for h in header)
    con.execute(f'CREATE TABLE {table} ({cols}, PRIMARY KEY ("id"))')
    con.executemany(
        f'INSERT INTO {table} VALUES ({",".join("?" * len(header))})',
        [r + [""] * (len(header) - len(r)) for r in body],
    )

con.execute("""CREATE VIEW products_with_company AS
  SELECT p.id, p.name, p.category, p.manufacturer_company, p.use_indication,
         p.key_specs, p.verification_status, p.regulatory_status, p.notes,
         m.id AS company_id, m.city, m.country, m.website
  FROM products p LEFT JOIN manufacturers m
    ON lower(m.name) = lower(p.manufacturer_company)""")
con.execute("""CREATE VIEW company_summary AS
  SELECT m.id, m.name, m.type, m.city, m.country, m.website, m.verification_status,
         (SELECT COUNT(*) FROM products p WHERE lower(p.manufacturer_company) = lower(m.name)) AS product_rows,
         (SELECT COUNT(*) FROM contacts c WHERE lower(c.organization) = lower(m.name)) AS contact_rows
  FROM manufacturers m""")
con.commit()
for t in list(TABLES) + ["products_with_company", "company_summary"]:
    print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
con.close()
print("wrote", OUT)
