#!/usr/bin/env python3
"""
Automated Content Scheduler
Runs OpenManus agent to create content on a schedule
"""

import os
import sys
import time
import schedule
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from content_creator import ContentCreatorAgent


class ContentScheduler:
    """Schedule automated content creation"""
    
    def __init__(self):
        self.agent = ContentCreatorAgent()
        self.content_count = 0
        self.max_daily_content = 3
        
    def create_scheduled_content(self):
        """Create content based on schedule"""
        logger.info("Starting scheduled content creation...")
        
        if self.content_count >= self.max_daily_content:
            logger.info(f"Daily limit reached ({self.max_daily_content} videos)")
            return
        
        try:
            # Research trending topics
            topics = self.agent.research_trending_topics()
            
            # Create content for the first topic
            if topics:
                topic = topics[0]
                result = self.agent.create_content(topic)
                
                if result:
                    self.content_count += 1
                    logger.info(f"Content created successfully. Total today: {self.content_count}")
                else:
                    logger.error("Content creation failed")
            
        except Exception as e:
            logger.error(f"Error in scheduled content creation: {e}")
    
    def reset_daily_count(self):
        """Reset the daily content count"""
        self.content_count = 0
        logger.info("Daily content count reset")
    
    def run_scheduler(self):
        """Run the scheduler"""
        logger.info("Starting Content Scheduler...")
        
        # Schedule content creation
        # Create content at 9 AM, 2 PM, and 7 PM
        schedule.every().day.at("09:00").do(self.create_scheduled_content)
        schedule.every().day.at("14:00").do(self.create_scheduled_content)
        schedule.every().day.at("19:00").do(self.create_scheduled_content)
        
        # Reset daily count at midnight
        schedule.every().day.at("00:00").do(self.reset_daily_count)
        
        logger.info("Scheduler configured:")
        logger.info("  - Content creation at 9:00 AM, 2:00 PM, 7:00 PM")
        logger.info("  - Daily limit: 3 videos")
        logger.info("  - Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {e}")


def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         Content Scheduler                                  ║
    ║         Automated Video Content Generation                 ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    scheduler = ContentScheduler()
    scheduler.run_scheduler()


if __name__ == "__main__":
    main()