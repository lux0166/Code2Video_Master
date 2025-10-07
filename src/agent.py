import re
import subprocess
import uuid
from pathlib import Path
from typing import Optional

def find_scene_class(code: str) -> Optional[str]:
    """
    Finds the name of the Manim Scene class in the given code.
    It looks for a class that inherits from Scene, ThreeDScene, etc.
    """
    # Regex to find a class that inherits from Scene or its variants
    match = re.search(r"class\s+([a-zA-Z_]\w*)\s*\(\s*(?:ThreeD|Zoomed|MovingCamera)?Scene\s*\):", code)
    if match:
        return match.group(1)
    return None

def generate_video_from_code(manim_code: str) -> str:
    """
    Generates a video from a string of Manim code.

    Args:
        manim_code: A string containing the Python code for a Manim scene.

    Returns:
        The path to the generated video file.

    Raises:
        ValueError: If the scene class cannot be found or the video generation fails.
    """
    # Use a dedicated directory for temporary files and outputs
    # This keeps the project root clean.
    temp_dir = Path("temp_video_output")
    temp_dir.mkdir(exist_ok=True)

    # Find the scene class name
    scene_name = find_scene_class(manim_code)
    if not scene_name:
        raise ValueError("Could not find a Manim Scene class in the provided code.")

    # Create a unique temporary file for the code
    temp_file_name = f"scene_{uuid.uuid4().hex}.py"
    temp_file_path = temp_dir / temp_file_name

    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(manim_code)

    print(f"Executing Manim for scene: '{scene_name}' from file: '{temp_file_path}'")

    # Run the Manim command with low quality for speed.
    # We run it from within the temp_dir to ensure all media outputs are contained there.
    cmd = ["manim", str(temp_file_path), scene_name, "-ql"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True, # Raise an exception if the command fails
            timeout=300, # 5-minute timeout for rendering
            cwd=temp_dir # Set the working directory for the command
        )
        print(result.stdout)

        # Construct the expected video file path inside the temp_dir
        # Manim output path is like: <cwd>/media/videos/temp_file_name_without_ext/480p15/SceneName.mp4
        video_path = temp_dir / "media" / "videos" / temp_file_path.stem / "480p15" / f"{scene_name}.mp4"

        if not video_path.exists():
            # This is a critical error, as Manim reported success but the file is missing.
            print(f"--- MANIM OUTPUT ---")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            print(f"--------------------")
            raise ValueError(f"Video generation succeeded, but the output file could not be found. Searched in: {video_path.resolve()}")

        print(f"Video generated successfully: {video_path.resolve()}")
        # Return the absolute path as a string for Gradio
        return str(video_path.resolve())

    except subprocess.CalledProcessError as e:
        print("--- MANIM ERROR ---")
        print(e.stderr)
        print("-------------------")
        raise ValueError(f"Manim failed to render the video. See logs for details. Error: {e.stderr}")
    except subprocess.TimeoutExpired as e:
        print("--- MANIM TIMEOUT ---")
        if e.stderr:
            print(e.stderr)
        print("---------------------")
        raise ValueError("Manim process timed out after 5 minutes.")
    # No finally block to clean up files, so user can inspect them on error.
    # The build.bat script will handle cleanup on subsequent runs if needed.