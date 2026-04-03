#!/usr/bin/env python3
"""
Mi Abuelita Meri - CORRECT Structure
10 Acts × 1 Scene (10 min) = 10 Scenes Total
OR
10 Acts × 2 Scenes (5 min each) = 20 Scenes Total
"""

import os
import json
import time
import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class CorrectEpisodeCreator:
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.voice_profile = "abuelita_meri"
    
    def generate_script(self, act_number, title):
        """Generate ONE 10-minute scene per act"""
        logger.info(f"Generating Act {act_number}/10...")
        
        act_themes = [
            "Meri llega al templo y nota algo raro",
            "Encuentra la primera pista",
            "Los rumores se esparcen",
            "Meri sabe quién es el culpable",
            "La confrontación cara a cara",
            "La confesión sale a la luz",
            "El escándalo público",
            "Meri dicta sentencia",
            "La redención",
            "El desenlace final"
        ]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": f"{title} - ACTO {act_number}: {act_themes[act_number-1]}",
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
                    
                    # LIMIT TO 2 SCENES MAX!
                    scenes = script.get("scenes", [])
                    if len(scenes) > 2:
                        # Keep only first 2 scenes
                        scenes = scenes[:2]
                        script["scenes"] = scenes
                    
                    logger.info(f"  Act {act_number}: {len(scenes)} scene(s)")
                    return script
            
            return None
            
        except Exception as e:
            logger.error(f"  Error: {e}")
            return None
    
    def generate_image(self, act_number):
        """Generate ONE image per act"""
        prompts = [
            "Caribbean church exterior at sunset",
            "Church interior with stained glass",
            "Two women whispering in pew",
            "Congregation gossiping",
            "Confrontation at altar",
            "Emotional confession",
            "Chaos in church",
            "Judge at pulpit",
            "Forgiveness moment",
            "Peaceful ending with sunset"
        ]
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": [{"image_prompt": prompts[act_number-1]}],
                    "style": "cinematic"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"  Image generated")
                    return result.get("results", [])
            
            return []
            
        except Exception as e:
            logger.error(f"  Image error: {e}")
            return []
    
    def generate_audio(self, script):
        """Generate audio for scenes"""
        scenes = script.get("scenes", [])
        logger.info(f"  Generating audio for {len(scenes)} scene(s)...")
        
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
                    logger.info(f"  Audio: {success} file(s)")
                    return audio
            
            return []
            
        except Exception as e:
            logger.error(f"  Audio error: {e}")
            return []
    
    def create_video(self, script, act_number):
        """Create video for one act"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"act{act_number}_{timestamp}"
        
        logger.info(f"  Creating video...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/create-video",
                json={
                    "project_name": project_name,
                    "script": script,
                    "quality": "medium"
                },
                timeout=600
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"  ✅ Video done!")
                    return result
            
            logger.error(f"  ❌ Video failed")
            return None
            
        except Exception as e:
            logger.error(f"  Video error: {e}")
            return None
    
    def run(self):
        """Create all 10 acts"""
        title = "Cuando el Diácono Descubrió el Misterio de la Sacristía"
        
        print("=" * 60)
        print(f"  TITLE: {title}")
        print(f"  Structure: 10 Acts × 1-2 Scenes = 10-20 Total")
        print("=" * 60)
        print()
        
        for act in range(1, 11):
            print(f"\n--- ACT {act}/10 ---")
            
            # Generate script (1-2 scenes only!)
            script = self.generate_script(act, title)
            if not script:
                continue
            
            # Generate image
            self.generate_image(act)
            
            # Generate audio
            self.generate_audio(script)
            
            # Create video
            self.create_video(script, act)
            
            print()
        
        print("\n" + "=" * 60)
        print("  DONE! Check workspace/output/videos/")
        print("=" * 60)


if __name__ == "__main__":
    creator = CorrectEpisodeCreator()
    creator.run()
