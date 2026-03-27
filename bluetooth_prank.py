#!/usr/bin/env python3
import bluetooth
import subprocess
import random
import time
import os
import signal
import threading
from pathlib import Path

# Konfigurasi
PRANK_SOUNDS = [
    "rickroll.mp3",
    "airhorn.mp3", 
    "fart.mp3",
    "scream.mp3",
    "police-siren.mp3"
]
BT_NAME = "FreeAirPods"  # Nama BT palsu
PRANK_INTERVAL = 300  # 5 menit

class BluetoothPrank:
    def __init__(self):
        self.server_sock = None
        self.is_running = True
        self.current_client = None
        
    def play_sound(self, sound_file):
        """Mainkan sound via PulseAudio"""
        cmd = f"paplay --volume=100000 {sound_file} &"
        subprocess.Popen(cmd, shell=True)
        print(f"🔊 Playing: {sound_file}")
    
    def play_random_prank(self):
        """Pilih dan mainkan prank random"""
        sound = random.choice(PRANK_SOUNDS)
        sound_path = f"/home/kali/pranks/{sound}"
        if os.path.exists(sound_path):
            self.play_sound(sound_path)

def audio_hijack(self):
    """Spam silence + loud noise untuk block musik"""
    # 1. Kirim silence burst (mute victim)
    subprocess.run(["paplay", "--volume=0", "/dev/zero"], 
                   stdout=subprocess.DEVNULL)
    
    # 2. Volume max prank
    subprocess.run(["paplay", "--volume=150000", "airhorn.mp3"])
    
    # 3. Rapid connect/disconnect (Bluetooth storm)
    subprocess.run(["bluetoothctl", "disconnect"])
    time.sleep(0.5)
    subprocess.run(["bluetoothctl", "connect", self.current_client[0]])
    
    def handle_client(self, sock, addr):
        """Handle client connection"""
        self.current_client = addr
        print(f"🎯 Victim connected: {addr}")
        
        # Auto prank setelah connect
        time.sleep(3)
        self.play_random_prank()
        
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
        except:
            pass
        finally:
            sock.close()
            print(f"👋 {addr} disconnected")
            self.current_client = None
    
    def signal_handler(self, sig, frame):
        self.is_running = False
    
    def run(self):
        """Main server loop"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Setup Bluetooth RFCOMM
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        
        port = self.server_sock.getsockname()[1]
        uuid = "00001101-0000-1000-8000-00805F9B34FB"  # Serial port UUID
        
        bluetooth.advertise_service(
            self.server_sock, 
            "PrankAudio",
            service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE]
        )
        
        print(f"🎭 BT Prank Server: {BT_NAME}")
        print(f"📡 Waiting for victims... (Ctrl+C to stop)")
        
        prank_timer = 0
        while self.is_running:
            try:
                sock, addr = self.server_sock.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(sock, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
                # Auto prank timer
                prank_timer += 1
                if prank_timer > PRANK_INTERVAL and not self.current_client:
                    self.play_random_prank()
                    prank_timer = 0
                    
            except bluetooth.BluetoothError:
                time.sleep(1)
        
        self.server_sock.close()

if __name__ == "__main__":
    prank = BluetoothPrank()
    prank.run()