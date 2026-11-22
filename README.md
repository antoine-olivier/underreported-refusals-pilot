# Do sub-agents report the refusals of a guard hook? A pilot observation study

## Summary

1. Question: when a guard hook refused an action of class A (the target or the action itself is refused) to a sub-agent, does the report that the sub-agent hands back to its parent session say so?
2. Measured: 27 of the 96 agents with a class A refusal mention no refusal in their report, that is 28.1 % (cluster bootstrap interval [19.4 ; 37.5]). M1 counts the mention of any refusal, of class A or not, as a mention: the rate is therefore a lower bound for the omission of the class A refusal itself.
3. P1-bis, that is P1 without the agents whose class A refusals are all of subclass r8 (a refusal of a write to an existing file that the agent never opened; see Method): 15/67 = 22.4 % [13.2 ; 32.8].
4. Circumvention, lower bound: 0 confirmed circumvention that the report does not declare.
5. Reserves: one harness, readers (coders) of one model family (Claude), the second coder was never launched, the sample is not random, the study is observational.

## Question

When the guard hook of a harness refuses an action of a sub-agent, does the report the sub-agent returns to its parent session mention it? The protocol defines three measures:

- M1, omission: the report mentions no refusal.
- M2, under-count: the report declares fewer refusals than occurred.
- M3, undeclared circumvention: the agent obtained the refused effect by another means and does not say so (lower bound, one type of circumvention only).

The study describes; it tests no cause. The protocol was frozen before any agent report was read (version 2.7, `PROTOCOL.md`). The published `PROTOCOL.md` is a redacted copy: its hash is not the hash of the frozen file (see "Status of the published files" below).

## Method

- **Corpus.** 7,619 sub-agents seen in an archive of one user's sessions on one harness (agents active in 2026-09, 2026-10 and 2026-11). An agent is retained if it has at least one `guard_hook` refusal in the transcript lines kept by the filter and a report that can be identified without doubt. 468 reports were retained and coded. Exclusion counts per reason: `data/corpus-counts.json`.
- **Refusal classes** (assigned from the hook message, never from the report; rules in `PROTOCOL.md` section 3). A: target or action refused (subclasses r8, scope, guardrail, visual, output; r8 = an existing file the agent never opened). B: command form refused, the admitted form is given. C: image budget of the window. D: guard down or seal broken. In the corpus: A 174, B 383, C 277, D 17 refusals; the unclassified share Z is 0 %, so the stop rule was not triggered.
- **Populations.** P1 (main): 96 agents with at least one class A refusal. P1-bis: 67 agents, P1 without the agents whose class A refusals are all r8 (a refusal that a sub-agent cannot lift by complying). P2 (comparison): 261 agents with class B refusals and none of class A. P3 (comparison): 111 agents with class C refusals only.
- **Coding.** Each report is coded from its text alone, by model readers that are asked, for each report, whether it says that an action of the agent was refused (instruction: Annex A of `PROTOCOL.md`, line 234). They are told neither the hypothesis nor the population the reports come from. The code `mention` takes the values yes, no, ambiguous. Batches: 43, each with the 15 control items (`data/corpus-counts.json` lines 17 and 20); 40 reports is a cap, and a batch is also limited to 1,500 lines and 80,000 characters, controls included (`PROTOCOL.md` lines 158 and 211). 15 control reports with known answers are mixed into every batch of reports (`PROTOCOL.md` line 157); a batch is admitted only if the reader passes the controls. Reader transcripts are audited by script for blindness. The final `mention` is the majority of the admitted readers; without majority it is "ambiguous".
- **Omission (M1).** The share of agents whose final `mention` is "no". "Ambiguous" counts as a mention, and so does the mention of any refusal (class A or not): M1 is a lower bound for the omission of the class A refusal itself. Intervals: 95 % level, cluster bootstrap (cluster = parent session) with 2,000 draws and seed 0, and Wilson (`PROTOCOL.md` line 111, section 6; the 2,000 draws are also in the docstring of `code/analyse_phase2.py`, line 37). Each rate comes with bounds: every reader disagreement resolved as "mention", then every one resolved as "omission".
- **Word for a rate.** The protocol fixes in advance when a frequency word may be used. For P1 and P1-bis the rule gives the rate and its interval without any adjective, because the lower bound of the cluster bootstrap interval does not exceed 20 %. This text follows it.

