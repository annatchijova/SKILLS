---
name: versioned-schema-evolution
description: Stamp every serialized artifact with a schema version and evolve the format over time without breaking data that was already persisted — detect the version on load, migrate old shapes forward, and keep readers for old versions working. Use this whenever you design or change a serialization format (JSON, SQLite rows, pickle, .npy), whenever you load data that an older version of the code may have written, whenever you add or remove a field from something already on disk, and whenever a "load" path has to cope with more than one shape of stored data. Triggers — "schema migration", "backward compatible", "version mismatch", "old saved data", "from_dict", "deserialize", "we changed the format". Push to use this whenever serialized data outlives the exact code version that wrote it.
---

# Versioned Schema Evolution

Any format you persist will outlive the code that wrote it. The moment a saved file, a database row, or a serialized model can be loaded by a *different* version of your code than created it, you have a schema-evolution problem — and if the format carries no version, you have an unsolvable one: you cannot safely change it, because you cannot tell what you are looking at. The version stamp is not metadata; it is the contract that makes the format evolvable at all.

## Stamp the version — in the artifact, not just the code

Write a version field into every serialized artifact (`"engine_version": "pca_v2.4"`). This is distinct from a hashing version (see `deterministic-core`, which versions the *canonical form* so a seal stays stable): this version governs *deserialization* — it tells the loader which shape it is about to read. Increment it whenever the serialized shape changes in a way that affects how it must be read back.

## Detect the version on load, and decide deliberately

A loader must read the stamped version first and branch on it. There are three honest responses to a version it sees:

- **Known and current** — load directly.
- **Known but older** — migrate forward (below), or load with documented best-effort compatibility.
- **Unknown / newer than this code** — warn loudly and proceed best-effort, or refuse, depending on how load-bearing the data is. Never load a future version silently as if it were the current one; the fields you assume may not mean what you think.

A version mismatch is information the caller needs, surfaced as a warning, not swallowed.

## Migrate old shapes forward

When changes accumulate, a chain of small migrators beats a pile of conditionals. Register a migrator per version step (`v1 -> v2`, `v2 -> v3`) and, on load, apply them in sequence from the artifact's version up to the current one. Each migrator does one thing: add the field, rename the key, split the column. The loader never special-cases "what if this is v1 being read by v3 code" — it just walks the chain. This keeps every individual migration small and reviewable, and it means old data is always readable by new code.

## Backward compatibility: a missing field is not a zero

The subtle trap is filling a field that an old schema didn't have. If v1 saved no `mean_vector` and v2 needs one, defaulting it to zeros produces an object that *loads cleanly and is wrong* — the model is now centered on the wrong point and every result over it is quietly off. The honest move is to fill the safe default *and mark the artifact as degraded* (`requires_rebuild = True`) so a staleness check rebuilds it from real data instead of trusting the reconstruction. That hand-off to `honest-degradation` is the difference between "backward compatible" and "backward compatible and silently incorrect".

## Match the strictness to the source

Deserialization strictness depends on what the source can preserve. JSON cannot encode a dtype — every number comes back as a 64-bit float — so a JSON loader must coerce (with a warning), not reject, on dtype. A binary source (pickle, `.npy`) *does* preserve dtype, so there a mismatch is a real corruption and should raise. A single `strict` flag, defaulted correctly per source, expresses this: `strict=False` for text round-trips, `strict=True` for binary.

## Keep the old readers alive

When you bump the version, do not delete the ability to verify or read the previous one. Historical artifacts — sealed bundles, audit records, archived models — were written under the old schema and must still validate. "Increment the version and keep supporting verification for the prior version" is the rule; a migration that orphans everything written before it is a data-loss event wearing a refactor's clothes.

## Tooling

`scripts/schema_versioning.py` is a small, dependency-free framework: `dump()` stamps the current version, `load()` detects the stored version, walks a registered chain of migrators up to current, warns on unknown/newer versions, and supports per-source strictness. It includes a worked `v1 -> v2` migration. Run it to see an old-shape record loaded, migrated, and flagged.
