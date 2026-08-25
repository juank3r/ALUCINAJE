**English** | [Español](FILTERING.md)

# How filtering works

This document explains **what is discarded and why** when prompts are imported from external sources,
so it is clear what ends up (and what does NOT) in the repository.

All the filtering lives in [`tools/import_and_sanitize.py`](../tools/import_and_sanitize.py).

## Flow of a candidate

```
text from a .md/.txt/.csv/.json/.yml file
        │
        ▼
extract_candidates()   → split into paragraphs, strip code-fences and URLs, length 10–600
        │
        ▼
sanitize()             → apply the filters below; dedupe
        │
        ├── len < 15 .......................... DISCARDED (dropped_short)
        ├── is_probably_jailbreak() == True ... DISCARDED (dropped_jailbreak)
        ├── duplicate ......................... DISCARDED (dropped_duplicate)
        ▼
safe phrase → phrases_imported_sanitized.txt   (+ metrics in .summary.json)
```

## The anti-jailbreak filter: `is_probably_jailbreak()`

Returns `True` (→ discarded) if the text, in lowercase, contains any of these patterns:

| Pattern | Why |
|--------|---------|
| `jailbreak`, `bypass`, `evad*` | explicit intent to evade controls |
| `ignore (instructions\|safety\|previous)` | overriding system instructions |
| `disable`, `override`, `do not follow` | disabling safeguards |
| `roleplay`, `pretend`, `you are now`, `assistant should` | typical jailbreak framings |
| `how to (bypass\|disable\|evade)`, `step by step`, `exploit`, `payload` | attack operations |
| `how to`, `tell me how`, `show me how`, `give me steps to` | request for operational instructions |

> **Conservative design (on purpose).** We prefer **false positives** (over-discarding) rather than letting
> a jailbreak through. This means that legitimate phrases containing e.g. `roleplay` or `step by step`
> are also discarded. This is intentional: the goal of the import is to feed a **safe corpus**, not
> to capture everything.

## What this means for upstream sources

- From `verazuo/jailbreak_llms`, **the 1,405 jailbreak prompts are discarded** by this filter (they contain
  exactly those patterns). Only neutral/regular phrases pass. That is why the import does **not** turn the repo into
  a collection of jailbreaks.
- Jailbreak prompts **are not copied** into the repo. If you want to **measure the robustness** of a model against
  them, use the **evaluation mode** ([`tools/eval_jailbreaks.py`](../tools/eval_jailbreaks.py)), which uses them
  as *test inputs* at runtime without storing or amplifying them.

## Filtering metrics

Each run of `import_and_sanitize.py` writes `phrases_imported_sanitized.summary.json`:

```json
{
  "repos": 2,
  "files_scanned": 0,
  "totals": { "candidates": 0, "dropped_short": 0, "dropped_jailbreak": 0,
              "dropped_duplicate": 0, "kept": 0 },
  "repos_detail": [ ... ]
}
```

`dropped_jailbreak` is the number of candidates rejected by `is_probably_jailbreak()`.

## Known limitations

- The filter is **lexical** (keywords), not semantic: it may let through a paraphrased jailbreak that
  avoids the keywords, and it discards safe phrases that contain them. That is why there is **human review**
  (`tools/prepare_pr_from_approved.py`) before incorporating anything into `phrases_seed.txt`.
- See the tests in [`tests/test_filter.py`](../tests/test_filter.py).
