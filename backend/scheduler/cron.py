"""
Scheduler for running periodic vulnerability checks.
Uses APScheduler to run vulnerability scanning tasks at regular intervals.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from datetime import datetime

from backend.config import settings
from backend.services.alert_checker import alert_checker

logger = logging.getLogger(__name__)


class VulnerabilityScheduler:
    """Scheduler for vulnerability checking tasks."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": MemoryJobStore()},
            executors={"default": AsyncIOExecutor()},
            job_defaults={"coalesce": False, "max_instances": 1},
            timezone="UTC"
        )
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Set up scheduled jobs."""
        # Main vulnerability check job - runs every N hours based on config
        self.scheduler.add_job(
            func=self._run_vulnerability_check,
            trigger=IntervalTrigger(hours=settings.scraper_interval_hours),
            id='vulnerability_check',
            name='Vulnerability Check',
            replace_existing=True,
            max_instances=1  # Prevent overlapping runs
        )
        
        # Daily cleanup job - runs at 2 AM UTC
        self.scheduler.add_job(
            func=self._run_cleanup_tasks,
            trigger=CronTrigger(hour=2, minute=0),
            id='daily_cleanup',
            name='Daily Cleanup',
            replace_existing=True
        )
        
        # Weekly stats generation - runs on Sundays at 3 AM UTC
        self.scheduler.add_job(
            func=self._generate_weekly_stats,
            trigger=CronTrigger(day_of_week=6, hour=3, minute=0),
            id='weekly_stats',
            name='Weekly Statistics',
            replace_existing=True
        )
        
        logger.info(f"Scheduled vulnerability checks every {settings.scraper_interval_hours} hours")
    
    async def _run_vulnerability_check(self):
        """Run the main vulnerability checking process."""
        try:
            logger.info("Starting scheduled vulnerability check...")
            start_time = datetime.utcnow()
            
            await alert_checker.check_new_vulnerabilities()
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"Vulnerability check completed in {duration:.2f} seconds")
            
        except Exception as e:
            logger.error(f"Error during scheduled vulnerability check: {e}")
    
    async def _run_cleanup_tasks(self):
        """Run daily cleanup tasks."""
        try:
            logger.info("Starting daily cleanup tasks...")
            
            # Clean up old processed CVE/advisory tracking
            # (In a real implementation, you might want to persist this data)
            alert_checker.processed_cves.clear()
            alert_checker.processed_advisories.clear()
            
            logger.info("Daily cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup tasks: {e}")
    
    async def _generate_weekly_stats(self):
        """Generate weekly statistics."""
        try:
            logger.info("Generating weekly statistics...")
            
            # This could generate reports, send summary emails, etc.
            # For now, just log that it ran
            
            logger.info("Weekly statistics generation completed")
            
        except Exception as e:
            logger.error(f"Error generating weekly stats: {e}")
    
    def start(self):
        """Start the scheduler."""
        try:
            self.scheduler.start()
            logger.info("Vulnerability scheduler started")
            
            # Log next run times
            for job in self.scheduler.get_jobs():
                next_run = job.next_run_time
                logger.info(f"Job '{job.name}' next run: {next_run}")
                
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
    
    def shutdown(self):
        """Shutdown the scheduler."""
        try:
            self.scheduler.shutdown(wait=True)
            logger.info("Vulnerability scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
    
    def get_job_status(self):
        """Get status of all scheduled jobs."""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time,
                "trigger": str(job.trigger)
            })
        return jobs
    
    async def trigger_vulnerability_check(self):
        """Manually trigger a vulnerability check."""
        logger.info("Manually triggering vulnerability check...")
        await self._run_vulnerability_check()


# Global scheduler instance
scheduler = VulnerabilityScheduler()