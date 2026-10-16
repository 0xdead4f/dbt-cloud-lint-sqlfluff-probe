# dbt Cloud CI Lint — SQLFluff `library_path` probe

Benign security-research probe supporting bug bounty report
`9473e6b0-b398-4347-8b4e-de53689983d6` to dbt Labs.

dbt Cloud's CI **Lint** step runs
`sqlfluff lint --library-path=none --dialect postgres` over the cloned
repository. SQLFluff's CLI converts the literal string `none` to a falsy
Python `None`, so the flag that exists to disable repository-controlled
Python imports disables nothing, and the repository's own `library_path`
value is used instead. SQLFluff then imports and executes every module in
that directory.

This repository contains:

- `dbtcloud_probe_cmdlib/p.py` — runs one command and returns the output
  through SQLFluff's error channel. Default: `id` and `cat /etc/passwd`.
- four `.sql` files delivering the directive in spellings that survive a
  correct `--library-path` fix.
- five benign controls that prove the repository's configuration is read,
  without any code running.
- one negative control that must never fire.

Nothing here contacts the network, reads credentials, or touches anything
outside the lint process. It is inert unless a SQLFluff run is configured to
honour a repository-supplied `library_path`.
