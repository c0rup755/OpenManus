#!/usr/bin/env python3
"""
Mi Abuelita Meri - OPTIMIZED Content Creator
Creates 3 episodes per day (1.5+ hours total)
Each episode = 3 Acts (10 min each) = 30 min total
Only 1 image per act = 3 images per episode = FAST
"""

import os
import sys
import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('optimized_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OptimizedAbuelitaMeriBot:
    """Optimized content creator - 1 image per 10-min act"""
    
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.channel_name = "Mi Abuelita Meri - Bochinches y Cuentos"
        self.voice_profile = "abuelita_meri"
        self.daily_count = 0
        self.max_daily_videos = 3
        
        # Review folder
        self.review_dir = os.path.join("output", "for_review")
        os.makedirs(self.review_dir, exist_ok=True)
        
        # Approved folder
        self.approved_dir = os.path.join("output", "approved")
        os.makedirs(self.approved_dir, exist_ok=True)
        
        # Episode topics queue
        self.topic_queue = [
            {"type": "bochinches", "topic": "Doña Carmen se cree la dueña del barrio pero nadie la respeta"},
            {"type": "bochinches", "topic": "El hijo de la vecina que se fue a 'buscar trabajo' a Orlando"},
            {"type": "bochinches", "topic": "La pastora del templo que tiene un novio secreto"},
            {"type": "cuentos", "topic": "La Llorona del río Grande de Loíza"},
            {"type": "cuentos", "topic": "El Cuco que vivía debajo de la cama de Dorotea"},
            {"type": "cuentos", "topic": "Los duendes del cafetal de Jayuya"},
        ]
        self.topic_index = 0
    
    def get_next_topic(self):
        """Get next topic from queue"""
        if self.topic_index >= len(self.topic_queue):
            self.topic_index = 0
        topic = self.topic_queue[self.topic_index]
        self.topic_index += 1
        return topic
    
    def generate_script(self, topic, act_number=1, total_acts=3):
        """Generate a 10-minute script for one act"""
        logger.info(f"Generating Act {act_number}/{total_acts} script for: {topic}")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": f"{topic} - ACT {act_number} of {total_acts} (10 minutes)",
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
                    logger.info(f"Generated Act {act_number} with {len(scenes)} scenes")
                    return script
            
            logger.error(f"Script generation failed for Act {act_number}")
            return None
            
        except Exception as e:
            logger.error(f"Script error for Act {act_number}: {e}")
            return None
    
    def generate_image_for_act(self, act_number, episode_type):
        """Generate ONE image for the entire 10-minute act"""
        logger.info(f"Generating image for Act {act_number}")
        
        try:
            # Create a single image prompt for the entire act
            image_prompt = f"3D Pixar style cinematic scene, Abuelita Meri the matriarch, {episode_type} episode Act {act_number}, Caribbean setting, vibrant colors, dramatic lighting, 4K quality"
            
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": [{"image_prompt": image_prompt}],
                    "style": "3d_pixar"
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    images = result.get("results", [])
                    success_count = sum(1 for img in images if img.get("success"))
                    logger.info(f"Generated {success_count} image for Act {act_number}")
                    return images
            
            return []
            
        except Exception as e:
            logger.error(f"Image error for Act {act_number}: {e}")
            return []
    
    def generate_audio_for_act(self, script):
        """Generate audio for all scenes in an act"""
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
                    success_count = sum(1 for a in audio if a.get("success"))
                    logger.info(f"Generated {success_count}/{len(audio)} audio files")
                    return audio
            
            return []
            
        except Exception as e:
            logger.error(f"Audio error: {e}")
            return []
    
    def create_video_for_act(self, script, episode_type, act_number):
        """Create video for one act"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"abuelita_meri_{episode_type}_act{act_number}_{timestamp}"
        
        logger.info(f"Creating video for Act {act_number}: {project_name}")
        
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
                    logger.info(f"Video created for Act {act_number}: {result.get('filepath')}")
                    return result
            
            return None
            
        except Exception as e:
            logger.error(f"Video error for Act {act_number}: {e}")
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
    
    def save_for_review(self, video_results, thumbnail, script, episode_type):
        """Save all acts for review"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            review_name = f"{episode_type}_{timestamp}"
            
            # Create review folder
            review_folder = os.path.join(self.review_dir, review_name)
            os.makedirs(review_folder, exist_ok=True)
            
            # Copy videos
            for i, video_result in enumerate(video_results):
                if video_result and video_result.get("filepath"):
                    import shutil
                    src = video_result["filepath"]
                    dst = os.path.join(review_folder, f"{review_name}_act{i+1}.mp4")
                    shutil.copy2(src, dst)
                    logger.info(f"Act {i+1} video saved for review: {dst}")
            
            # Copy thumbnail
            if thumbnail and os.path.exists(thumbnail):
                import shutil
                dst = os.path.join(review_folder, f"{review_name}_thumbnail.png")
                shutil.copy2(thumbnail, dst)
                logger.info(f"Thumbnail saved for review: {dst}")
            
            # Save script
            script_path = os.path.join(review_folder, f"{review_name}_script.json")
            with open(script_path, 'w', encoding='utf-8') as f:
                json.dump(script, f, indent=2, ensure_ascii=False)
            logger.info(f"Script saved for review: {script_path}")
            
            # Create info file
            info_path = os.path.join(review_folder, "INFO.txt")
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"Episode: {script.get('title', 'Unknown')}\n")
                f.write(f"Type: {episode_type}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Acts: {len(video_results)} (10 min each)\n")
                f.write(f"Total Duration: ~30 minutes\n")
                f.write(f"\nTO APPROVE:\n")
                f.write(f"1. Watch all 3 acts\n")
                f.write(f"2. If approved, move this folder to: output/approved/\n")
                f.write(f"3. Upload to YouTube manually\n")
            
            logger.info(f"\nContent saved for review in: {review_folder}")
            logger.info(f"Review the videos and move to 'approved' folder when ready")
            
            return review_folder
            
        except Exception as e:
            logger.error(f"Error saving for review: {e}")
            return None
    
    def create_episode(self):
        """Create one complete episode (3 acts = 30 minutes)"""
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
        logger.info(f"Format: 3 Acts (10 min each) = 30 min total")
        logger.info(f"{'='*60}\n")
        
        # Generate thumbnail
        title = f"Act 1: {topic}"
        thumbnail = self.generate_thumbnail(title, episode_type)
        
        # Create 3 acts
        video_results = []
        all_scripts = []
        
        for act_number in range(1, 4):
            logger.info(f"\n--- Creating Act {act_number}/3 ---")
            
            # Step 1: Generate script for this act
            script = self.generate_script(topic, act_number, 3)
            if not script:
                logger.error(f"Failed to generate script for Act {act_number}")
                continue
            
            all_scripts.append(script)
            
            # Step 2: Generate ONE image for this act
            images = self.generate_image_for_act(act_number, episode_type)
            
            # Step 3: Generate audio for all scenes in this act
            audio = self.generate_audio_for_act(script)
            
            # Step 4: Create video for this act
            video = self.create_video_for_act(script, episode_type, act_number)
            
            if video:
                video_results.append(video)
                logger.info(f"Act {act_number} completed successfully!")
            else:
                logger.error(f"Failed to create video for Act {act_number}")
        
        if video_results:
            # Save for review
            review_folder = self.save_for_review(video_results, thumbnail, {"title": topic, "acts": all_scripts}, episode_type)
            
            self.daily_count += 1
            logger.info(f"\nEpisode created with {len(video_results)}/3 acts!")
            logger.info(f"Daily progress: {self.daily_count}/{self.max_daily_videos}")
            
            return review_folder
        else:
            logger.error("No acts were created successfully")
            return None
    
    def run_now(self):
        """Create one episode now"""
        logger.info("Creating episode now...")
        return self.create_episode()
    
    def run_scheduled(self):
        """Run on schedule (9 AM, 2 PM, 7 PM)"""
        import schedule
        
        def job():
            self.create_episode()
        
        # Schedule for 9 AM, 2 PM, 7 PM
        schedule.every().day.at("09:00").do(job)
        schedule.every().day.at("14:00").do(job)
        schedule.every().day.at("19:00").do(job)
        
        logger.info("Scheduled for 9 AM, 2 PM, 7 PM")
        logger.info("Press Ctrl+C to stop")
        
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    print("=" * 60)
    print("  Mi Abuelita Meri - OPTIMIZED Content Creator")
    print("  3 Acts × 10 min = 30 min per episode")
    print("  1 image per act = FAST generation")
    print("=" * 60)
    
    bot = OptimizedAbuelitaMeriBot()
    
    print("\nOptions:")
    print("1. Create one episode (3 acts = 30 min)")
    print("2. Run scheduled automation (9 AM, 2 PM, 7 PM)")
    print("3. Create multiple episodes")
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
