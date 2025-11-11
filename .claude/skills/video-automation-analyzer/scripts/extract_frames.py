#!/usr/bin/env python3
"""Extract frames from video file without analysis."""
import sys
import argparse
from pathlib import Path
import cv2

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from video_analyzer import VideoProcessor


def main():
    parser = argparse.ArgumentParser(description="Extract frames from video")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("--output", default="./frames", help="Output directory")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second")
    parser.add_argument("--format", choices=["jpg", "png"], default="jpg")

    args = parser.parse_args()

    # Validate input
    video_path = Path(args.video_path)
    if not video_path.exists():
        print(f"Video not found: {args.video_path}", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract frames
    print(f"Extracting frames from {video_path.name}...")
    processor = VideoProcessor(fps_sample=args.fps)
    frames = processor.extract_key_frames(str(video_path))

    # Save frames
    for i, (timestamp, frame) in enumerate(frames):
        frame_file = output_dir / f"frame_{i:04d}_{timestamp}ms.{args.format}"
        cv2.imwrite(str(frame_file), frame)
        print(f"  Saved {frame_file.name}")

    print(f"\nExtracted {len(frames)} frames to {output_dir}")


if __name__ == "__main__":
    main()
