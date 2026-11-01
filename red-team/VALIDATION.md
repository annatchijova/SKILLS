# Collection validation

Validation date: 2026-11-01.

## Executed checks

- Full source-tree and blob verification against Claude-Red commit
  `a8de813edc9f66f60d44cfe42d47750e89d9930b`: 79 sources, 79 adaptation destinations.
- Snapshot preservation: 28 local skills, 42 files, checked against the pinned
  SOURCES.json hashes and compared with the originals during integration.
- Structural skill validation: all 79 adaptations passed skill-creator's
  `quick_validate.py`.
- Collection tooling regression suite: 18 passing tests, including failing fixtures
  for changed source bytes, reduced inventory, snapshot changes, broken references,
  duplicate coverage, symlink traversal and contradictory metadata identities.
- Catalog selection: general mode returns 92 original skills; red-team mode returns
  107 skills, without recursive discovery.
- Stored ADAPTATIONS.json compared equal to the validator-generated manifest.

## Independent review

See [the independent report](reviews/independent-review.md) for 24 desk scenarios
across eight representative adaptations, evidence bounds and reviewed byte identities.
The reviewer found a metadata-identity parsing inconsistency (IR-01). Integration
replaced the catalog reader with the validator's shared reader and added duplicate-key
and quoted-identity regression controls. The final test suite passes both paths.
The report preserves the finding and records any independent closure separately.

## Limits

These checks validate authored content structure, provenance, selection and tooling.
They do not certify every technique, reproduce upstream exploits, test live targets,
or establish that an agent will always follow the methodology. Embedded behavioral
acceptance cases are evaluator specifications, not executed security findings.
The independent behavioral review is a sample of eight adaptations, not all 79.
No installation into agent discovery directories, commit or push was performed.

## Repeat

From this directory:

```bash
python3 -B -m unittest -v test_collection.py
python3 -B validate_collection.py --upstream /path/to/Claude-Red
python3 -B catalog.py general
python3 -B catalog.py red-team
```

The pinned revision must exist in the upstream Git object database. Keep the snapshot
baseline pinned when checking preservation; an intentional update requires review and
repinning. These local hashes are integrity checks, not a signed external attestation.
