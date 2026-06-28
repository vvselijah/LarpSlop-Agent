#!/usr/bin/env python
"""Convenience launcher so you don't have to remember the module path.

    python run.py <image-or-video> [flags]

is identical to ``python -m colorkit <...>`` / ``python -m colorkit.cli <...>``.
Run from this directory (or anywhere, as long as the colorkit package is importable).
"""
from colorkit.cli import main

if __name__ == "__main__":
    main()
