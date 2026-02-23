"""
Configuration file for Handwriting Generator
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
IAM_DATA_DIR = os.path.join(DATA_DIR, 'iam_database')
DATABASE_PATH = os.path.join(DATA_DIR, 'handwriting_database.json')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IAM_DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Canvas settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400

# Vector extraction settings
RDP_EPSILON = 2.0  # Ramer-Douglas-Peucker simplification threshold

# Feature extraction settings
FEATURE_NAMES = [
    'slant_angle',
    'letter_spacing',
    'stroke_thickness',
    'cursive_ratio',
    'loop_size',
    'connection_type',
    'baseline_variation',
    'aspect_ratio',
    'pressure_variation',
    'avg_speed'
]

# ============================================
# SIMILARITY MATCHING THRESHOLDS
# ============================================
# Minimum similarity for accepting a match
MIN_SIMILARITY_THRESHOLD = 0.65  # 65% - Will warn user if below this

# Similarity quality levels
SIMILARITY_EXCELLENT = 0.90  # 90%+ = Excellent (near-perfect match)
SIMILARITY_GOOD = 0.80       # 80-89% = Good (very close match)
SIMILARITY_FAIR = 0.70       # 70-79% = Fair (acceptable match)
SIMILARITY_POOR = 0.65       # 65-69% = Poor (usable but not ideal)
# Below 65% = System will still work but warn user

# Automatic match behavior
AUTO_ACCEPT_THRESHOLD = 0.75  # 75%+ automatically accepted as good match
REQUIRE_CONFIRMATION_BELOW = 0.70  # Below 70% asks user if they want to proceed

# Style transfer settings
MAX_SLANT_DELTA = 15  # degrees
MAX_SPACING_DELTA = 0.3  # 30%
MAX_THICKNESS_DELTA = 0.4  # 40%

# Generation settings
NATURAL_VARIATION_POSITION = 0.03  # ±3%
NATURAL_VARIATION_ROTATION = 2  # ±2 degrees
NATURAL_VARIATION_SIZE = 0.05  # ±5%
NATURAL_VARIATION_STROKE = 0.1  # ±10%

# SVG settings
SVG_DEFAULT_STROKE_COLOR = 'black'
SVG_DEFAULT_FILL = 'none'
SVG_STROKE_LINECAP = 'round'
SVG_STROKE_LINEJOIN = 'round'

# Flask settings
SECRET_KEY = 'your-secret-key-change-in-production'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload

# Database generation settings
NUM_STYLES_TO_GENERATE = 100  # Number of styles to extract from IAM
MIN_SAMPLES_PER_WRITER = 5  # Minimum samples needed per writer

# GUI Settings
GUI_BG_COLOR = '#141414'  # Dark background
GUI_TEXT_COLORS = ['#FFFF00', '#00FFFF', '#90EE90', '#FFB6C1']  # Yellow, Teal, Light Green, Light Pink
GUI_FONT = ('Consolas', 10, 'bold')  # Font: Consolas Bold, Size 10
GUI_TITLE_FONT = ('Consolas', 14, 'bold')
GUI_BUTTON_FONT = ('Consolas', 9, 'bold')
