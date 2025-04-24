import os
import logging
import tempfile
from typing import Optional

logger = logging.getLogger(__name__)

class SpeechGenerator:
    """
    A class to generate speech from text and combine it with videos.
    """
    
    def __init__(self, output_dir):
        """
        Initialize the speech generator.
        
        Args:
            output_dir (str): Directory for output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_speech(self, text: str, output_filename: str) -> Optional[str]:
        """
        Convert text to speech using gTTS.
        
        Args:
            text (str): The text to convert to speech
            output_filename (str): The output audio file name
            
        Returns:
            str: Path to the generated audio file, or None if an error occurred
        """
        try:
            # Import gTTS here to avoid issues if it's not installed
            from gtts import gTTS
            
            # Clean up the text (remove markdown, etc.)
            cleaned_text = self._clean_text_for_speech(text)
            
            # Generate the speech file
            audio_path = os.path.join(self.output_dir, output_filename)
            tts = gTTS(text=cleaned_text, lang='en', slow=False)
            tts.save(audio_path)
            
            logger.info(f"Generated speech audio: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None
    
    def combine_audio_video(self, video_path: str, audio_path: str, output_path: str) -> Optional[str]:
        """
        Combine a video with an audio track using MoviePy.
        
        Args:
            video_path (str): Path to the input video file
            audio_path (str): Path to the input audio file
            output_path (str): Path for the output video
            
        Returns:
            str: Path to the combined video, or None if an error occurred
        """
        try:
            # Import MoviePy here to avoid issues if it's not installed
            from moviepy.editor import VideoFileClip, AudioFileClip
            
            # Load the video and audio
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            # If audio is longer than video, loop the video
            if audio_clip.duration > video_clip.duration:
                video_clip = video_clip.loop(duration=audio_clip.duration)
            # If video is longer than audio, trim the video
            elif video_clip.duration > audio_clip.duration:
                video_clip = video_clip.subclip(0, audio_clip.duration)
            
            # Set the audio
            final_clip = video_clip.set_audio(audio_clip)
            
            # Write the result
            final_clip.write_videofile(
                output_path, 
                codec='libx264', 
                audio_codec='aac',
                temp_audiofile=tempfile.NamedTemporaryFile(suffix='.m4a').name, 
                remove_temp=True
            )
            
            # Close the clips
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            logger.info(f"Combined video with audio: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error combining audio and video: {str(e)}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """
        Clean markdown text to make it suitable for text-to-speech.
        
        Args:
            text (str): Markdown-formatted text
            
        Returns:
            str: Clean text suitable for TTS
        """
        # Remove markdown headers
        text = text.replace('#', '')
        
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '').replace('__', '').replace('_', '')
        
        # Remove code blocks
        import re
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        
        # Replace mathematical notation with spoken form
        text = text.replace('^2', ' squared')
        text = text.replace('^3', ' cubed')
        text = re.sub(r'\^(\d+)', r' to the power of \1', text)
        
        # Replace common mathematical symbols
        text = text.replace('±', 'plus or minus')
        text = text.replace('≠', 'not equal to')
        text = text.replace('≈', 'approximately equal to')
        text = text.replace('∞', 'infinity')
        text = text.replace('∑', 'sum of')
        text = text.replace('∫', 'integral of')
        text = text.replace('π', 'pi')
        
        # Cleanup extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text