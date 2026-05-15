# nesbox-to-pokemon-sav
In layman's terms: Convert a NESbox save-state into a Gen 1 Pokémon battery save.
In complex terms: Extracts the SRAM data from a NESBox/VBA-like save-state.

Please note that this script was written with assistance from an LLM (namely, Google Gemini). I have checked and rewritten/refactored lines of code as necessary myself, and all research prior to the script was done myself. None of the documentation here was written with an LLM.

Usage: `python3 extract_save.py /path/to/nesbox.save`

NESBox's Game Boy emulator uses a seemingly modified version of the VisualBoyAdvance save-state format (version 12). With regard to Pokémon games, this data actually contains the SRAM data (what is used in a typical .sav file). 


This script:
1. Decompresses the NESBox save from its gz compression, if necessary.
2. Searches the raw binary for strings of `00 80 00 00`. This should mark the start of SRAM (AKA the .sav) data for a Generation 1 Pokémon game in NESBox/VBA save-state format.
(If you end up having to do this manually in a hex editor, you'll see this appears a few times. Try to find the `00 80 00 00` near lots of other structured-looking data with `50`s near it. `50` is the string terminator in Gen 1 games).
3. Extract the next 32 KiB (32,768 bytes) of data, as this is the size of Gen 1 SRAM data.
4. Output it as a .sav file, named batterysave-originalFilename.sav

For posterity, here's a quick writeup of how to then load the .sav file in VBA and mGBA. 
- VBA: File>Import>Battery file...>select outputted .sav file. Then, Emulation>Reset.
- mGBA: File>Load alternative save game...>select outputted .sav file. mGBA should auto-reset for you.
- Alternatively, or for most other emulators, simply name it the exact same name as your ROM (i.e., if your ROM is named "Pokémon Red (USA).gb", name your save "Pokémon Red (USA).sav"). Then launch or reload the game. The startup screen should show CONTINUE with your save.
