#!/usr/bin/env python3
"""
Mi Abuelita Meri - MEGA EPISODE CREATOR
10 Acts × 10 Minutes = 100 Minutes Total
10 Scenes per Act | 1 Image per Act
Church Drama Edition
"""

import os
import sys
import json
import time
import requests
import logging
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mega_episode.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MegaEpisodeCreator:
    """Creates 100-minute mega episodes with innuendo titles"""
    
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.channel_name = "Mi Abuelita Meri - Bochinches y Cuentos"
        self.voice_profile = "abuelita_meri"
        
        # Output directories
        self.output_dir = "output"
        self.review_dir = os.path.join(self.output_dir, "for_review")
        self.thumbnail_dir = os.path.join(self.output_dir, "thumbnails")
        os.makedirs(self.review_dir, exist_ok=True)
        os.makedirs(self.thumbnail_dir, exist_ok=True)
        
        # Innuendo title templates for church drama
        self.title_templates = [
            "La Pastora y el {secret} que {action} el Templo",
            "Cuando el {person} Descubrió el {secret} de la {location}",
            "El {scandal} que {action} a Toda la Congregación",
            "La {confession} que {shook} la Comunidad de Fe",
            "Doña {name} y el {mystery} del {place}",
            "El {secret} que la {person} No Quería que {reveal}",
            "La {revelation} del {day}: Lo que {happened} en el {place}",
            "Cuando {person} {action} y Todo {changed}",
            "El {incident} que {exposed} la {truth} del {place}",
            "La {scandal} del {time}: {what} {happened}"
        ]
        
        self.innuendo_words = {
            "secret": ["Secreto", "Misterio", "Pecado", "Verdade", "Confesión"],
            "action": ["Sacudió", "Conmovió", "Tembló", "Estremeció", "Sacudió"],
            "person": ["Pastora", "Diácono", "Corista", "Tesorera", "Ujier"],
            "location": ["Templo", "Sacristía", "Oficina", "Sótano", "Campanario"],
            "scandal": ["Escándalo", "Bochinche", "Lío", "Desastre", "Caos"],
            "confession": ["Confesión", "Revelación", "Verdad", "Historia", "Cuento"],
            "shook": ["Sacudió", "Conmovió", "Tembló", "Estremeció", "Impactó"],
            "name": ["Carmen", "Dolores", "Mercedes", "Consuelo", "Soledad"],
            "mystery": ["Misterio", "Secreto", "Enigma", "Puzzle", "Acertijo"],
            "place": ["Templo", "Iglesia", "Capilla", "Santuario", "Altar"],
            "reveal": ["Supiéramos", "Descubriéramos", "Conociéramos", "Viéramos"],
            "revelation": ["Revelación", "Verdad", "Historia", "Cuento", "Confesión"],
            "day": ["Domingo", "Sábado", "Viernes", "Miércoles", "Lunes"],
            "happened": ["Pasó", "Ocurrió", "Sucedió", "Aconteció", "Se desató"],
            "incident": ["Incidente", "Suceso", "Acontecimiento", "Evento", "Escándalo"],
            "exposed": ["Expuso", "Reveló", "Descubrió", "Mostró", "Sacó"],
            "truth": ["Verdad", "Realidad", "Historia", "Secreto", "Misterio"],
            "time": ["Medianoche", "Madrugada", "Atardecer", "Amanecer", "Noche"],
            "what": ["Lo que", "Aquello que", "Eso que", "Todo lo que"],
            "changed": ["Cambió", "Se transformó", "Se revolucionó", "Se derrumbó"]
        }
    
    def generate_innuendo_title(self):
        """Generate a catchy innuendo title for church drama"""
        template = self.title_templates[0]  # Fixed: use first template
        
        title = "La Pastora y el Secreto que Sacudió el Templo"
        
        # Add some variation
        variations = [
            "La Pastora y el Secreto que Sacudió el Templo",
            "Cuando el Diácono Descubrió el Misterio de la Sacristía",
            "El Escándalo que Conmovió a Toda la Congregación",
            "La Confesión que Sacudió la Comunidad de Fe",
            "Doña Carmen y el Misterio del Altar",
            "El Secreto que la Pastora No Quería que Supiéramos",
            "La Revelación del Domingo: Lo que Pasó en el Templo",
            "Cuando la Corista Cantó y Todo Cambió",
            "El Incidente que Expuso la Verdad del Templo",
            "La Escándalo de la Medianoche"
        ]
        
        # Randomly select one
        import random
        title = random.choice(variations)
        
        logger.info(f"Generated title: {title}")
        return title
    
    def generate_thumbnail(self, title):
        """Generate a cinematic thumbnail for the episode"""
        logger.info(f"Generating thumbnail for: {title}")
        
        try:
            width, height = 1280, 720
            img = Image.new('RGB', (width, height), color=(30, 0, 50))
            draw = ImageDraw.Draw(img)
            
            # Create dramatic gradient background
            for y in range(height):
                factor = y / height
                r = int(30 + factor * 80)
                g = int(0 + factor * 20)
                b = int(50 + factor * 100)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Add church silhouette
            church_points = [
                (400, 300), (450, 200), (500, 150), (550, 200), (600, 300),
                (600, 500), (400, 500)
            ]
            draw.polygon(church_points, fill=(20, 20, 40), outline=(100, 100, 150))
            
            # Add cross
            draw.rectangle([490, 100, 510, 200], fill=(200, 200, 220))
            draw.rectangle([450, 130, 550, 150], fill=(200, 200, 220))
            
            # Add text
            try:
                title_font = ImageFont.truetype("arial.ttf", 48)
                subtitle_font = ImageFont.truetype("arial.ttf", 32)
                channel_font = ImageFont.truetype("arial.ttf", 28)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                channel_font = ImageFont.load_default()
            
            # Title
            bbox = draw.textbbox((0, 0), title, font=title_font)
            x = (width - bbox[2] + bbox[0]) // 2
            y = height - 200
            draw.text((x, y), title, fill=(255, 215, 0), font=title_font)
            
            # Subtitle
            subtitle = "Mega Episodio - 100 Minutos"
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            x = (width - bbox[2] + bbox[0]) // 2
            draw.text((x, y + 60), subtitle, fill=(255, 255, 255), font=subtitle_font)
            
            # Channel name
            bbox = draw.textbbox((0, 0), self.channel_name, font=channel_font)
            x = (width - bbox[2] + bbox[0]) // 2
            draw.text((x, height - 60), self.channel_name, fill=(255, 200, 100), font=channel_font)
            
            # Save thumbnail
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thumbnail_church_drama_{timestamp}.png"
            filepath = os.path.join(self.thumbnail_dir, filename)
            img.save(filepath, "PNG")
            
            logger.info(f"Thumbnail saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Thumbnail error: {e}")
            return None
    
    def generate_act_script(self, act_number, title):
        """Generate a 10-minute script with 10 scenes for one act"""
        logger.info(f"Generating Act {act_number}/10 script")
        
        act_themes = [
            "Introducción y Presentación de Personajes",
            "El Descubrimiento del Secreto",
            "La Primera Confrontación",
            "Los Rumores se Esparcen",
            "La Confesión Inesperada",
            "El Escándalo Público",
            "La Búsqueda de la Verdad",
            "La Confrontación Final",
            "La Resolución del Misterio",
            "El Desenlace y las Consecuencias"
        ]
        
        theme = act_themes[act_number - 1]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": f"{title} - ACTO {act_number}: {theme} (10 minutos, 10 escenas)",
                    "content_type": "abuelita_meri",
                    "style": "dramatic",
                    "length": 10,
                    "language": "spanish",
                    "voice_profile": self.voice_profile
                },
                timeout=180
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
    
    def generate_image_for_act(self, act_number, title):
        """Generate ONE cinematic image for the entire act"""
        logger.info(f"Generating image for Act {act_number}")
        
        image_prompts = [
            "Church interior with dramatic lighting, pews, altar, stained glass windows, mysterious atmosphere",
            "Close-up of shocked faces in congregation, dramatic shadows, candlelight",
            "Two people arguing in church vestibule, dramatic tension, cinematic composition",
            "Whispering congregation, gossip spreading, dramatic lighting, shadows",
            "Person kneeling at confessional, emotional moment, dramatic lighting",
            "Crowd gathering outside church, scandal breaking, dramatic sky",
            "Detective-like investigation in church, clues, dramatic shadows",
            "Intense confrontation at altar, dramatic lighting, powerful emotions",
            "Truth revealed, dramatic revelation, cinematic lighting, emotional faces",
            "Final resolution, peaceful church, sunset through windows, hopeful atmosphere"
        ]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": [{"image_prompt": image_prompts[act_number - 1]}],
                    "style": "cinematic"
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
    
    def create_video_for_act(self, script, act_number, title):
        """Create video for one act"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = title.replace(" ", "_").replace("/", "_")[:30]
        project_name = f"mega_{safe_title}_act{act_number}_{timestamp}"
        
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
    
    def save_mega_episode(self, video_results, thumbnail, title, all_scripts):
        """Save the complete mega episode for review"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = title.replace(" ", "_").replace("/", "_")[:30]
            review_name = f"mega_{safe_title}_{timestamp}"
            
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
                    logger.info(f"Act {i+1} video saved: {dst}")
            
            # Copy thumbnail
            if thumbnail and os.path.exists(thumbnail):
                import shutil
                dst = os.path.join(review_folder, f"{review_name}_thumbnail.png")
                shutil.copy2(thumbnail, dst)
                logger.info(f"Thumbnail saved: {dst}")
            
            # Save scripts
            script_path = os.path.join(review_folder, f"{review_name}_scripts.json")
            with open(script_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "title": title,
                    "acts": all_scripts
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Scripts saved: {script_path}")
            
            # Create info file
            info_path = os.path.join(review_folder, "INFO.txt")
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(f"MEGA EPISODE: {title}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Format: 10 Acts × 10 Minutes = 100 Minutes Total\n")
                f.write(f"Scenes: 10 per Act = 100 Total\n")
                f.write(f"Images: 1 per Act = 10 Total\n")
                f.write(f"\nAct Structure:\n")
                for i in range(10):
                    f.write(f"  Act {i+1}: {['Introducción', 'Descubrimiento', 'Confrontación', 'Rumores', 'Confesión', 'Escándalo', 'Búsqueda', 'Confrontación Final', 'Resolución', 'Desenlace'][i]}\n")
                f.write(f"\nTO APPROVE:\n")
                f.write(f"1. Watch all 10 acts\n")
                f.write(f"2. If approved, move this folder to: output/approved/\n")
                f.write(f"3. Upload to YouTube as one 100-minute video\n")
            
            logger.info(f"\n{'='*60}")
            logger.info(f"MEGA EPISODE CREATED: {title}")
            logger.info(f"Location: {review_folder}")
            logger.info(f"Total Duration: ~100 minutes")
            logger.info(f"{'='*60}\n")
            
            return review_folder
            
        except Exception as e:
            logger.error(f"Error saving mega episode: {e}")
            return None
    
    def create_mega_episode(self):
        """Create the complete 100-minute mega episode"""
        logger.info(f"\n{'='*60}")
        logger.info(f"STARTING MEGA EPISODE CREATION")
        logger.info(f"{'='*60}\n")
        
        # Step 1: Generate catchy innuendo title
        title = self.generate_innuendo_title()
        
        # Step 2: Generate thumbnail
        thumbnail = self.generate_thumbnail(title)
        
        # Step 3: Create 10 acts
        video_results = []
        all_scripts = []
        
        for act_number in range(1, 11):
            logger.info(f"\n{'='*40}")
            logger.info(f"CREATING ACT {act_number}/10")
            logger.info(f"{'='*40}\n")
            
            # Generate script for this act
            script = self.generate_act_script(act_number, title)
            if not script:
                logger.error(f"Failed to generate script for Act {act_number}")
                continue
            
            all_scripts.append(script)
            
            # Generate ONE image for this act
            images = self.generate_image_for_act(act_number, title)
            
            # Generate audio for all scenes in this act
            audio = self.generate_audio_for_act(script)
            
            # Create video for this act
            video = self.create_video_for_act(script, act_number, title)
            
            if video:
                video_results.append(video)
                logger.info(f"✅ Act {act_number} completed successfully!")
            else:
                logger.error(f"❌ Failed to create video for Act {act_number}")
            
            # Small delay between acts
            time.sleep(2)
        
        # Step 4: Save everything for review
        if video_results:
            review_folder = self.save_mega_episode(video_results, thumbnail, title, all_scripts)
            return review_folder
        else:
            logger.error("No acts were created successfully")
            return None


def main():
    print("=" * 60)
    print("  Mi Abuelita Meri - MEGA EPISODE CREATOR")
    print("  Church Drama Edition")
    print("  10 Acts × 10 Minutes = 100 Minutes Total")
    print("  10 Scenes per Act | 1 Image per Act")
    print("=" * 60)
    
    creator = MegaEpisodeCreator()
    
    print("\nThis will create a complete 100-minute episode.")
    print("Estimated time: 30-45 minutes")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Create the mega episode
    result = creator.create_mega_episode()
    
    if result:
        print(f"\n✅ MEGA EPISODE CREATED SUCCESSFULLY!")
        print(f"📁 Location: {result}")
        print(f"📝 Review the videos and move to 'approved' folder when ready")
    else:
        print(f"\n❌ Failed to create mega episode")


if __name__ == "__main__":
    main()
