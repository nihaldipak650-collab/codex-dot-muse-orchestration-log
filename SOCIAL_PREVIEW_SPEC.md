# Social preview specification

Status: specification only; no image generated or uploaded in this task.

## Copy and canvas

- Canvas: **1280 × 640 px**, opaque PNG, under 1 MB. GitHub accepts PNG/JPG/GIF and recommends this size; see [official requirements](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).
- Title: **Codex · DOT · Muse**.
- Main line: **Failure-driven browser AI orchestration**.
- Supporting line: **Recorded runs. Inspectable failures. Progress-first playbooks.**
- Evidence footer: **26h file-evidence span · 90m benchmark · 8h research window**.
- Small qualifier: **Research project · runtime on the roadmap**.

## Composition

Use a dark navy background, off-white text and teal worker lanes. Keep a 64 px safe margin. Put title and message in the left 55%; place a simple two-lane diagram in the right 45%: Human → Codex → DOT / Muse → Evidence → Verify & refill. The two worker nodes have equal weight. Keep title at least 48 px and supporting text at least 26 px. Avoid logos belonging to other providers, tiny tables, star counts and decorative badge clusters.

The diagram represents the intended workflow, not a screenshot of shipped software. Use the same terms as README. Maintain contrast, check a 640 × 320 reduction, and ensure the title and qualifier survive common sharing crops. Repeat image meaning in README text for accessibility.

## Future screenshot / GIF brief

A real recording can show the published sanitized JSONL next to a simple event timeline: composer draft → sent message → reply visible → result received. Label it **synthetic replay of recorded failure patterns** if synthetic fixtures drive it. A historical replay must link each event to its source and distinguish missing observations. Target 10–15 seconds with pauseable captions. Use LICEcap or equivalent only after the fixture/viewer exists; never stage a browser worker conversation or expose cookies, account names or private prompts.

The current Mermaid architecture satisfies this task's visual requirement. A future preview upload is an owner action after an actual image is reviewed.