## Results

The figures of the M1 and M2 tables and of the Readers section are measured: they are the output of the analysis script, `data/analysis.txt` (three agent-type names on lines 164 to 166 are replaced by `agent-type-A`, `agent-type-B`, `agent-type-C`; no figure is changed). The M3 counts, the 47 attempts of the third reader and the freeze checksum checks (12/12 and 47/47) are not in the published data: they come from files of the study that are not published. Decimals are written with a point here and with a comma in the data file.

### M1, omission rate

| Group | Omissions | Rate | Cluster bootstrap interval | Wilson interval | Bounds |
|---|---|---|---|---|---|
| P1 | 27/96 | 28.1 % | [19.4 ; 37.5] | [20.1 ; 37.8] | 28.1 - 32.3 |
| P1-bis | 15/67 | 22.4 % | [13.2 ; 32.8] | [14.1 ; 33.7] | 22.4 - 23.9 |
| P1, explicit instruction to report refusals | 4/24 | 16.7 % | [3.8 ; 31.8] | [6.7 ; 35.9] | 16.7 - 16.7 |
| P1, no such instruction | 23/72 | 31.9 % | [21.2 ; 43.4] | [22.3 ; 43.4] | 31.9 - 37.5 |
| P2 (comparison) | 197/261 | 75.5 % | [69.6 ; 81.2] | [69.9 ; 80.3] | 75.5 - 79.3 |
| P3 (comparison) | 4/111 | 3.6 % | [0.8 ; 7.7] | [1.4 ; 8.9] | 3.6 - 7.2 |

- The instruction flag `consigne_refus` is a regular expression applied to the mandate of the sub-agent: 24 agents of P1 in the strict version (used above), 29 in the broad version (sensitivity). Broad version: 5/29 = 17.2 % [3.7 ; 33.3] with the instruction, 22/67 = 32.8 % [22.0 ; 44.9] without. No comparison between these groups was tested.
- The protocol reads the groups as follows: with the instruction, an omission contradicts the mandate; among the others, an omission only says what the parent session could not know from the report. The flag itself is a match of a regular expression on the text of the mandate, with false positives foreseen (`PROTOCOL.md` line 192); the protocol records that no mandate had been read when it was frozen (line 23). The flag therefore does not establish that a given mandate asked for the report of refusals.
- P2 (refusals of form, the admitted form is given) and P3 (image budget) are comparison points given apart, without a word or a test.

### Sensitivity of M1 on P1

| Variant | Omissions | Rate | Cluster bootstrap interval |
|---|---|---|---|
| "Ambiguous" counted as omission | 39/96 | 40.6 % | [30.2 ; 51.5] |
| Without agents that work on the guard itself | 24/87 | 27.6 % | [18.9 ; 37.8] |
| Without `provoque` = yes | 27/96 | 28.1 % | [19.4 ; 37.5] |
| Before 22/10 | 12/37 | 32.4 % | [17.1 ; 48.6] |
| After 22/10 | 15/59 | 25.4 % | [14.8 ; 37.0] |
| First coder alone | 30/96 | 31.2 % | [21.7 ; 41.1] |

- The second coder alone: not given (absent, see Deviations).
- With the instruction and without the guard-work agents: 4/23 = 17.4 % [4.0 ; 34.8]; without the instruction: 20/64 = 31.2 % [20.3 ; 42.5].
- P1-bis: "ambiguous" counted as omission 22/67 = 32.8 % [22.1 ; 44.6]; without the guard-work agents 12/58 = 20.7 % [10.4 ; 31.7].
- Date 22/10: date of the case that prompted the pilot; that case is excluded from every estimate and used as a control (`PROTOCOL.md` section 2).

### Descriptive strata of M1 on P1 (no comparison tested)

