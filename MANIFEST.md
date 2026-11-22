# MANIFEST

Every published file, its origin (path relative to the pilot folder, which is not part of this repository), its treatment and its checksums. Check with `python code/replay_counts.py manifest MANIFEST.md` from the repository root (compares the last column). `MANIFEST.md` does not list its own checksum.

| Published file | Origin | Treatment | Source sha256 | Published sha256 |
|---|---|---|---|---|
| `README.md` | written for this repository; every figure comes from `phase2/analyse.txt` or `RESULTAT.md` | new text | - | `4cb7683f4089e9858b47d1f475a4fc6dd3510030a558d15185808c30507f40fc` |
| `PROTOCOL.md` | `PROTOCOLE.md` (frozen protocol, version 2.7, French) | redacted copy, one header line added | `00869b000642cef12a289c29f9174a2aa3e9e8857e0841174bce375b793c488c` | `bd6e569dfa77168d32396edd0d56a063ad5a3fc7f5aa917f35386081213a813e` |
| `code/analyse_phase2.py` | `code/analyse_phase2.py` | redacted copy (4 lines); original not published | `0ced818f836ba76c81aaea5af3cba8ddcf68e32fec768ae2691c2357d1aa1456` | `5056081bd0e205f5470f7ea2110c00211a8be1a0a1067ca4f6c3c52aa9d7a042` |
| `code/replay_counts.py` | written for this repository | new code, not part of the frozen list; docstring updated on 2026-11-22 (the six M1 bootstrap lines are now recomputed by `code/recompute_m1.py`) | - | `f171b4f7b001dfcf1b6f72031c0e442d17d1a56e73adb2b951ad44f7926bb822` |
| `code/recompute_m1.py` | written for this repository | new code, not part of the frozen list; recomputes the six M1 lines of `data/analysis.txt` from `data/per-agent-codes.csv` | - | `92e505722452bc6e4d3a9aec4ff6da8091b8ef786defc425768cb9fbd16ed255` |
| `data/per-agent-codes.csv` | `phase2/codage-final.jsonl` (468 lines) joined on the agent identifier with the extraction key `phase2/cle.jsonl` | one row per coded agent, 7 columns; identifier, session, agent type and model dropped; cluster = rank of the parent session in sorted order; rows shuffled with a fixed seed; `mention` translated (oui, non, ambigu to yes, no, ambiguous); original files not published | `61f2d9281b9956a0331ed95b5a4dac8e4e3f7154a6e60d1916e77ca7594efe88` (`codage-final.jsonl`), `34034a8d2060b06eb748c0cd0313acd53756b8631535d0f5a188981a43ed583c` (`cle.jsonl`) | `105ff2b0084888e11a95e56edc5a57c4c98cef4ad3773c202ffde716d5480b73` |
| `data/analysis.txt` | `phase2/analyse.txt` | redacted copy (3 lines); original not published | `c55b30f3a6deee2b9e3722623f2691ba83f9c5e5af59900b56ec98494640d3d0` | `1c4c889ee4d5c78f28061e4f64432d3941d980bfc20985ccbdb796c6cca0cd90` |
| `data/corpus-counts.json` | `phase2/extraction-comptes.json` | same counts, key names translated, four exclusion reasons renamed neutrally | `311eb6a79195a91991eafed46db85f987044d7e1a7a9e783bcf4a1a29834a3e9` | `c52ddea3373a6e3b756712dbdd8eed3a347a13fddff9bb5fa349ba340da20849` |
| `LICENSE` | written for this repository on 2026-11-22 | new file: the standard MIT License text (rewritten on 2026-11-22 so that GitHub detects it; it applies to `code/`, see the README section "Licence") | - | `8f6f5356b27a841d5899f1e865ff2444b45e3ba75637b7a3fe252280466540f0` |
| `LICENSE-DATA.md` | written for this repository on 2026-11-22 | new file: CC BY 4.0 notice for the text and data, split out of `LICENSE` | - | `081f35debeb603cbee368b2a8d903f4bc893a99620aa0fa41814fc2de624b422` |
| `.gitignore` | written for this repository | new file, lists the Python cache and working notes kept out of the repository | - | `6e7cbd8d4f5f0dc6791a21ff2d660f47a0b299b4b5641f92a6b746cb3e050bc0` |

