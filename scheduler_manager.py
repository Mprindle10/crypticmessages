#!/usr/bin/env python3
"""
Cryptic Message Scheduler Service Runner
Handles starting, stopping, and monitoring the automated delivery system
"""

import os
import sys
import signal
import subprocess
import time
from pathlib import Path
import logging
import json
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SchedulerManager:
    def __init__(self):
        self.scheduler_process = None
        self.pid_file = Path("scheduler.pid")
        self.log_file = Path("scheduler.log")
        
    def start_scheduler(self):
        """Start the scheduler service"""
        if self.is_running():
            logger.info("Scheduler is already running")
            return True
            
        try:
            # Start the scheduler process
            self.scheduler_process = subprocess.Popen([
                sys.executable, "scheduler_service.py"
            ], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
            )
            
            # Save PID
            with open(self.pid_file, 'w') as f:
                f.write(str(self.scheduler_process.pid))
                
            logger.info(f"Scheduler started with PID: {self.scheduler_process.pid}")
            
            # Give it a moment to start
            time.sleep(2)
            
            if self.scheduler_process.poll() is None:
                logger.info("Scheduler service is running successfully")
                return True
            else:
                logger.error("Scheduler failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}")
            return False
    
    def stop_scheduler(self):
        """Stop the scheduler service"""
        if not self.is_running():
            logger.info("Scheduler is not running")
            return True
            
        try:
            # Read PID from file
            if self.pid_file.exists():
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                    
                # Send SIGTERM to gracefully stop
                os.kill(pid, signal.SIGTERM)
                
                # Wait for process to stop
                timeout = 10
                while timeout > 0:
                    try:
                        os.kill(pid, 0)  # Check if process exists
                        time.sleep(1)
                        timeout -= 1
                    except OSError:
                        # Process no longer exists
                        break
                
                if timeout == 0:
                    # Force kill if still running
                    logger.warning("Force killing scheduler process")
                    os.kill(pid, signal.SIGKILL)
                
                # Clean up PID file
                self.pid_file.unlink()
                logger.info("Scheduler stopped successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")
            return False
    
    def is_running(self):
        """Check if scheduler is currently running"""
        if not self.pid_file.exists():
            return False
            
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
                
            # Check if process exists
            os.kill(pid, 0)
            return True
            
        except (OSError, ValueError):
            # PID file exists but process doesn't
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False
    
    def restart_scheduler(self):
        """Restart the scheduler service"""
        logger.info("Restarting scheduler service")
        self.stop_scheduler()
        time.sleep(2)
        return self.start_scheduler()
    
    def get_status(self):
        """Get detailed status of the scheduler"""
        status = {
            'running': self.is_running(),
            'pid': None,
            'uptime': None,
            'log_size': 0,
            'last_log_entry': None
        }
        
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    status['pid'] = int(f.read().strip())
            except:
                pass
                
        if self.log_file.exists():
            try:
                status['log_size'] = self.log_file.stat().st_size
                
                # Get last log entry
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        status['last_log_entry'] = lines[-1].strip()
            except:
                pass
                
        return status
    
    def tail_logs(self, lines=50):
        """Show recent log entries"""
        if not self.log_file.exists():
            logger.info("No log file found")
            return
            
        try:
            with open(self.log_file, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                
            print(f"\n--- Last {len(recent_lines)} log entries ---")
            for line in recent_lines:
                print(line.rstrip())
                
        except Exception as e:
            logger.error(f"Error reading logs: {str(e)}")

def main():
    manager = SchedulerManager()
    
    if len(sys.argv) < 2:
        print("Usage: python scheduler_manager.py {start|stop|restart|status|logs}")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    
    if command == "start":
        if manager.start_scheduler():
            print("✅ Scheduler started successfully")
            print("\nScheduled delivery times:")
            print("- Sunday: 8:00 AM")
            print("- Wednesday: 6:00 PM")
            print("- Friday: 3:00 PM")
        else:
            print("❌ Failed to start scheduler")
            sys.exit(1)
            
    elif command == "stop":
        if manager.stop_scheduler():
            print("✅ Scheduler stopped successfully")
        else:
            print("❌ Failed to stop scheduler")
            sys.exit(1)
            
    elif command == "restart":
        if manager.restart_scheduler():
            print("✅ Scheduler restarted successfully")
        else:
            print("❌ Failed to restart scheduler")
            sys.exit(1)
            
    elif command == "status":
        status = manager.get_status()
        print(f"\n📊 Scheduler Status:")
        print(f"Running: {'✅ Yes' if status['running'] else '❌ No'}")
        if status['pid']:
            print(f"PID: {status['pid']}")
        print(f"Log file size: {status['log_size']} bytes")
        if status['last_log_entry']:
            print(f"Last log: {status['last_log_entry']}")
            
    elif command == "logs":
        lines = 50
        if len(sys.argv) > 2:
            try:
                lines = int(sys.argv[2])
            except ValueError:
                pass
        manager.tail_logs(lines)
        
    else:
        print("Unknown command. Use: start|stop|restart|status|logs")
        sys.exit(1)

if __name__ == "__main__":
    main()
