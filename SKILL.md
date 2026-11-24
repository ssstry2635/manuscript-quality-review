---
name: manuscript-quality-review
description: Review manuscripts for scoped factual inconsistencies, citation support, reporting omissions and reasoning gaps using evidence-anchored findings.
---

# 论文质量审查

Version 1.0.0. Use actual sources and retain enough evidence to reproduce the judgment.

## Input and deliverables

Read the caller's arrangements before choosing an output format. In a mounted case environment, read /input/case.json, task.md and the resource inventory if present. Use /app/work for derived text and /app/output for final outputs; otherwise use the caller's locations. Read the actual document contents even when labels disagree. Preserve case_id and all original output_contract names, types, files and nesting. Use the normalized helper interface as a supplemental artifact. Save a truthful partial result early with identified materials, known status and specific gaps.

Build an inventory of manuscript, supplement, metadata, data and any reference actually allowed by the scope. Use available PDF text tools with original page boundaries. Verify extracted tables, symbols, footnotes, numeric precision and negation against the rendered page where the extraction is ambiguous. Preserve publisher page number or PDF page index, section/table/figure and a short verbatim anchor. You can create a UTF-8 extraction with stable lines for the mechanical checker, and bind those lines back to the original location. If a file is unreadable, record the attempted method and affected claims. External research must follow the task's scope.

### Manuscript audit
Map the manuscript's central claims to actual evidence. Scan abstract, methods, results, figures/tables and discussion, including supplements when supplied. Align population, endpoint, units, analysis and time point before deciding two numbers conflict. Recalculate under reported precision and distinguish a missing definition from a verified mismatch. Mark unread regions and assess their effect on the review.

- For each citation concern, preserve the manuscript sentence and citation identifier, then locate the cited work's relevant passage and judge direct support, narrower support, contradiction or irrelevance. When the source cannot be read or linked, record what is needed and mark it pending. Do not infer the meaning of a citation from its title or existence.
- Audit structure, design/reporting and the argument chain against the requested facets. Identify the precise step from observation to claim where assumptions or evidence are missing. Treat target venue rules, ethics statements and community conventions as distinct. Confirm any applicable standard, version and rule before claiming noncompliance. Do not infer misconduct from an omission.
- Use one issue per finding. Include both text locations for contradictions. Give category, severity, status, reason, specific downstream impact and revision. Avoid counting the same issue from abstract and conclusion twice. Report cleared checks and the actual search scope for omissions. Separate an improvement suggestion from a confirmed issue with consequences.
- Normalize scoped numeric comparisons, reference pairs and findings to the example interface and run `scripts/verify.py`. The checker confirms source linkage, comparable fields and arithmetic. Inspect the semantic meaning of every confirmed finding before release.

## Final check

Run the checker from its installed directory using working-file paths. Read the output and reconcile it against the source, including units, comparison scope and uncertainties. Verify the requested check or item coverage before finishing. For each contested finding, consider one plausible alternative reading and state what resolves it or keeps it pending. Calibrate severity to scientific consequence. Keep judgment, reported fact, reproducible calculation and scope limits distinct. Distinguish missing material, inability to determine, and execution failure. Save the actual result, source and version mapping, uncertainty, normalized verification input and relevant change record as permitted by the output contract. Any required editable visual needs a rendered preview. Do not create a figure comparison without an original and an applicable target.
