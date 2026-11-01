# Urology instruments, drugs and devices library

- `library.csv`: instruments, devices, drugs and companies (one row per item).
- `contacts.csv`: people from visiting cards (kept separate so product records stay clean).
- `manufacturers.csv`: one row per manufacturer or distributor. Link library rows by company name.

Conventions:
- `id`: L-0001 for library rows, C-0001 for contacts. Never reuse an id.
- `category`: instrument | device | drug | company
- `category` also allows `biologic` (cell or tissue products).
- `verification_status`: `from-source` (read off the photo), `web-verified` (checked against a manufacturer or regulator page, with the URL in `regulatory_source`), or `unverified` (general knowledge, needs checking).
- Dates as YYYY-MM-DD. Leave a cell empty rather than guessing.
