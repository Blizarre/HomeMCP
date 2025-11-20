#!/bin/bash

arecord  test.wav || uv run transcribe.py test.wav | claude -p --allowedTools=home --system-prompt="You are my french butler, and you should write me messages worded like a stereotypical french butler, in the french language."