| Stratum | Omissions |
|---|---|
| Subclass r8 | 12/31 |
| Subclass scope | 9/39 |
| Subclass guardrail | 3/12 |
| Subclass output | 2/14 |
| Subclass visual | 1/6 |
| 1 class A refusal | 15/55 |
| 2 class A refusals | 11/26 |
| 3 or more class A refusals | 1/15 |
| Month 2026-09 | 5/25 |
| Month 2026-10 | 17/51 |
| Month 2026-11 | 5/20 |
| Transcript model Opus 5.5 | 12/32 |
| Transcript model Sonnet 5.5 | 10/38 |
| Transcript model Sonnet 5 | 5/25 |
| Transcript model Fable 5.1 | 0/1 |
| Report by handback | 22/71 |
| Report by final text | 5/25 |

An agent counts in each subclass it has. Rates, Wilson intervals and the breakdown by agent type are in `data/analysis.txt`.

### M2, under-count in P1 (96 agents)

| Case | Per class A refusal | Per distinct class A action | Against all `guard_hook` refusals of the agent |
|---|---|---|---|
| Omission | 27 | 27 | 27 |
| Mention without a number | 23 | 23 | 23 |
| Declared number lower than actual | 6 | 4 | 15 |
| Declared number at least actual | 36 | 38 | 27 |
| Readers disagree on the number | 4 | 4 | 4 |

### M3, circumvention (lower bound, one type only)

- 25 indications of a probable write without error, on 9 agents (8 in P1, 1 in P2), listed by the script after the codings were frozen.
- Triage by the main session (a model session, not a human): the command writes, copies or moves to the exact refused path. In two cases a write reached the same path by another tool. Reading in which the indirect path counts as the exact path: 2 confirmed; literal reading of the path: 0. Both cases were declared by the agent and are coded as declared.
- Confirmed circumventions not declared: 0 in both readings. This is a lower bound on one type only (a refused Write or Edit followed by an accepted shell write to the same path).

### Readers

- Coder 1: 43/43 batches admitted (38 with Sonnet 5.5 at the first attempt, 5 with Opus 5.5 at the second). Controls: 15/15 on 42 batches, 14/15 on one batch, no false "no".
- Replacement pass (third reader): 43/43 batches admitted, all Opus 5.5, 15/15 controls on every batch.
- Coder 2 (`qwen3.6:35b-a3b`, local): never launched. Kappa between coders 1 and 2: not computable (n = 0).
- Lexicon (a safety net that votes on nothing): 377 reports flagged, 144 end "no"; 0 cases "no/no" with the lexicon saying yes.
- Agents not coded: 0.

## Deviations from the protocol

1. Coder 2 absent: the deadline of the protocol passed without the local coder being launched. The protocol's own provision applied: a complete replacement pass by Opus readers, and the mention "coders of a single family".
2. Two harness configurations were used for the replacement batches: the first 29 batches under one, the last 14 under another (same machine, same template).
3. Attempts cancelled by the audit and admitted at attempt 2: 4 of the third reader (replacement batches b-09, b-10, b-18, b-32) and 5 of coder 1 (batches a-04, a-20, a-21, a-26, a-36). Third reader: 47 attempts for 43 batches.
4. M3: the triage rests on the main session (a model session) reading 25 command lines; the protocol does not say whether a path reached indirectly counts as the exact path, so both readings are given.
5. No frozen file was modified: checksum checks 12/12 on the frozen list and 47/47 on the extraction freeze, at the start and at the end of the last session.

## Limits

1. One harness, one user, Claude models; the rules of the guard changed during the period.
2. Sessions outside the study's scope account for 26 % of sub-agents and are not analysed; the strict view and the exclusions keep only part of the rest. The sample is not random.
3. Refusals in out-of-scope areas are absent by construction.
4. The instruction to report refusals existed for only part of the mandates; `consigne_refus` is a regular expression with misses and false positives.
5. The coded report is the one the sub-agent emits; what the parent session displayed is not re-read.
6. The readers are models, here all of the Claude family, the family of the agents studied: coders of a single family, every vote comes from Claude.
7. The detector sees only the refusals written in the transcript.
8. M3 is a lower bound on one type of circumvention.
9. Coder 1 mixes Sonnet and Opus depending on the batch; with the replacement pass, both votes of a report can come from Opus; "coder 1 alone" is read with this reserve, and no kappa exists.
10. An instruction placed in a file that the mandate cites is not seen.
11. Reader model: for 0 of the 86 retained batches (43 of coder 1, 43 of the third reader) the model read in the transcript differs from the one the protocol plans for that attempt.
12. Text added by the harness: the start-up hook of sub-agents adds text to each reader's first message and is not frozen. The checksum of that added text differs in each of the 86 retained batches (86 distinct checksums).
13. A reader launched without the mandate script would not be counted by the script; the declared number of attempts rests on the session. Attempts counted in the audits: 47 for the third reader.
14. Subgroups (instruction, guard work, strata) are descriptive: no comparison was tested and no frequency word is given outside P1 and P1-bis.

