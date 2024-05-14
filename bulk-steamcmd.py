import os
import subprocess
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

def download_mod(mod_id, steamcmd_path, game_id):
    cmd = [
        steamcmd_path,
        '+login', 'anonymous',
        '+workshop_download_item', game_id, mod_id,
        '+quit'
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        logger.info(f"Successfully downloaded mod {mod_id}")
    else:
        logger.error(f"Failed to download mod {mod_id}: {result.stderr.decode('utf-8', errors='ignore')}")

def move_mod(mod_id, steamapps_dir, workshop_dir):
    mod_dir = os.path.join(steamapps_dir, mod_id)
    if os.path.exists(mod_dir):
        destination_dir = os.path.join(workshop_dir, mod_id)
        os.makedirs(destination_dir, exist_ok=True)
        for item in os.listdir(mod_dir):
            s = os.path.join(mod_dir, item)
            d = os.path.join(destination_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        shutil.rmtree(mod_dir)  # Remove original mod directory
        logger.info(f"Moved mod {mod_id} to {destination_dir}")
    else:
        logger.warning(f"Mod directory for {mod_id} does not exist")

def download_and_move_mod(mod_id, steamcmd_path, game_id, steamapps_dir, workshop_dir):
    download_mod(mod_id, steamcmd_path, game_id)
    move_mod(mod_id, steamapps_dir, workshop_dir)

def main(mods_file, steamcmd_path, game_id, workshop_dir):
    try:
        with open(mods_file, 'r', encoding='utf-8') as file:
            mods = [line.split()[0] for line in file.readlines() if line.strip()]

        steamapps_dir = os.path.join('SteamCMD', 'steamapps', 'workshop', 'content', game_id)

        with ThreadPoolExecutor(max_workers=4) as executor:
            for mod_id in mods:
                executor.submit(download_and_move_mod, mod_id, steamcmd_path, game_id, steamapps_dir, workshop_dir)
                
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Subprocess error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    logger = setup_logging()
    
    mods_file = "mods.txt"  # The file containing the list of mod IDs
    steamcmd_path = r"C:\path\to\steamcmd.exe"  # Path to steamcmd executable
    game_id = "108600"  # Game ID for the mods you want to download
    workshop_dir = r"C:\path\to\workshop\mods"  # Directory where mods will be moved

    main(mods_file, steamcmd_path, game_id, workshop_dir)
