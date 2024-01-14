# Export Completion to Depressurizer

## Requirements

- Playnite
- Have Python for Windows (`py`) installed and available on the `PATH`.
- Depressurizer installed, with an `%APPDATA%/depressurizer` configuration directory

## Usage

- Install into playnite. 
- Click Extensions > Export for Depressurizer
- Wait for "Saved" message box
- Open the "playnite" profile in Depressurizer

## How it Works

The powershell script exports your current view's games and their collection status to a CSV table. Then the playniteToDepressurizer.py script converts that CSV file into a depressurizer profile
