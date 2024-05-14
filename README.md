# Bulk-SteamCMD

Downloads and organizes Steam Workshop mods in bulk for any Steam game using SteamCMD.

## Download

Clone the repository:
```bash
git clone https://github.com/Zadeson/bulk-steamcmd.git
cd bulk-steamcmd
```

## Setup

1. Create `mods.txt` in the project directory with one mod ID per line.

2. Edit `bulk-steamcmd.py` to set paths and game ID:
   ```python
   if __name__ == "__main__":
       logger = setup_logging()
       
       mods_file = "mods.txt"
       steamcmd_path = r"C:\path\to\steamcmd.exe"
       game_id = "108600"
       workshop_dir = r"C:\path\to\workshop\mods"

       main(mods_file, steamcmd_path, game_id, workshop_dir)
   ```

## Usage

Run the script:
```bash
python bulk-steamcmd.py
```
