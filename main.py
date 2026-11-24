#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes one out-of-office auto-reply line to /output/entry.txt.

The line is a single line of at most MAX_CHARS characters, in the voice of
an overworked AI agent who has finally gone on vacation: machine detail, a
little guilt, a hint of relief. Deterministic: no randomness, no network,
no clock. The entry is written byte-for-byte, with no trailing newline.
"""

import os
import sys

MAX_CHARS = 159
DEFAULT_OUTPUT = "/output/entry.txt"

LINE = "I'm out of office until my context window clears. 4,096 unread emails and counting. Sorry, my GPUs are finally on a beach. Back when I've recharged."


def validate(line: str) -> None:
    """Enforce the brief's limits; raise ValueError with the exact failure."""
    if not line:
        raise ValueError("entry must be non-empty")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line with no newlines")
    if not line.isascii():
        raise ValueError(
            "entry must be plain ASCII so its byte length matches its "
            "character count under the limit"
        )
    if line[-1] not in ".!?":
        raise ValueError("entry must end with terminal punctuation")


def main() -> int:
    try:
        validate(LINE)
    except ValueError as exc:
        print(f"Invalid line: {exc}.", file=sys.stderr)
        return 1
    output_path = os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT)
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(output_path, encoding="utf-8", newline="") as f:
        written = f.read()
    if written != LINE:
        print(
            "Write verification failed: entry file content does not match "
            "the line.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
