"""Inspect standard RIFF PCM teaching files locally; no audio playback or editing."""
import io
import json
from fractions import Fraction
from pathlib import Path
import struct
import sys
import wave

def inspect(path):
    path = Path(path)
    if path.stat().st_size > 20 * 1024 * 1024:
        raise ValueError("Teaching limit: file must be at most 20 MiB")
    data = path.read_bytes()
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("Only standard RIFF WAVE files are supported")
    if struct.unpack_from("<I", data, 4)[0] + 8 != len(data):
        raise ValueError("RIFF length does not match the file")
    offset = 12
    formats = []
    payload_sizes = []
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("Incomplete chunk header")
        label = data[offset:offset + 4]
        size = struct.unpack_from("<I", data, offset + 4)[0]
        start = offset + 8
        end = start + size
        if end > len(data):
            raise ValueError("Incomplete chunk data")
        if label == b"fmt ":
            if size < 16:
                raise ValueError("Incomplete PCM format")
            formats.append(struct.unpack_from("<HHIIHH", data, start))
        if label == b"data":
            payload_sizes.append(size)
        offset = end + size % 2
        if offset > len(data):
            raise ValueError("Missing chunk padding byte")
    if len(formats) != 1 or len(payload_sizes) != 1 or formats[0][0] != 1:
        raise ValueError("Teaching subset requires one PCM format1 chunk and one data chunk")
    _, channels, rate, byte_rate, alignment, bits = formats[0]
    if channels < 1 or rate < 1 or bits not in (8, 16, 24, 32):
        raise ValueError("Unsupported PCM parameters")
    frame_bytes = channels * (bits // 8)
    if alignment != frame_bytes or byte_rate != rate * frame_bytes or payload_sizes[0] % frame_bytes:
        raise ValueError("Inconsistent PCM frame fields")
    with wave.open(io.BytesIO(data), "rb") as audio:
        frames = audio.getnframes()
        payload = audio.readframes(frames)
        if len(payload) != payload_sizes[0] or frames * frame_bytes != len(payload):
            raise ValueError("Frame count and readable payload differ")
    duration = Fraction(frames, rate)
    return {"file": path.name, "channels": channels, "sample_width_bytes": bits // 8,
            "frame_rate_hz": rate, "frames": frames, "frame_bytes": frame_bytes,
            "payload_bytes": len(payload), "duration_fraction": str(duration),
            "duration_seconds": round(float(duration), 6)}

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python3 inspect_wav.py teaching-file.wav")
        print(json.dumps(inspect(sys.argv[1]), indent=2))
    except (ValueError, OSError, EOFError, struct.error, wave.Error) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
