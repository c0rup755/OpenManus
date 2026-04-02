#!/usr/bin/env python3
"""
Mi Abuelita Meri - Autonomous Content Creator
Runs continuously and creates content automatically
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
    """Autonomous content creator for Mi Abuelita Meri channel"""
    
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.channel_name = "Mi Abuelita Meri - Bochinches y Cuentos"
        self.voice_profile = "abuelita_meri"
        self.daily_count = 0
        self.max_daily_videos = 3
        
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
                    "length": 10,  # 10-minute episodes
                    "language": "spanish",
                    "voice_profile": self.voice_profile
                },
                timeout=180
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
                    
                    scenes = script.get("scenes", [])
                    logger.info(f"Generated {len(scenes)} scenes")
                    return script
            
            logger.error("Script generation failed")
            return None
            
        except Exception as e:
            logger.error(f"Script error: {e}")
            return None
    
    def generate_images(self, scenes):
        """Generate images for scenes"""
        logger.info(f"Generating images for {len(scenes)} scenes")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": scenes,
                    "style": "3d_pixar"
                },
                timeout=600
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
    
    def generate_audio(self, scenes):
        """Generate audio for scenes"""
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
                timeout=600
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
                timeout=900
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
            thumbnail_dir = os.path.join("output", "thumbnails")
            os.makedirs(thumbnail_dir, exist_ok=True)
            filename = f"thumbnail_{episode_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(thumbnail_dir, filename)
            img.save(filepath, "PNG")
            
            logger.info(f"Thumbnail saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Thumbnail error: {e}")
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
        logger.info(f"Creating Episode: {topic}")
        logger.info(f"Type: {episode_type}")
        logger.info(f"{'='*60}\n")
        
        # Step 1: Generate script
        script = self.generate_script(topic)
        if not script:
            logger.error("Failed to generate script")
            return None
        
        # Step 2: Generate thumbnail
        title = script.get("title", topic)
        thumbnail = self.generate_thumbnail(title, episode_type)
        
        # Step 3: Generate images
        scenes = script.get("scenes", [])
        images = self.generate_images(scenes)
        
        # Step 4: Generate audio
        audio = self.generate_audio(scenes)
        
        # Step 5: Create video
        video = self.create_video(script, episode_type)
        
        if video:
            self.daily_count += 1
            logger.info(f"\nEpisode created successfully!")
            logger.info(f"Video: {video.get('filepath')}")
            logger.info(f"Thumbnail: {thumbnail}")
            logger.info(f"Daily count: {self.daily_count}/{self.max_daily_videos}")
            
            return {
                "video": video,
                "thumbnail": thumbnail,
                "script": script
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
                time.sleep(60)  # Check every minute
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
    print("  Mi Abuelita Meri - Autonomous Content Creator")
    print("  Bochinches, Cuentos, y Mareas de Oro")
    print("="*60 + "\n")
    
    bot = AbuelitaMeriBot()
    
    # Ask user what to do
    print("Options:")
    print("1. Create one episode now")
    print("2. Run scheduled automation (9 AM, 2 PM, 7 PM)")
    print("3. Create multiple episodes now")
    
    choice = input("\nSelect option (1/2/3): ").strip()
    
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
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()