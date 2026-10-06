# Security and sensitive information

This repository contains public research documents, sanitized examples, a hash utility and an experimental single-worker browser communication runtime. It does not operate a hosted orchestration service. Runtime results and session material are local-only and ignored; replies may contain private content. Third-party browser tools and workers have their own security policies.

Never include tokens, passwords, cookies, authentication headers, browser profiles, account screenshots, private prompts or original private archives in an issue, PR or attachment. A hash is not permission to publish the corresponding source.

## Reporting

If GitHub displays **Report a vulnerability** in the repository's Security tab, use that private channel. Otherwise, open only a redacted issue requesting a private reporting channel; include no exploit details or sensitive material. Do not assume ordinary issues or maintainer profiles are private. No private email address or response-time guarantee is established here.

For non-sensitive factual corrections, use the evidence-correction form with links to public files. If a public file exposes sensitive content, report the path without reproducing it. History cleanup or credential rotation requires owner handling; do not submit copies of the secret as evidence.

## Contributor checks

Inspect changed files and attachments before submitting. The integrity checker reads local bytes and performs no network calls; it does not detect secrets or validate research claims. Historical experiments may involve accounts and browser sessions, so future live tests need explicitly scoped permissions and side-effect limits.

The frozen tag is historical evidence. Corrections belong in follow-up records on main; the tag should not be rewritten as an ordinary documentation fix.
