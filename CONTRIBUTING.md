# Contributing to EchoCopi

**Hello, Many! 🌍👋🏽**

EchoCopi Core is a local memory ledger for AI assistants: every thought the assistant logs becomes one checksummed entry, and the ledger can prove whether an entry was altered. It is SparkPlugged's first product and the engine its own agents run on every day. The public Core is being brought level with that engine, in the open, and this page is how to take part.

## How work is organised

- Work is posted as issues. An issue labelled **help wanted** is open to claim.
- To claim one, comment on it. A maintainer confirms the claim and assigns the issue to you. An issue that is already assigned is taken; please pick another.
- Pull requests that are not tied to an assigned issue are closed without review. This keeps the queue honest for the people who claimed the work.
- One pull request per issue, scoped to the files the issue names.

## The contributor agreement comes first

Before your first pull request, SparkPlugged needs its contributor agreement signed. It is short: you keep your copyright, you license your contribution to the project, and you confirm the work is yours. Ask for it on the issue you claimed and it is sent to you by email. Nothing is reviewed or merged before it is signed.

## Two lanes

1. **The public Core, this repository.** Everyone starts here. Synthetic or sanitised data only; never commit real memory files.
2. **The private memory layer** that powers NovaLiveSystem. It opens to a contributor by written agreement after a completed milestone here, never by default.

## Standards

- Python 3.10 or newer. The runtime stays standard library only; test dependencies go in the test workflow.
- Every change ships with tests under `tests/` that run with `pytest` from the repository root.
- Keep diffs minimal. Do not reformat files you are not changing, and keep the existing line endings; a pull request that touches every line of a file to change one function will be sent back.
- Do not commit `evolution.json`, `session_*.jsonl` or any other memory file.
- The continuous-integration run must pass before review starts.

## Licence

EchoCopi Core is released under the SparkPlugged Community License (see `LICENSE`). Contributions are accepted under the contributor agreement and credited in git history and in release notes.

## Conduct

The `CODE_OF_CONDUCT.md` in this repository applies to every issue, pull request and discussion.

## Contact

Project questions go on the issue or in Discussions. Agreements and anything private: <hello.many@sparkpluggedts.com>.
