# GitHub presentation wheels

Research date: 2026-10-06. We inspected primary documentation and repository READMEs, then applied their information structure rather than their wording. Four wheels per category; 16 total. The [12-repository comparison](BENCHMARK_REPOS.csv) records API star counts, README blob identities and retrieval times. Stars describe visibility, not quality or tested performance.

## A. README and landing structure

| Wheel | Useful structure | Applied here / boundary |
|---|---|---|
| [Standard Readme](https://github.com/RichardLitt/standard-readme) | Predictable introduction, usage and contribution sections | Explain purpose before history; keep contribution discoverable. Do not imply a selected license. |
| [Best README Template](https://github.com/othneildrew/Best-README-Template) | Product explanation, getting started, roadmap | Short exploration path and separate roadmap. Remove irrelevant installation boilerplate. |
| [readme.so](https://github.com/octokatherine/readme.so) | Modular section selection | Select only sections with actual content; no empty feature or sponsor blocks. |
| [readme-md-generator](https://github.com/kefranabg/readme-md-generator) | Consistent project metadata and contribution entry | Three meaningful badges; no invented package version, test coverage or license badge. |

## B. Visual presentation

| Wheel | Useful structure | Applied here / boundary |
|---|---|---|
| [Shields.io](https://shields.io/) | Compact, legible static status labels | Research, documented evidence and contributions. Static labels are not live CI signals. |
| [Mermaid](https://mermaid.js.org/intro/) with [GitHub diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams) | Text-maintained architecture near the introduction | Human → coordinator → independent workers → evidence → decisions. Label it conceptual. |
| [LICEcap](https://cockos.com/licecap/) | Record a real selected screen region as a GIF | Future sanitized event-log replay only; no browser session recorded in this task. |
| [GitHub social preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview) | Deliberately designed sharing image | Concrete 1280 × 640 specification; no fabricated product interface. |

## C. Discovery and distribution

| Wheel | Useful structure | Applied here / boundary |
|---|---|---|
| [Repository search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories) | Name, description and topics are searchable; README search has explicit qualifiers | Put browser AI orchestration in the description. Do not promise ranking or star growth. |
| [Repository topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) | A small set of relevant discovery terms | Ten topics reflecting recorded tools and research; none implies a shipped MCP server. |
| [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | Versioned notes and assets tied to a tag | Link the immutable freeze tag; do not create a new release for presentation edits. |
| [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | Explain what, why, start, help and maintenance; use relative documentation links | Keep the landing short and move detailed history into linked evidence. |

Discovery path: accurate description/topics → clear positioning and conceptual visual → evidence table → exploration command → bounded contribution. This is an information-design hypothesis, not a measured conversion result.

## D. Contributor onboarding

| Wheel | Useful structure | Applied here / boundary |
|---|---|---|
| [Contribution guidelines](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors) | Explicit workflow and acceptable changes | Three small entry tasks with artifacts and acceptance criteria. |
| [Issue Forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) | Required evidence, expected outcome and scope fields | Separate corrections, bounded contributions and research proposals. |
| [Helpful contribution labels](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/encouraging-helpful-contributions-to-your-project-with-labels) | Curate small, explained tasks before labeling | Task briefs exist; no fabricated live issues or blanket beginner labels on runtime work. |
| [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) | Route reviews to actual maintainers | Deferred until owners accept responsibility; do not invent reviewers. |

Security reporting follows [GitHub's reporting documentation](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting). Discussions and CODEOWNERS remain owner decisions rather than empty governance files.

## Comparable projects and first-screen decisions

The CSV compares browser-use, Skyvern, Playwright MCP, Cline, Aider, OpenHands, Deep Agents, AutoGen, three browser-chat coding bridges and open-dots. We inspected README ordering and linked entries, not rendered viewport timing or runtime behavior. `NOT_IN_README` means only that; it does not assert absence elsewhere in the repository.

Real possible matches for the remembered browser-chat coding tool are [browser-agent](https://github.com/ianmadez/browser-agent), [chatgpt-browser-agent](https://github.com/abdallhMoukdad/chatgpt-browser-agent) and [browse_code](https://github.com/Dedeep007/browse_code). Their actual READMEs describe browser chat bridges. We cannot identify which one the user previously saw. The first has OpenBrowser branding and upstream badge references; canonical ownership is not inferred from its name.

Copy structurally: purpose before setup; a visual connected to the actual workflow; explicit limitations and scoped contribution paths. Do not copy enterprise claims, fully autonomous/free/security promises, unrelated badges or product installation flows when our deliverable is research documentation. AutoGen's current maintenance warning is a useful example of honest status placement. OpenHands' current README uses Agent Canvas branding; the comparison records that observed state.

Art of README examples could not be retrieved at the attempted repository locations and are excluded from the 16-wheel count. LICEcap's official website supplied its documentation when its repository README was unavailable. [Source receipts](docs/PRESENTATION_SOURCE_RECEIPTS.json) pin the successful GitHub benchmark reads.
