# Release checklist

How to publish `langgraph-declarative` to PyPI. Publishing is done by
`.github/workflows/release.yml`. It runs when a GitHub release is **published** and
uploads to PyPI through trusted publishing (OIDC), so no API token is stored. Running
the workflow manually (`workflow_dispatch`) publishes to TestPyPI instead.

**One-time setup (before the first automated release):** on PyPI, open the project →
*Publishing* → add a GitHub trusted publisher: owner `pjasielski`, repository
`langgraph-declarative`, workflow `release.yml`, environment `pypi`. In the GitHub
repo, create the environment `pypi` (*Settings → Environments*). Do the same on
TestPyPI with environment `testpypi` if you want dry runs. 0.2.0 was uploaded by hand,
so this has not been exercised yet.

Versions follow [SemVer](https://semver.org/) with 0.x rules: a minor bump (0.2 → 0.3)
may contain breaking changes, and a patch bump may not. Milestone labels (M05, M06…)
are not versions. Tags `vX.Y.Z` exist only for published releases.

## 1. Prepare (on the release branch)

- [ ] All milestone tasks done; roadmap and task files ticked
- [ ] `uv run --extra dev pytest` passes locally
- [ ] Every example runs: `for d in examples/*/; do uv run python $d/main.py; done`
- [ ] `pyproject.toml` → `version = "X.Y.Z"`; `uv lock` (updates the package's own entry)
- [ ] `CHANGELOG.md`: `## Unreleased (X.Y.Z)` → `## vX.Y.Z (YYYY-MM-DD)`. Breaking
      changes come first, each with a **Migrate:** line
- [ ] README and `examples/README.md`: no "unreleased" wording for this version.
      The README is the PyPI page and cannot be changed after upload — do this
      **before** tagging
- [ ] `HANDOFF.md` status and `docs/04-plan/ROADMAP.md` milestone rows say released
- [ ] Schema copies agree: `schema/workflow.schema.json` and
      `src/langgraph_declarative/workflow.schema.json` (enforced by `tests/test_json_schema.py`)

## 2. Verify in CI

- [ ] Push the branch and open a PR to `main`
- [ ] CI is green: the **test** matrix (Python 3.10 / 3.12 / 3.13 × locked / lowest /
      latest) and the **package** job (build → install the wheel in a clean venv → read
      the packaged schema → run the quickstart)
- [ ] Optional dry run: run `release.yml` with *Run workflow* to publish to TestPyPI,
      then `pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ langgraph-declarative==X.Y.Z`

## 3. Release

- [ ] Merge the PR into `main` (merge commit, so the tag marks the merge)
- [ ] Tag the merge commit:
      `git checkout main && git pull && git tag -a vX.Y.Z -m "langgraph-declarative X.Y.Z" && git push origin vX.Y.Z`
- [ ] Create the GitHub release from the tag. Paste the CHANGELOG section as the
      notes: `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <notes.md>`
- [ ] Watch `release.yml`: build → publish-pypi

## 4. Verify the published package

- [ ] https://pypi.org/project/langgraph-declarative/ shows X.Y.Z and the README renders
- [ ] Fresh install works:
      `uv run --isolated --no-project --with langgraph-declarative==X.Y.Z python -c "import langgraph_declarative as m; from importlib import resources; print((resources.files(m) / 'workflow.schema.json').is_file())"`
- [ ] Open the next `## Unreleased` CHANGELOG section when work resumes

## If something goes wrong

- **`release.yml` fails before publishing** (tests, build, or the tag/version check):
  nothing reached PyPI. Delete the GitHub release (`gh release delete vX.Y.Z`) and
  the tag (`git push origin :refs/tags/vX.Y.Z`), fix, and release again.
- **A bad build reached PyPI:** PyPI never accepts the same version twice. Yank it on
  PyPI (it stays installable when pinned) and release a patch version `X.Y.(Z+1)`.