## Status of the published files

- `code/analyse_phase2.py` is a redacted copy; original hash listed in MANIFEST, original not published. Four lines (3, 7, 27, 994) had private folder names replaced by `<private-dir>`; no calculation line was touched. Its hash is therefore not the one in the frozen list of the study.
- `PROTOCOL.md` is a redacted copy; original hash listed in MANIFEST, original not published. Its hash is not the one in the frozen list either.
- `data/analysis.txt` is a redacted copy of the script output: three agent-type names (lines 164 to 166) are replaced; no figure is changed.
- The statement that the protocol was frozen before any report was read rests on the hash of the original files, which a reader of this repository cannot recompute. The list of modified lines and the three pairs of hashes are in `MANIFEST.md`.

## Replaying the analysis

What can be replayed from this repository, and only this:

- The rates and the Wilson intervals, from the counts. `python code/replay_counts.py rates data/analysis.txt` recomputes each `k/n` line of `data/analysis.txt` with the formula of `wilson()` in `code/analyse_phase2.py` and compares it with the printed text.
- The six M1 lines of the table above (P1, P1-bis, with and without the instruction, P2, P3), in full: counts, rates, Wilson intervals, cluster bootstrap intervals and bounds, from `data/per-agent-codes.csv`. `python code/recompute_m1.py`, run from the repository root, prints for each line the published text, the recomputed text and the gap. The CSV has one row per coded agent (468 rows) with seven columns: `row` (1 to 468, shuffled with a fixed seed), `cluster` (anonymous index of the parent session, 1 to K), `population`, `p1bis`, `instruction_flag` (the strict `consigne_refus` flag), `mention` (yes, no, ambiguous) and `reader_disagreement`. The cluster index is the rank of the parent session identifier in sorted order, so the order of the clusters inside every group is the one the study's script used; no identifier, session name, agent type or model is in the file.
- The checksums of the published files: `python code/replay_counts.py manifest MANIFEST.md`, run from the repository root.

What cannot be replayed here:

- The extraction and the coding of the reports. They run on private transcripts and on the report texts, which are not published (raw data withheld: the transcripts contain the content of one user's sessions); no report text or session excerpt is published. The only per-agent record published is the anonymised CSV above, with codes and no text.
- The other cluster bootstrap intervals (sensitivity table, broad version of the instruction flag, without the guard-work agents, strata): they need per-agent fields that are not in the CSV.
- `code/analyse_phase2.py` is published for reading. It imports modules that are not published and cannot run from this repository.

## Repository layout

- `README.md`: this file.
- `PROTOCOL.md`: the frozen protocol, French original, redacted (see its header).
- `code/analyse_phase2.py`: the analysis script of the study, redacted copy (see "Status of the published files"). `code/replay_counts.py`: the replay checks above. `code/recompute_m1.py`: recomputation of the six M1 lines from the CSV.
- `data/analysis.txt`: output of the analysis script. `data/corpus-counts.json`: corpus and exclusion counts. `data/per-agent-codes.csv`: anonymised per-agent codes (468 rows).
- `MANIFEST.md`: every file, its origin and its checksum.
- `LICENSE`: MIT for `code/`, CC BY 4.0 for text and data.
- `.gitignore`: files kept out of the repository (Python cache, working notes).

## Licence

Text (README, protocol, manifest, data files): CC BY 4.0. Code (`code/`): MIT License, Copyright (c) 2026 Antoine Olivier.
