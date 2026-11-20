# ship-kit-demo

A public sandbox for the [Ship to Production Kit](https://github.com/aakashg/ship-to-production-kit). It is the kit's `template-repo/` plus the toy AI gateway from the kit's ops-agent test, with the kit's `.coderabbit.yaml`, `CODEOWNERS`, CI and auto-merge workflow switched on.

Two pull requests show both review routes:

| PR | What it changes | Risk | Expected route |
|---|---|---|---|
| `ops/max-tokens-4xx` | The ops agent's real fix: a max-tokens error becomes a 400, not a 500, with a test | LOW (no high-risk path) | CodeRabbit reviews and approves, the workflow turns on auto-merge, GitHub merges once CI is green |
| `fix/expired-session-401` | An expired session on `/v1/me` returns 401, not 500. Touches `app/auth/` | HIGH | CodeRabbit reviews but does not approve, the workflow labels it `needs-human-review`, it waits for the code owner |

The service is synthetic. Nothing here runs in production.

Run the tests: `pip install -r requirements.txt && python3 -m pytest -q`
