import re
import subprocess
import uuid
import sys
from pathlib import Path
from typing import Optional

def get_resource_path(relative_path: str) -> Path:
    """
    Get the absolute path to a resource, works for both development (source)
    and for packaged (PyInstaller) applications.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        # The _MEIPASS is a temporary directory created by PyInstaller
        base_path = Path(sys._MEIPASS)
    else:
        # Running in a normal Python environment from the project root
        base_path = Path(".").resolve()

    return base_path / relative_path

def find_scene_class(code: str) -> Optional[str]:
    """
    Finds the name of the Manim Scene class in the given code.
    It looks for a class that inherits from Scene, ThreeDScene, etc.
    """
    match = re.search(r"class\s+([a-zA-Z_]\w*)\s*\(\s*(?:ThreeD|Zoomed|MovingCamera)?Scene\s*\):", code)
    if match:
        return match.group(1)
    return None

def generate_video_from_code(manim_code: str) -> str:
    """
    Generates a video from a string of Manim code.
    """
    temp_dir = Path("temp_video_output")
    temp_dir.mkdir(exist_ok=True)

    scene_name = find_scene_class(manim_code)
    if not scene_name:
        raise ValueError("Could not find a Manim Scene class in the provided code.")

    temp_file_name = f"scene_{uuid.uuid4().hex}.py"
    temp_file_path = temp_dir / temp_file_name

    with open(temp_file_path, "w", encoding="utf-8") as f:
        f.write(manim_code)

    # Get the correct path to the custom TeX template
    tex_template_path = get_resource_path("assets/custom_template.tex")
    print(f"Using TeX template: {tex_template_path}")
    if not tex_template_path.exists():
        raise FileNotFoundError(f"Custom TeX template not found at {tex_template_path}")

    print(f"Executing Manim for scene: '{scene_name}' from file: '{temp_file_path.name}'")

    # Final, most robust command:
    # - Use the more powerful 'xelatex' compiler.
    # - Point to our custom, comprehensive TeX template.
    cmd = [
        "manim",
        temp_file_path.name,
        scene_name,
        "-ql",
        "--tex_compiler", "xelatex",
        "--tex_template", str(tex_template_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
            cwd=temp_dir,
            encoding='utf-8',
            errors='ignore'
        )
        print(result.stdout)
        if result.stderr:
            print(f"--- MANIM STDERR ---\n{result.stderr}\n--------------------")

        video_path = temp_dir / "media" / "videos" / temp_file_path.stem / "480p15" / f"{scene_name}.mp4"

        if not video_path.exists():
            print(f"--- MANIM OUTPUT ---")
            print(f"stdout: {result.stdout}")
            print(f"stderr: {result.stderr}")
            print(f"--------------------")
            raise ValueError(f"Video generation succeeded, but the output file could not be found. Searched in: {video_path.resolve()}")

        print(f"Video generated successfully: {video_path.resolve()}")
        return str(video_path.resolve())

    except subprocess.CalledProcessError as e:
        print("--- MANIM ERROR ---")
        print(f"Manim command failed with return code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        print("-------------------")
        raise ValueError(f"Manim failed to render the video. See logs for details. Error: {e.stderr}")
    except subprocess.TimeoutExpired as e:
        print("--- MANIM TIMEOUT ---")
        if e.stderr:
            print(e.stderr)
        print("---------------------")
        raise ValueError("Manim process timed out after 5 minutes.")