#!/usr/bin/env python3
"""
OpenManus Content Creator Integration
Automatically creates content using your Content Creator Studio
"""

import os
import sys
import json
import asyncio
import requests
from datetime import datetime
from pathlib import Path

# Add OpenManus to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agent.manus import Manus
from app.config import config


class ContentCreatorAgent:
    """Autonomous agent for creating video content"""
    
    def __init__(self):
        self.api_base = "http://localhost:5000"
        self.output_dir = Path("../workspace/output")
        self.topics = []
        self.scheduled_content = []
        
    def research_trending_topics(self, category="entertainment"):
        """Research trending topics for content creation"""
        print(f"[Agent] Researching trending topics in {category}...")
        
        # This would use OpenManus to browse and find topics
        # For now, return sample topics
        sample_topics = [
            "Celebrity drama that shocked everyone this week",
            "The most viral moments on social media",
            "Behind the scenes secrets from famous movies",
            "Unbelievable true stories that went viral",
            "The biggest plot twists in reality TV history"
        ]
        
        return sample_topics
    
    def generate_script(self, topic, content_type="abuelita_meri", style="dramatic", length=3):
        """Generate a script using the Content Creator Studio API"""
        print(f"[Agent] Generating script for: {topic}")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-script",
                json={
                    "topic": topic,
                    "content_type": content_type,
                    "style": style,
                    "length": length,
                    "language": "spanish",
                    "voice_profile": "abuelita_meri"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[Agent] Script generated successfully")
                    return result.get("script")
            
            print(f"[Agent] Script generation failed: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"[Agent] Error generating script: {e}")
            return None
    
    def generate_images(self, scenes, style="cinematic"):
        """Generate images for each scene"""
        print(f"[Agent] Generating images for {len(scenes)} scenes...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-images",
                json={
                    "scenes": scenes,
                    "style": style
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[Agent] Images generated successfully")
                    return result.get("results")
            
            print(f"[Agent] Image generation failed")
            return []
            
        except Exception as e:
            print(f"[Agent] Error generating images: {e}")
            return []
    
    def generate_audio(self, scenes, profile="abuelita_meri"):
        """Generate audio for each scene"""
        print(f"[Agent] Generating audio for {len(scenes)} scenes...")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/generate-audio",
                json={
                    "scenes": scenes,
                    "language": "spanish",
                    "gender": "female",
                    "voice_index": 0,
                    "engine": "edge",
                    "profile": profile
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[Agent] Audio generated successfully")
                    return result.get("results")
            
            print(f"[Agent] Audio generation failed")
            return []
            
        except Exception as e:
            print(f"[Agent] Error generating audio: {e}")
            return []
    
    def create_video(self, script, project_name, quality="high"):
        """Create the final video"""
        print(f"[Agent] Creating video: {project_name}")
        
        try:
            response = requests.post(
                f"{self.api_base}/api/create-video",
                json={
                    "project_name": project_name,
                    "script": script,
                    "quality": quality
                },
                timeout=600
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"[Agent] Video created: {result.get('filepath')}")
                    return result
            
            print(f"[Agent] Video creation failed")
            return None
            
        except Exception as e:
            print(f"[Agent] Error creating video: {e}")
            return None
    
    def create_content(self, topic, content_type="abuelita_meri", style="dramatic", length=3):
        """Complete content creation pipeline"""
        print(f"\n{'='*60}")
        print(f"[Agent] Starting content creation for: {topic}")
        print(f"{'='*60}\n")
        
        # Step 1: Generate script
        script = self.generate_script(topic, content_type, style, length)
        if not script:
            print("[Agent] Failed to generate script. Aborting.")
            return None
        
        # Extract scenes
        scenes = script.get("scenes", [])
        if not scenes:
            print("[Agent] No scenes found in script. Aborting.")
            return None
        
        # Step 2: Generate images
        images = self.generate_images(scenes, style)
        if not images:
            print("[Agent] Warning: No images generated")
        
        # Step 3: Generate audio
        audio = self.generate_audio(scenes, "abuelita_meri")
        if not audio:
            print("[Agent] Warning: No audio generated")
        
        # Step 4: Create video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"auto_{content_type}_{timestamp}"
        video = self.create_video(script, project_name, "high")
        
        if video:
            print(f"\n[Agent] Content creation complete!")
            print(f"[Agent] Video saved to: {video.get('filepath')}")
            return video
        else:
            print(f"\n[Agent] Video creation failed")
            return None
    
    def run_scheduled_content(self, count=1):
        """Create multiple pieces of content automatically"""
        print(f"\n[Agent] Starting automated content creation for {count} videos")
        
        # Research topics
        topics = self.research_trending_topics()
        
        results = []
        for i, topic in enumerate(topics[:count]):
            print(f"\n[Agent] Creating content {i+1}/{count}")
            result = self.create_content(topic)
            if result:
                results.append(result)
        
        print(f"\n[Agent] Automation complete. Created {len(results)}/{count} videos.")
        return results


def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         OpenManus Content Creator Agent                    ║
    ║         Automated Video Content Generation                 ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    agent = ContentCreatorAgent()
    
    # Example: Create one piece of content
    topic = "The biggest celebrity drama of the week"
    agent.create_content(topic)
    
    # Or run automated content creation
    # agent.run_scheduled_content(count=3)


if __name__ == "__main__":
    main()