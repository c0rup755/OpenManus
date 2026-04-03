#!/usr/bin/env python3
"""
Mi Abuelita Meri - SINGLE 100-MINUTE VIDEO CREATOR
Creates ONE video with 10 Acts
10 Images total (1 per act)
100 Minutes of audio
Much faster than creating 10 separate videos!
"""

import os
import json
import time
import requests
import logging
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('single_video.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SingleVideoCreator:
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.voice_profile = "abuelita_meri"
        # Flask server saves to workspace/output
        self.workspace_dir = os.path.join("..", "workspace")
        self.images_dir = os.path.join(self.workspace_dir, "output", "images")
        self.audio_dir = os.path.join(self.workspace_dir, "output", "audio")
        self.videos_dir = os.path.join(self.workspace_dir, "output", "videos")
        self.thumbnail_dir = "output"  # Keep thumbnails local
        
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
    
    def generate_all_scripts(self, title):
        """Generate 10 act scripts, each with 5-6 scenes"""
        all_scenes = []
        
        act_themes = [
            "La Llegada - Meri llega al templo y nota algo raro",
            "La Primera Pista - Meri encuentra algo sospechoso",
            "Los Rumores - El bochinche se esparce",
            "La Sospecha - Meri sabe quién es",
            "La Confrontación - Cara a cara",
            "La Confesión - La verdad sale",
            "El Escándalo - Todo se desmorona",
            "El Juicio - Meri dicta sentencia",
            "La Redención - ¿Hay perdón?",
            "El Desenlace - La lección final"
        ]
        
        for act in range(1, 11):
            logger.info(f"Generating Act {act}/10 script...")
            
            try:
                response = requests.post(
                    f"{self.api_base}/api/generate-script",
                    json={
                        "topic": f"{title} - ACTO {act}: {act_themes[act-1]}. Crear 5 escenas largas de 2 minutos cada una.",
                        "content_type": "abuelita_meri",
                        "style": "dramatic",
                        "length": 10,
                        "language": "spanish",
                        "voice_profile": self.voice_profile
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        script = result.get("script", {})
                        if isinstance(script, dict) and "script" in script:
                            script = script["script"]
                        scenes = script.get("scenes", [])
                        
                        # Renumber scenes globally
                        for scene in scenes:
                            scene["scene_number"] = len(all_scenes) + 1
                            scene["act"] = act
                            all_scenes.append(scene)
                        
                        logger.info(f"Act {act}: {len(scenes)} scenes (Total: {len(all_scenes)})")
                
            except Exception as e:
                logger.error(f"Script error for Act {act}: {e}")
        
        return all_scenes
    
    def generate_images(self, num_images=10):
        """Generate ONE image per act"""
        logger.info(f"Generating {num_images} images (1 per act)...")
        
        image_prompts = [
            "Caribbean church exterior at golden hour, warm light, palm trees",
            "Church interior with stained glass, mysterious shadows, candles",
            "Two women whispering in church pew, dramatic tension",
            "Congregation gossiping, dramatic candlelight, shadows",
            "Woman confronting another at altar, powerful moment",
            "Emotional confession scene, divine light, tears",
            "Chaos in church, dramatic lighting, shocked faces",
            "Judge-like figure at pulpit, commanding presence",
            "Moment of forgiveness, warm golden light, hope",
            "Peaceful ending, sunset through windows, redemption"
        ]
        
        for i in range(num_images):
            try:
                response = requests.post(
                    f"{self.api_base}/api/generate-images",
                    json={
                        "scenes": [{"image_prompt": image_prompts[i]}],
                        "style": "cinematic"
                    },
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        logger.info(f"Image {i+1}/{num_images} generated")
                
            except Exception as e:
                logger.error(f"Image {i+1} error: {e}")
            
            time.sleep(1)
    
    def generate_all_audio(self, scenes):
        """Generate audio for all scenes"""
        logger.info(f"Generating audio for {len(scenes)} scenes...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-audio",
                json={
                    "scenes": scenes,
                    "language": "spanish",
                    "gender": "female",
                    "voice_index": 0,
                    "engine": "edge",
                    "profile": self.voice_profile
                },
                timeout=1800  # 30 minutes for all audio
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    audio = result.get("results", [])
                    success = sum(1 for a in audio if a.get("success"))
                    logger.info(f"Generated {success}/{len(audio)} audio files")
                    return audio
            
            return []
            
        except Exception as e:
            logger.error(f"Audio error: {e}")
            return []
    
    def create_single_video(self, title):
        """Create ONE video with all scenes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"mega_episode_{timestamp}"
        
        logger.info(f"Creating single 100-minute video: {project_name}")
        
        # Load all images and audio - get all files regardless of numbering
        scene_results = []
        audio_results = []
        
        # Get all image files
        import glob
        image_files = sorted(glob.glob(os.path.join(self.images_dir, "scene_*.png")))
        for img_path in image_files:
            scene_results.append({"success": True, "filepath": img_path})
        
        # Get all audio files
        audio_files = sorted(glob.glob(os.path.join(self.audio_dir, "scene_*_audio.mp3")))
        for audio_path in audio_files:
            audio_results.append({"success": True, "filepath": audio_path})
        
        logger.info(f"Found {len(scene_results)} images and {len(audio_results)} audio files")
        
        if not scene_results or not audio_results:
            logger.error("No images or audio found")
            return None
        
        try:
            response = requests.post(
                f"{self.api_base}/api/create-video",
                json={
                    "project_name": project_name,
                    "script": {"title": title, "scenes": []},
                    "quality": "medium"  # Medium for faster rendering
                },
                timeout=3600  # 1 hour timeout for 100-minute video
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"✅ Video created: {result.get('filepath')}")
                    return result
            
            return None
            
        except Exception as e:
            logger.error(f"Video error: {e}")
            return None
    
    def generate_thumbnail(self, title):
        """Generate thumbnail"""
        try:
            width, height = 1280, 720
            img = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            for y in range(height):
                factor = y / height
                r = int(30 + factor * 80)
                g = int(0 + factor * 20)
                b = int(50 + factor * 100)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Church
            church = [(400, 300), (450, 200), (500, 150), (550, 200), (600, 300), (600, 500), (400, 500)]
            draw.polygon(church, fill=(20, 20, 40), outline=(100, 100, 150))
            draw.rectangle([490, 100, 510, 200], fill=(200, 200, 220))
            draw.rectangle([450, 130, 550, 150], fill=(200, 200, 220))
            
            try:
                font = ImageFont.truetype("arial.ttf", 42)
                small = ImageFont.truetype("arial.ttf", 28)
            except:
                font = ImageFont.load_default()
                small = ImageFont.load_default()
            
            if len(title) > 40:
                draw.text((100, height - 180), title[:40], fill=(255, 215, 0), font=font)
                draw.text((100, height - 130), title[40:], fill=(255, 215, 0), font=font)
            else:
                draw.text((100, height - 150), title, fill=(255, 215, 0), font=font)
            
            draw.text((100, height - 80), "MEGA EPISODIO - 100 MINUTOS", fill=(255, 255, 255), font=small)
            
            filename = f"thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join("output", "thumbnails", filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            img.save(filepath)
            logger.info(f"Thumbnail saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Thumbnail error: {e}")
            return None
    
    def run(self):
        """Create the complete episode"""
        title = "Cuando el Diácono Descubrió el Misterio de la Sacristía"
        
        logger.info(f"\n{'='*60}")
        logger.info(f"TITLE: {title}")
        logger.info(f"Creating ONE 100-minute video")
        logger.info(f"{'='*60}\n")
        
        # Generate thumbnail
        self.generate_thumbnail(title)
        
        # Step 1: Generate all scripts
        logger.info("STEP 1: Generating scripts...")
        scenes = self.generate_all_scripts(title)
        logger.info(f"Total scenes: {len(scenes)}\n")
        
        # Step 2: Generate images
        logger.info("STEP 2: Generating images...")
        self.generate_images(10)
        logger.info("Images done\n")
        
        # Step 3: Generate audio
        logger.info("STEP 3: Generating audio...")
        self.generate_all_audio(scenes)
        logger.info("Audio done\n")
        
        # Step 4: Create single video
        logger.info("STEP 4: Creating video (this will take 20-40 minutes)...")
        video = self.create_single_video(title)
        
        if video:
            logger.info(f"\n{'='*60}")
            logger.info(f"✅ SUCCESS!")
            logger.info(f"Video: {video.get('filepath')}")
            logger.info(f"{'='*60}")
            return video
        else:
            logger.error("❌ Video creation failed")
            return None


def main():
    print("=" * 60)
    print("  SINGLE 100-MINUTE VIDEO CREATOR")
    print("  10 Acts | 10 Images | 1 Video")
    print("=" * 60)
    
    creator = SingleVideoCreator()
    result = creator.run()
    
    if result:
        print(f"\n✅ Done!")
    else:
        print(f"\n❌ Failed")


if __name__ == "__main__":
    main()
