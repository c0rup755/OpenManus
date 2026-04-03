#!/usr/bin/env python3
"""
Mi Abuelita Meri - FAST MEGA EPISODE CREATOR
10 Acts × 10 Minutes = 100 Minutes Total
5-6 Scenes per Act (LONGER narration per scene)
1 Image per Act | FAST video rendering
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
        logging.FileHandler('fast_mega.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FastMegaCreator:
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.voice_profile = "abuelita_meri"
        self.review_dir = os.path.join("output", "for_review")
        self.thumbnail_dir = os.path.join("output", "thumbnails")
        os.makedirs(self.review_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
    
    def generate_script(self, act_number, title):
        """Generate 10-minute script with ONLY 5-6 scenes (longer each)"""
        logger.info(f"Generating Act {act_number} script (5-6 scenes, ~2 min each)")
        
        act_themes = [
            "La Llegada al Templo - Meri observa algo sospechoso",
            "El Descubrimiento - Meri encuentra una pista",
            "Los Rumores - El pueblo habla",
            "La Confrontación - Meri enfrenta al culpable",
            "La Confesión - La verdad sale a la luz",
            "El Escándalo - Todo se desmorona",
            "La Verdad - Lo que realmente pasó",
            "El Juicio - Meri dicta sentencia",
            "La Redención - ¿Hay perdón?",
            "El Desenlace - La lección final"
        ]
        
        theme = act_themes[act_number - 1]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": f"{title} - ACTO {act_number}: {theme}. IMPORTANTE: Crear SOLO 5 o 6 escenas largas de 2 minutos cada una. Cada escena debe tener narración extensa y detallada.",
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
                    
                    # Force only 5-6 scenes by combining if needed
                    scenes = script.get("scenes", [])
                    if len(scenes) > 6:
                        scenes = self._combine_scenes(scenes[:12], target=5)
                        script["scenes"] = scenes
                    
                    logger.info(f"Act {act_number}: {len(scenes)} scenes ready")
                    return script
            
            return None
            
        except Exception as e:
            logger.error(f"Script error: {e}")
            return None
    
    def _combine_scenes(self, scenes, target=5):
        """Combine multiple scenes into fewer, longer scenes"""
        combined = []
        group_size = len(scenes) // target
        
        for i in range(target):
            start = i * group_size
            end = start + group_size if i < target - 1 else len(scenes)
            group = scenes[start:end]
            
            combined_narration = " ".join([s.get("narration", "") for s in group])
            combined.append({
                "scene_number": i + 1,
                "narration": combined_narration,
                "image_prompt": group[0].get("image_prompt", "Cinematic church scene"),
                "duration_seconds": 120
            })
        
        return combined
    
    def generate_image(self, act_number):
        """Generate ONE image for the act"""
        logger.info(f"Generating image for Act {act_number}")
        
        prompts = [
            "Beautiful Caribbean church exterior at sunset, dramatic sky, warm golden light",
            "Church interior with stained glass windows, mysterious shadows, candlelight",
            "Two women arguing in church pew, dramatic tension, cinematic lighting",
            "Congregation whispering and gossiping, dramatic shadows, candlelight",
            "Woman kneeling at altar praying, emotional moment, divine light from above",
            "Crowd gathered outside church, scandal breaking, dramatic stormy sky",
            "Detective-like investigation in church office, clues on desk, moody lighting",
            "Intense confrontation at church pulpit, dramatic spotlight, powerful emotions",
            "Truth revealed with dramatic lighting, faces illuminated, cinematic",
            "Peaceful resolution, sunset through church windows, hope and forgiveness"
        ]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": [{"image_prompt": prompts[act_number - 1]}],
                    "style": "cinematic"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"Image generated for Act {act_number}")
                    return result.get("results", [])
            
            return []
            
        except Exception as e:
            logger.error(f"Image error: {e}")
            return []
    
    def generate_audio(self, script):
        """Generate audio for all scenes"""
        scenes = script.get("scenes", [])
        logger.info(f"Generating audio for {len(scenes)} scenes")
        
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
                timeout=300
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
    
    def create_video(self, script, act_number, title):
        """Create video for one act - should be FAST with only 5-6 scenes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"mega_act{act_number}_{timestamp}"
        
        logger.info(f"Creating video for Act {act_number}...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/create-video",
                json={
                    "project_name": project_name,
                    "script": script,
                    "quality": "high"
                },
                timeout=600  # 10 minutes max
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"✅ Video created for Act {act_number}")
                    return result
            
            logger.error(f"❌ Video creation failed for Act {act_number}")
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
            
            # Gradient background
            for y in range(height):
                factor = y / height
                r = int(30 + factor * 80)
                g = int(0 + factor * 20)
                b = int(50 + factor * 100)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Church silhouette
            church = [(400, 300), (450, 200), (500, 150), (550, 200), (600, 300), (600, 500), (400, 500)]
            draw.polygon(church, fill=(20, 20, 40), outline=(100, 100, 150))
            
            # Cross
            draw.rectangle([490, 100, 510, 200], fill=(200, 200, 220))
            draw.rectangle([450, 130, 550, 150], fill=(200, 200, 220))
            
            # Text
            try:
                font = ImageFont.truetype("arial.ttf", 42)
                small = ImageFont.truetype("arial.ttf", 28)
            except:
                font = ImageFont.load_default()
                small = ImageFont.load_default()
            
            # Title (wrap if too long)
            if len(title) > 40:
                line1 = title[:40]
                line2 = title[40:]
                draw.text((100, height - 180), line1, fill=(255, 215, 0), font=font)
                draw.text((100, height - 130), line2, fill=(255, 215, 0), font=font)
            else:
                draw.text((100, height - 150), title, fill=(255, 215, 0), font=font)
            
            draw.text((100, height - 80), "MEGA EPISODIO - 100 MINUTOS", fill=(255, 255, 255), font=small)
            
            filename = f"thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.thumbnail_dir, filename)
            img.save(filepath)
            logger.info(f"Thumbnail saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Thumbnail error: {e}")
            return None
    
    def save_episode(self, videos, thumbnail, title, scripts):
        """Save everything for review"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"mega_episode_{timestamp}"
        folder = os.path.join(self.review_dir, folder_name)
        os.makedirs(folder, exist_ok=True)
        
        import shutil
        
        # Copy videos
        for i, video in enumerate(videos):
            if video and video.get("filepath"):
                src = video["filepath"]
                dst = os.path.join(folder, f"act_{i+1}.mp4")
                shutil.copy2(src, dst)
        
        # Copy thumbnail
        if thumbnail and os.path.exists(thumbnail):
            shutil.copy2(thumbnail, os.path.join(folder, "thumbnail.png"))
        
        # Save scripts
        with open(os.path.join(folder, "scripts.json"), 'w', encoding='utf-8') as f:
            json.dump({"title": title, "acts": scripts}, f, indent=2, ensure_ascii=False)
        
        # Info file
        with open(os.path.join(folder, "INFO.txt"), 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {title}\n")
            f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Format: 10 Acts × 10 Minutes = 100 Minutes\n")
            f.write(f"Scenes: 5-6 per act\n")
            f.write(f"Videos Created: {len(videos)}/10\n")
            f.write(f"\nTO APPROVE:\n")
            f.write(f"1. Watch videos in this folder\n")
            f.write(f"2. Move to output/approved/ if good\n")
            f.write(f"3. Upload to YouTube\n")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"EPISODE SAVED: {folder}")
        logger.info(f"Videos: {len(videos)}/10")
        logger.info(f"{'='*60}\n")
        
        return folder
    
    def create_mega_episode(self):
        """Create the complete episode"""
        title = "Cuando el Diácono Descubrió el Misterio de la Sacristía"
        
        logger.info(f"\n{'='*60}")
        logger.info(f"TITLE: {title}")
        logger.info(f"10 Acts × 10 Min = 100 Minutes Total")
        logger.info(f"{'='*60}\n")
        
        # Generate thumbnail
        thumbnail = self.generate_thumbnail(title)
        
        videos = []
        scripts = []
        
        for act in range(1, 11):
            logger.info(f"\n--- ACT {act}/10 ---")
            
            # Generate script (5-6 scenes)
            script = self.generate_script(act, title)
            if not script:
                continue
            scripts.append(script)
            
            # Generate image
            self.generate_image(act)
            
            # Generate audio
            self.generate_audio(script)
            
            # Create video (should be fast with 5-6 scenes)
            video = self.create_video(script, act, title)
            if video:
                videos.append(video)
            
            time.sleep(1)
        
        if videos:
            return self.save_episode(videos, thumbnail, title, scripts)
        return None


def main():
    print("=" * 60)
    print("  FAST MEGA EPISODE CREATOR")
    print("  10 Acts × 10 Min = 100 Minutes")
    print("  5-6 Scenes per Act (FAST rendering)")
    print("=" * 60)
    
    creator = FastMegaCreator()
    result = creator.create_mega_episode()
    
    if result:
        print(f"\n✅ DONE! Location: {result}")
    else:
        print(f"\n❌ Failed")


if __name__ == "__main__":
    main()
