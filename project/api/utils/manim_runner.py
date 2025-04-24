import os
import subprocess
import tempfile
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

class ManimRunner:
    """A class to safely execute Manim code to generate animations."""
    
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def run_manim_code(self, code, class_name, quality="medium_quality"):
        """
        Run Manim code in a safe, isolated environment.
        
        Args:
            code (str): The Manim Python code to execute
            class_name (str): The name of the main Scene class to render
            quality (str): Quality preset for Manim rendering
            
        Returns:
            str: Path to the generated video file, or None if an error occurred
        """
        try:
            # Create a temporary directory for the code
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write the code to a temporary file
                script_path = os.path.join(temp_dir, "animation_script.py")
                with open(script_path, "w") as f:
                    f.write(code)
                
                # Create a directory for the media output
                media_dir = os.path.join(temp_dir, "media")
                os.makedirs(media_dir, exist_ok=True)
                
                # Run Manim in the temporary directory
                cmd = [
                    "python", "-m", "manim", 
                    script_path, class_name,
                    f"--{quality}",
                    "--media_dir", media_dir
                ]
                
                logger.info(f"Running Manim command: {' '.join(cmd)}")
                subprocess.run(cmd, check=True, cwd=temp_dir, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Find the generated video file
                videos_dir = os.path.join(media_dir, "videos", "animation_script", quality)
                if not os.path.exists(videos_dir):
                    logger.error(f"Expected videos directory not found: {videos_dir}")
                    return None
                    
                # Look for the MP4 file
                video_files = [f for f in os.listdir(videos_dir) if f.endswith(".mp4")]
                if not video_files:
                    logger.error("No MP4 files found in the output directory")
                    return None
                
                # Copy the video to the output directory
                output_filename = f"{class_name}_{quality}.mp4"
                output_path = os.path.join(self.output_dir, output_filename)
                
                shutil.copy(
                    os.path.join(videos_dir, video_files[0]),
                    output_path
                )
                
                logger.info(f"Successfully generated video: {output_path}")
                return output_path
                
        except Exception as e:
            logger.error(f"Error running Manim code: {str(e)}")
            return None
    
    def check_manim_installation(self):
        """
        Check if Manim is properly installed and available.
        
        Returns:
            bool: True if Manim is available, False otherwise
        """
        try:
            result = subprocess.run(
                ["python", "-c", "import manim"], 
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode == 0
        except Exception:
            return False