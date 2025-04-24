from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time
import uuid
import subprocess
import threading
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create static directories if they don't exist
UPLOAD_FOLDER = os.path.join(app.static_folder, 'videos')
MANIM_CODE_FOLDER = os.path.join(app.static_folder, 'manim_code')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MANIM_CODE_FOLDER, exist_ok=True)

# Predefined responses for demo purposes
DEMO_RESPONSES = {
    "pythagorean theorem": {
        "explanation": """# The Pythagorean Theorem

The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse (c) equals the sum of squares of the other two sides (a and b).

Mathematically: a² + b² = c²

Key points:
- Only works for right triangles
- The hypotenuse is always the longest side
- Used extensively in geometry and real-world applications

Example:
If a = 3 and b = 4, then:
3² + 4² = c²
9 + 16 = c²
c = √25 = 5""",
        "manim_code": """from manim import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Create right triangle
        triangle = Polygon(
            ORIGIN, RIGHT * 3, UP * 4,
            color=WHITE
        )
        
        # Add labels
        labels = VGroup(
            MathTex("a = 3").next_to(triangle, DOWN),
            MathTex("b = 4").next_to(triangle, RIGHT),
            MathTex("c = 5").next_to(triangle, UP+LEFT)
        )
        
        # Show equation
        equation = MathTex(
            "a^2 + b^2 = c^2",
            "\\\\",
            "3^2 + 4^2 = 5^2",
            "\\\\",
            "9 + 16 = 25"
        ).to_edge(RIGHT)
        
        # Animations
        self.play(Create(triangle))
        self.play(Write(labels))
        self.play(Write(equation))
        self.wait(2)"""
    },
    "quadratic equations": {
        "explanation": """# Quadratic Equations

A quadratic equation has the form: ax² + bx + c = 0

The solution is found using the quadratic formula:
x = (-b ± √(b² - 4ac)) / 2a

Key concepts:
1. The discriminant (b² - 4ac) determines the number of solutions:
   - If > 0: Two real solutions
   - If = 0: One real solution (repeated)
   - If < 0: Two complex solutions

2. The graph is always a parabola
   - Opens upward if a > 0
   - Opens downward if a < 0""",
        "manim_code": """from manim import *

class QuadraticEquation(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 6, 1],
            axis_config={"include_tip": True}
        )
        
        # Plot quadratic function
        graph = axes.plot(
            lambda x: x**2 - 2*x - 3,
            color=BLUE
        )
        
        # Add labels
        labels = VGroup(
            axes.get_x_axis_label("x"),
            axes.get_y_axis_label("y")
        )
        
        # Show equation
        equation = MathTex(
            "x^2 - 2x - 3 = 0"
        ).to_edge(UP)
        
        # Solutions
        solutions = VGroup(
            Dot(axes.c2p(-1, 0), color=RED),
            Dot(axes.c2p(3, 0), color=RED)
        )
        
        # Animations
        self.play(Create(axes), Create(labels))
        self.play(Write(equation))
        self.play(Create(graph))
        self.play(Create(solutions))
        self.wait(2)"""
    }
}

@app.route('/')
def index():
    return jsonify({"status": "API is running"})

@app.route('/api/chat', methods=['POST'])
def chat():
    if not request.json or 'prompt' not in request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    prompt = request.json['prompt'].lower()
    logger.info(f"Received prompt: {prompt}")
    
    # Generate a unique ID for this request
    unique_id = str(uuid.uuid4())[:8]
    
    try:
        # Check for predefined responses first
        for key, response in DEMO_RESPONSES.items():
            if key in prompt:
                # Create a dummy video for demonstration
                video_filename = f"{unique_id}_animation.mp4"
                video_path = os.path.join(UPLOAD_FOLDER, video_filename)
                create_dummy_video(video_path)
                
                return jsonify({
                    "explanation": response["explanation"],
                    "video_url": f"/api/static/videos/{video_filename}",
                    "manim_code": response["manim_code"]
                })
        
        # If no predefined response matches, return a generic response
        return jsonify({
            "explanation": "I understand you're asking about " + prompt + ". While I'm in demo mode, I can only provide detailed responses about the Pythagorean theorem and quadratic equations. Please try one of those topics!",
            "video_url": None,
            "manim_code": None
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Failed to process the math request",
            "details": str(e)
        }), 500

@app.route('/api/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

def create_dummy_video(output_path):
    """Create a dummy video file for development purposes."""
    try:
        # Use FFmpeg to create a dummy video
        cmd = [
            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=duration=10:size=640x480:rate=30', 
            '-vf', "drawtext=text='Mathematical Visualization':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2",
            '-c:v', 'libx264', output_path
        ]
        
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Created dummy video at {output_path}")
    except Exception as e:
        logger.error(f"Error creating dummy video: {str(e)}")
        # Create an empty file as fallback
        with open(output_path, 'wb') as f:
            f.write(b'dummy video content')

if __name__ == '__main__':
    app.run(debug=True)