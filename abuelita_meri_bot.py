#!/usr/bin/env python3
"""
Mi Abuelita Meri - Content Review System
Creates videos and saves them for your approval before upload
"""

import os
import sys
import json
import time
import schedule
import requests
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('abuelita_meri.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AbuelitaMeriBot:
    """Autonomous content creator - saves for review, no auto-upload"""
    
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.channel_name = "Mi Abuelita Meri - Bochinches y Cuentos"
        self.voice_profile = "abuelita_meri"
        self.daily_count = 0
        self.max_daily_videos = 3
        
        # Base directory (workspace folder)
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.output_dir = os.path.join(self.base_dir, "workspace", "output")
        
        # Review folder - videos go here for your approval
        self.review_dir = os.path.join(self.output_dir, "for_review")
        os.makedirs(self.review_dir, exist_ok=True)
        
        # Approved folder - you move videos here when ready
        self.approved_dir = os.path.join(self.output_dir, "approved")
        os.makedirs(self.approved_dir, exist_ok=True)
        
        # Server output directories
        self.server_images_dir = os.path.join(self.output_dir, "images")
        self.server_audio_dir = os.path.join(self.output_dir, "audio")
        self.server_videos_dir = os.path.join(self.output_dir, "videos")
        
        # Episode topics queue
        self.topic_queue = [
            {"type": "bochinches", "topic": "Doña Carmen se cree la dueña del barrio pero nadie la respeta"},
            {"type": "bochinches", "topic": "El hijo de la vecina que se fue a 'buscar trabajo' a Orlando"},
            {"type": "bochinches", "topic": "La señora que tiene 3 novios y ninguno sabe del otro"},
            {"type": "cuentos", "topic": "La historia de la abuela que enamoró al cura del pueblo"},
            {"type": "cuentos", "topic": "El cuento de Doña Perfecta y sus 5 matrimonios"},
            {"type": "bochinches", "topic": "El marido que le regaló un carro usado a la amante"},
            {"type": "recetas_con_chisme", "topic": "La receta del arroz que curaba las penas de amor"},
            {"type": "bochinches", "topic": "Doña Rosa y su obsesión con las coplas de la iglesia"},
            {"type": "cuentos", "topic": "La leyenda del esposo desaparecido en la boda"},
            {"type": "bochinches", "topic": "La mujer que gasta más en uñas que en la renta"},
        ]
        self.current_topic_index = 0
    
    def get_next_topic(self):
        """Get the next topic from the queue"""
        if self.current_topic_index >= len(self.topic_queue):
            self.current_topic_index = 0
        
        topic_data = self.topic_queue[self.current_topic_index]
        self.current_topic_index += 1
        return topic_data
    
    def generate_script(self, topic):
        """Generate a script"""
        logger.info(f"Generating script for: {topic}")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": topic,
                    "content_type": "abuelita_meri",
                    "style": "humorous",
                    "length": 90,  # 90 minutes = 3 actos x 30 min each
                    "language": "spanish",
                    "voice_profile": self.voice_profile
                },
                timeout=300  # Longer timeout for 90-min script
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    script = result.get("script")
                    
                    # Parse raw_text if needed
                    if "raw_text" in script:
                        raw = script["raw_text"]
                        if "```json" in raw:
                            raw = raw.split("```json")[1].split("```")[0]
                        elif "```" in raw:
                            raw = raw.split("```")[1].split("```")[0]
                        raw = raw.strip()
                        try:
                            script = json.loads(raw)
                        except:
                            logger.error("Failed to parse script JSON")
                            return None
                    
                    # Count scenes based on format
                    if "actos" in script:
                        escena_count = sum(len(a.get("escenas", [])) for a in script.get("actos", []))
                        logger.info(f"Generated 3 actos with {escena_count} escenas (90 min)")
                    else:
                        scenes = script.get("scenes", [])
                        logger.info(f"Generated {len(scenes)} scenes")
                    return script
            
            logger.error("Script generation failed")
            return None
            
        except Exception as e:
            logger.error(f"Script error: {e}")
            return None
    
    def generate_images(self, scenes_or_script):
        """Generate images for scenes or full script with actos"""
        # Check if it's a script with actos
        if scenes_or_script and isinstance(scenes_or_script[0], dict) and "actos" in scenes_or_script[0]:
            logger.info("Generating images for 90-min script with actos structure")
            # Count total images: 3 acto + 9 escena = 12 images
            logger.info("Generating: 3 acto images + 9 escena images = 12 total")
        else:
            logger.info(f"Generating images for {len(scenes_or_script)} scenes")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": scenes_or_script,
                    "style": "3d_pixar"
                },
                timeout=900  # Longer timeout for 12 images
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    images = result.get("results", [])
                    success_count = sum(1 for img in images if img.get("success"))
                    logger.info(f"Generated {success_count}/{len(images)} images")
                    return images
            
            return []
            
        except Exception as e:
            logger.error(f"Image error: {e}")
            return []
    
    def generate_audio(self, scenes_or_script):
        """Generate audio for scenes or full script with actos"""
        # Check if it's a script with actos
        if scenes_or_script and isinstance(scenes_or_script[0], dict) and "actos" in scenes_or_script[0]:
            logger.info("Generating audio for 90-min script with actos structure")
            logger.info("Generating: 9 escena audio files")
        else:
            logger.info(f"Generating audio for {len(scenes_or_script)} scenes")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-audio",
                json={
                    "scenes": scenes_or_script,
                    "language": "spanish",
                    "gender": "female",
                    "voice_index": 0,
                    "engine": "edge",
                    "profile": self.voice_profile
                },
                timeout=900  # Longer timeout for 9 audio files
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    audio = result.get("results", [])
                    success_count = sum(1 for a in audio if a.get("success"))
                    logger.info(f"Generated {success_count}/{len(audio)} audio files")
                    return audio
            
            return []
            
        except Exception as e:
            logger.error(f"Audio error: {e}")
            return []
    
    def create_video(self, script, episode_type):
        """Create the final video"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"abuelita_meri_{episode_type}_{timestamp}"
        
        logger.info(f"Creating video: {project_name}")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/create-video",
                json={
                    "project_name": project_name,
                    "script": script,
                    "quality": "high"
                },
                timeout=1800  # 30 minutes timeout for 90-min video
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"Video created: {result.get('filepath')}")
                    return result
            
            return None
            
        except Exception as e:
            logger.error(f"Video error: {e}")
            return None
    
    def generate_thumbnail(self, title, episode_type):
        """Generate a thumbnail"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            width, height = 1280, 720
            img = Image.new('RGB', (width, height), color=(255, 140, 0))
            draw = ImageDraw.Draw(img)
            
            # Gradient
            for y in range(height):
                factor = y / height
                r = int(255 - factor * 50)
                g = int(140 + factor * 60)
                b = int(0 + factor * 100)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Text
            try:
                font = ImageFont.truetype("arial.ttf", 60)
                small_font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Title
            bbox = draw.textbbox((0, 0), title, font=font)
            x = (width - bbox[2] + bbox[0]) // 2
            y = height // 2 - 50
            draw.text((x, y), title, fill=(255, 255, 255), font=font)
            
            # Channel name
            channel = "Mi Abuelita Meri"
            bbox = draw.textbbox((0, 0), channel, font=small_font)
            x = (width - bbox[2] + bbox[0]) // 2
            draw.text((x, height - 100), channel, fill=(255, 255, 0), font=small_font)
            
            # Save
            thumbnail_dir = os.path.join(self.output_dir, "thumbnails")
            os.makedirs(thumbnail_dir, exist_ok=True)
            filename = f"thumbnail_{episode_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(thumbnail_dir, filename)
            img.save(filepath, "PNG")
            
            logger.info(f"Thumbnail saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Thumbnail error: {e}")
            return None
    
    def save_for_review(self, video_result, thumbnail, script, episode_type):
        """Save video and thumbnail to review folder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Clean episode title for folder name (SHORTEN to avoid path length issues)
            clean_title = script.get('title', episode_type)
            clean_title = clean_title.replace(' ', '_').replace('ñ', 'n').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            clean_title = ''.join(c for c in clean_title if c.isalnum() or c in '_-')
            # Shorten to first 30 chars
            clean_title = clean_title[:30]
            
            review_name = f"EP_{clean_title}_{timestamp}"
            
            # Create review folder
            review_folder = os.path.join(self.review_dir, review_name)
            os.makedirs(review_folder, exist_ok=True)
            logger.info(f"Created review folder: {review_folder}")
            
            # Create subfolders for organization
            images_folder = os.path.join(review_folder, "images")
            audio_folder = os.path.join(review_folder, "audio")
            os.makedirs(images_folder, exist_ok=True)
            os.makedirs(audio_folder, exist_ok=True)
            
            # Copy video - use shutil.copy with bytes mode
            if video_result and video_result.get("filepath"):
                import shutil
                import shutil as sh
                src = str(video_result["filepath"])
                dst = os.path.join(review_folder, f"{review_name}.mp4")
                logger.info(f"Copying video: {src} -> {dst}")
                try:
                    sh.copy(src, dst)
                    logger.info(f"Video saved: {dst}")
                except Exception as e:
                    logger.error(f"Video copy failed: {e}")
            
            # Copy thumbnail
            if thumbnail:
                import shutil as sh
                dst = os.path.join(review_folder, f"{review_name}_thumbnail.png")
                logger.info(f"Copying thumbnail: {thumbnail} -> {dst}")
                try:
                    sh.copy(thumbnail, dst)
                    logger.info(f"Thumbnail saved: {dst}")
                except Exception as e:
                    logger.error(f"Thumbnail copy failed: {e}")
            
            # Copy images
            try:
                if os.path.exists(self.server_images_dir):
                    for img_file in os.listdir(self.server_images_dir):
                        if img_file.endswith(('.png', '.jpg', '.jpeg')):
                            src = os.path.join(self.server_images_dir, img_file)
                            dst = os.path.join(images_folder, img_file)
                            shutil.copy2(src, dst)
                    logger.info(f"Images copied")
            except Exception as e:
                logger.error(f"Copy images error: {e}")
            
            # Copy audio
            try:
                if os.path.exists(self.server_audio_dir):
                    for audio_file in os.listdir(self.server_audio_dir):
                        if audio_file.endswith('.mp3'):
                            src = os.path.join(self.server_audio_dir, audio_file)
                            dst = os.path.join(audio_folder, audio_file)
                            shutil.copy2(src, dst)
                    logger.info(f"Audio copied")
            except Exception as e:
                logger.error(f"Copy audio error: {e}")
            
            # Save script
            script_path = os.path.join(review_folder, f"{review_name}_script.json")
            with open(script_path, 'w', encoding='utf-8') as f:
                json.dump(script, f, indent=2, ensure_ascii=False)
            logger.info(f"Script saved for review: {script_path}")
            
            # Count scenes
            if "actos" in script:
                escena_count = sum(len(a.get("escenas", [])) for a in script.get("actos", []))
                acto_count = len(script.get("actos", []))
                structure = f"{acto_count} Actos x {escena_count} Escenas"
            else:
                escena_count = len(script.get("scenes", []))
                structure = f"{escena_count} Scenes"
            
            # Create info file
            info_path = os.path.join(review_folder, "INFO.txt")
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"=========================================\n")
                f.write(f"  ABUELITA MERI - EPISODE PACKAGE\n")
                f.write(f"=========================================\n\n")
                f.write(f"Episode: {script.get('title', 'Unknown')}\n")
                f.write(f"Type: {episode_type}\n")
                f.write(f"Duration: 90 minutes\n")
                f.write(f"Structure: {structure}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"\n=========================================\n")
                f.write(f"  FOLDER CONTENTS\n")
                f.write(f"=========================================\n")
                f.write(f"- {review_name}.mp4 (Final Video)\n")
                f.write(f"- {review_name}_thumbnail.png (Thumbnail)\n")
                f.write(f"- {review_name}_script.json (Script)\n")
                f.write(f"- images/ (Scene images)\n")
                f.write(f"- audio/ (Audio files)\n")
                f.write(f"\n=========================================\n")
                f.write(f"  TO APPROVE & UPLOAD\n")
                f.write(f"=========================================\n")
                f.write(f"1. Watch the video\n")
                f.write(f"2. Check images/audio folders\n")
                f.write(f"3. If approved, move entire folder to: output/approved/\n")
                f.write(f"4. Upload video to YouTube\n")
            
            logger.info(f"\n=========================================")
            logger.info(f"EPISODE SAVED: {review_name}")
            logger.info(f"=========================================")
            logger.info(f"Folder: {review_folder}")
            logger.info(f"Review the video and move to 'approved' folder when ready")
            
            return review_folder
            
        except Exception as e:
            logger.error(f"Error saving for review: {e}")
            return None
    
    def create_episode(self):
        """Create one complete episode"""
        if self.daily_count >= self.max_daily_videos:
            logger.info(f"Daily limit reached ({self.max_daily_videos} videos)")
            return None
        
        # Get next topic
        topic_data = self.get_next_topic()
        topic = topic_data["topic"]
        episode_type = topic_data["type"]
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Creating 90-Minute Episode: {topic}")
        logger.info(f"Type: {episode_type}")
        logger.info(f"Structure: 3 Actos x 30 min x 3 Escenas = 9 scenes")
        logger.info(f"{'='*60}\n")
        
        # Step 1: Generate script (90 minutes)
        script = self.generate_script(topic)
        if not script:
            logger.error("Failed to generate script")
            return None
        
        # Step 2: Generate thumbnail
        title = script.get("title", topic)
        thumbnail = self.generate_thumbnail(title, episode_type)
        
        # Step 3: Generate images (send full script for actos/escenas structure)
        images = self.generate_images([script])  # Send as list with script
        
        # Step 4: Generate audio (send full script for actos/escenas structure)
        audio = self.generate_audio([script])  # Send as list with script
        
        # Step 5: Create video
        video = self.create_video(script, episode_type)
        
        if video:
            # Step 6: Save for review (NO UPLOAD)
            review_folder = self.save_for_review(video, thumbnail, script, episode_type)
            
            self.daily_count += 1
            logger.info(f"\n{'='*60}")
            logger.info(f"90-MINUTE EPISODE CREATED - WAITING FOR YOUR APPROVAL")
            logger.info(f"{'='*60}")
            logger.info(f"Video: {video.get('filepath')}")
            logger.info(f"Review folder: {review_folder}")
            logger.info(f"Daily count: {self.daily_count}/{self.max_daily_videos}")
            logger.info(f"\nTo approve and upload:")
            logger.info(f"1. Watch the video in the review folder")
            logger.info(f"2. Move the folder to 'output/approved/'")
            logger.info(f"3. Upload to YouTube manually")
            logger.info(f"{'='*60}\n")
            
            return {
                "video": video,
                "thumbnail": thumbnail,
                "script": script,
                "review_folder": review_folder
            }
        else:
            logger.error("Video creation failed")
            return None
    
    def run_scheduled(self):
        """Run on schedule"""
        logger.info("Starting Abuelita Meri Bot...")
        logger.info(f"Channel: {self.channel_name}")
        logger.info(f"Schedule: 9:00 AM, 2:00 PM, 7:00 PM")
        logger.info(f"Max daily videos: {self.max_daily_videos}")
        logger.info(f"Review folder: {self.review_dir}")
        logger.info(f"NO AUTO-UPLOAD - Videos saved for your approval")
        
        # Schedule content creation
        schedule.every().day.at("09:00").do(self.create_episode)
        schedule.every().day.at("14:00").do(self.create_episode)
        schedule.every().day.at("19:00").do(self.create_episode)
        
        # Reset daily count at midnight
        schedule.every().day.at("00:00").do(self.reset_daily_count)
        
        logger.info("\nBot is running! Press Ctrl+C to stop.\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
    
    def reset_daily_count(self):
        """Reset daily count"""
        self.daily_count = 0
        logger.info("Daily count reset")
    
    def run_now(self):
        """Create an episode immediately"""
        logger.info("Creating episode now...")
        return self.create_episode()


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("  Mi Abuelita Meri - Content Creator")
    print("  WITH REVIEW SYSTEM - NO AUTO-UPLOAD")
    print("="*60 + "\n")
    
    bot = AbuelitaMeriBot()
    
    print("Options:")
    print("1. Create one episode for review")
    print("2. Run scheduled automation (9 AM, 2 PM, 7 PM)")
    print("3. Create multiple episodes for review")
    print("4. Check pending reviews")
    
    choice = input("\nSelect option (1/2/3/4): ").strip()
    
    if choice == "1":
        bot.run_now()
    elif choice == "2":
        bot.run_scheduled()
    elif choice == "3":
        count = int(input("How many episodes? "))
        for i in range(count):
            print(f"\nCreating episode {i+1}/{count}")
            bot.run_now()
            if i < count - 1:
                print("Waiting 30 seconds before next episode...")
                time.sleep(30)
    elif choice == "4":
        review_dir = os.path.join("output", "for_review")
        if os.path.exists(review_dir):
            folders = os.listdir(review_dir)
            if folders:
                print(f"\nPending reviews ({len(folders)}):")
                for folder in folders:
                    print(f"  - {folder}")
                print(f"\nReview them in: {review_dir}")
            else:
                print("\nNo pending reviews")
        else:
            print("\nNo review folder found")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()