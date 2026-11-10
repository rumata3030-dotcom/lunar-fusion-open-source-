# Lunar-Fusion-Open-Source (v0.5)

**An open concept for in-situ ³He extraction on the Moon, built around a coaxial recuperator with 60% thermal recovery.**

> Status: **raw concept, deliberately optimistic.**
> If the idea is worth anything, smarter people will find the flaws and fix them. That is the point of this repository.

## Why this project exists
I spent two years building a waste-oil-to-diesel reactor as a hobby. That reactor taught me the hardest lesson in thermal engineering: heating a poorly-conducting medium evenly, without coking or sintering, is the real problem — not the chemistry.

Lunar ³He extraction has the *exact same* physics problem. This repository is my attempt to transfer that experience to the Moon.

## What is verified
- Γ-regime correction for vibrated granular beds → see [`firmware/vkgr-fluidics/vkgr_fluidics_v0.5.py`](firmware/vkgr-fluidics/vkgr_fluidics_v0.5.py)
- Thermal loop physics for the coaxial recuperator

## What is speculative
- 13.8 MW orbital laser
- DFD with 573 N thrust
- Industrial-scale production (the original concept overestimated by ~1000×)

## What is real
- The coaxial counter-flow recuperator concept
- The Γ-regime insight (this is the single most original contribution)
- Two years of practical pyrolysis experience, now transferred to regolith

## Project layout
- `docs/` — concept, background, and physics review
- `firmware/` — fluidization simulator (Python)
- `cad/`, `optics/` — open slots, seeking contributors

## How to contribute
Open an issue. Tell me where I'm wrong. That is the entire process.
