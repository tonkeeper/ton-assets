# Bounty Objective: False positive: Bumpkin Reward (BPL) marked as scam (ticker similar to BP xStock BPx)
Target: tonkeeper/ton-assets Issue #6560
URL: https://github.com/tonkeeper/ton-assets/issues/6560

## Issue Description
Hi team,

our jetton **Bumpkin Reward (BPL)** is marked as scam (`verification: blacklist` on tonapi / Tonkeeper), but it is the legit official token of the Telegram game Bumpkin Legends.

- Address: `EQBnrFntamCFXRZNltYsRa_Ms9Q1DJD8ZWIJwv5p04iuWrJd`
- Tonviewer: https://tonviewer.com/EQBnrFntamCFXRZNltYsRa_Ms9Q1DJD8ZWIJwv5p04iuWrJd

We believe this is the same false positive as #6496 (StarNex SNX vs SharkNinja xStock SNx): the flag probably comes from the ticker similarity with the verified **BP xStock (BPx)**. BPL has nothing to do with BP or xStocks: different symbol, different name, different project.

Why it is not a scam:
- Mint is closed and the admin is the zero address (supply can't be changed)
- Real liquidity pool on DeDust (BPL/TON): https://dexscreener.com/ton/eqa1oh5bk7n60loqpveygvebb7sdvl5nxfvsahamaab665eg
- Official announcement with the contract address in our channel: https://t.me/bumpkinlegendss/26
- Game bot: https://t.me/Bumpkinlegends_bot · website: https://bumpkinlegends.it/ · community: https://t.me/bumpkinlegendsss
- Verification PR already opened: #6556

Could you please review and remove the scam mark, or tell us the exact reason so we can fix it?

Thank you!


## Instructions for Kuro (Autonomous Solver):
1. Use skills: `systematic-debugging` and `code-review-and-quality`.
2. Inspect the repository structure, locate relevant files, and understand the bug/feature.
3. Apply the minimal, robust fix or implementation.
4. Run any existing test suites or linters in the workspace.
5. Ensure the fix adheres to the project's existing code style.
6. When done, output a summary of files modified and verification results.
