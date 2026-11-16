# Tiny Chess 4K

A small, strong chess engine in a single 4 KB Python file.

- `main.py` — the engine (alpha-beta + quiescence, transposition table,
  PeSTO evaluation, iterative deepening, fixed node budget; deterministic).
- Plays via the make.fun tiny-chess-01 environment protocol
  (`MAKEFUN_ENV_URL`, `POST /game`, `POST /move`).

MIT licensed. Built from scratch for make.fun bounty `tiny-chess-01`.