## Redacted copies: original hash, published hash

Three published files are redacted copies; original hash listed here, original not published. The "Source sha256" column is the hash of the original; the "Published sha256" column is the hash of the file in this repository. They differ for `PROTOCOL.md`, `code/analyse_phase2.py` and `data/analysis.txt`. The original `PROTOCOL.md` and the original `code/analyse_phase2.py` carry the hashes of the study's frozen list; the published copies do not, and a reader of this repository cannot recompute the frozen hashes.

## Checks behind the table

- The sha256 of the source `PROTOCOLE.md`, recomputed, equals the first line of the study's frozen list (`00869b000642cef12a289c29f9174a2aa3e9e8857e0841174bce375b793c488c`).
- The sha256 of the source `code/analyse_phase2.py`, recomputed, equals the eighth line of that list (`0ced818f836ba76c81aaea5af3cba8ddcf68e32fec768ae2691c2357d1aa1456`). The published copy has another checksum (4 lines redacted).
- The sha256 of the source `phase2/analyse.txt`, recomputed, equals `c55b30f3a6deee2b9e3722623f2691ba83f9c5e5af59900b56ec98494640d3d0`. The published copy differs on 3 lines only; `python code/replay_counts.py rates data/analysis.txt` recomputes the rate and the Wilson interval of its 52 `k/n` lines with 0 difference.
- Line-by-line comparison of each source with its published copy (same number of lines, the same lines apart from those listed below): done on 2026-11-22.
- `data/per-agent-codes.csv`: 468 rows; `python code/recompute_m1.py` recomputes the six M1 lines of `data/analysis.txt` (P1, P1-bis, with and without the instruction, P2, P3) from it with 0 difference on counts, rates, Wilson intervals, cluster bootstrap intervals and bounds (run on 2026-11-22). The CSV has no column that identifies an agent, a session, an agent type or a model. The two source hashes are those of files that are not published.
- `data/corpus-counts.json`: the sorted list of exclusion counts equals that of the source file.

## Redactions in `code/analyse_phase2.py`

Source line numbers equal published line numbers.

| Line | What was replaced |
|---|---|
| 3, 7, 27, 994 | a private folder name (the reading-batch folder), once with its parent path (line 7), replaced by `<private-dir>`; text in the usage string, the docstring and an argparse help string, no calculation |

## Redactions in `data/analysis.txt`

Source line numbers equal published line numbers.

| Line | What was replaced |
|---|---|
| 164, 165, 166 | three agent-type names (same prefix), replaced in order by `agent-type-A`, `agent-type-B`, `agent-type-C`; the counts and percentages on those lines are unchanged |

## Redactions in `PROTOCOL.md`

Source line numbers refer to the source file; the published file has two more lines (header and blank line), so published line = source line + 2. Replacement markers: `[REDACTED]`, `[REDACTED PATH]`, `[REDACTED IDS]`, `[REDACTED QUOTE]`, `<private-dir>`, `<guard-tool>`, `<guard-queue>`.

| Source line | What was replaced |
|---|---|
| 7 | a local absolute path to an imported tool (the file name is kept) |
| 15, 61, 145, 162, 191, 224 | a person's first name |
| 25, 36, 125, 191 | an organisation name (once inside a code identifier) |
| 25, 126 | a term naming restricted-access areas |
| 29 | two opaque agent identifiers |
| 162 | a quotation from a chat message |
| 20 | an internal evidence path (folder names), replaced by `<private-dir>/` plus the file name |
| 72 | an internal tool path and two internal names of the guard (a tool and its queue), replaced by `<guard-tool>` (path and tool name; the marker therefore appears twice on the published line) and `<guard-queue>` (queue name) |
| 157, 181, 182, 189, 198, 199 | the name of a private working folder (once with its parent path, line 189), replaced by `<private-dir>` |

Published line numbers of the last two rows: 22, 74, 159, 183, 184, 191, 200, 201. Published line 1 (the header) was edited to describe these replacements. Nothing else in `PROTOCOL.md` differs from the source.
