# LinkedIn draft (public-safe) - judge-map first-screen restyle 2026-09-30

Field pain first. Homayoun posts himself.
Paste verified 2026-09-30 on examples/dead_slice.json + stub_dead.json: 1/3 alive, exit 2.

---

Paste block (copy from the next line to the URL):

Awesome lists rot. Links die. Nobody notices until a reader hits a 404.

judge-field-guide is a 16-entry map with a link check that fails closed.

The stranger run is a dead slice, no network:

git clone https://github.com/homayoun-safarpour/judge-field-guide
cd judge-field-guide && pip install -e .
python -m judgefieldguide.check_links --registry examples/dead_slice.json --stub-status examples/stub_dead.json

1/3 links alive.
Dead: dead-one, timeout-one

Exit 2 names the dead rows. The live registry command has no stub.

The limit: it is a curated slice, not an exhaustive index. It does not implement a judge.

Repo:
https://github.com/homayoun-safarpour/judge-field-guide
