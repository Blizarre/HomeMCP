#!/usr/bin/env python3

from typing import Any
import sys
import whisper


def printerr(*args: Any, **kwargs: Any):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


printerr("Loading Whisper model... (this may take a moment)")
model = whisper.load_model("small")  # Options: tiny, base, small, medium, large
printerr("Model loaded successfully!")

printerr("Transcribing audio with Whisper...")
result = model.transcribe(sys.argv[1])

# Extract transcribed text
print(result["text"])
