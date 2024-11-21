import os
import shutil
import subprocess
import argparse

def automate_manim(svg_file, output_name):
    if not os.path.isfile(f"svg/{svg_file}"):
        print(f"Error: {svg_file} does not exist.")
        return

    target_svg = "svg/target.svg"

    shutil.copy(f"svg/{svg_file}", target_svg)

    try:
        manim_command = ["manim", "-pqh", "Animation.py", "FourierAnimation"]
        subprocess.run(manim_command, check=True)

        gif_output = "media/images/Animation/output.gif"
        ffmpeg_command = [
            "ffmpeg",
            "-i", "media/videos/Animation/1080p60/FourierAnimation.mp4",
            "-vf", "fps=30,scale=1200:-1:flags=lanczos",
            "-loop", "0",
            gif_output
        ]
        subprocess.run(ffmpeg_command, check=True)

        final_gif_name = f"{output_name}.gif"
        final_mp4_name = f"{output_name}.mp4"

        shutil.move(gif_output, f"gifs/{final_gif_name}")
        shutil.move("media/videos/Animation/1080p60/FourierAnimation.mp4", f"videos/{final_mp4_name}")

        print(f"Process completed. Outputs: {final_gif_name}, {final_mp4_name}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        if os.path.exists(target_svg):
            os.remove(target_svg)

def main():
    parser = argparse.ArgumentParser(description="Automate Manim and FFmpeg tasks.")
    parser.add_argument("svg_file", help="Name of svg file to use, should be in Fourier/svg.")
    parser.add_argument("output_name", help="Base name for the output GIF and MP4.")
    args = parser.parse_args()

    automate_manim(args.svg_file, args.output_name)

if __name__ == "__main__":
    main()
