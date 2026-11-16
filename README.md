# Tiny Chess 4K

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Arifpratama19/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Arifpratama19/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A small, strong chess engine in a single 4 KB Python file. Built for the [make.fun bounty "Build the strongest chess engine in 4 KB of Python"](https://make.fun/bounty/tiny-chess-01).

- `main.py` — the engine (alpha-beta + quiescence, transposition table,
  PeSTO evaluation, iterative deepening, fixed node budget; deterministic).
- Plays via the make.fun tiny-chess-01 environment protocol
  (`MAKEFUN_ENV_URL`, `POST /game`, `POST /move`).

MIT licensed. Built from scratch for make.fun bounty `tiny-chess-01`.
