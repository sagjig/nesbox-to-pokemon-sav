# nesbox-to-pokemon-sav

## Overview and disclosures
In layman's terms: Convert a NESbox save of a Gen 1 Pokémon game into a .sav file, for use with Game Boy emulators, [PkHex](https://projectpokemon.org/home/files/file/1-pkhex/), etc.

In complex terms: Extracts the SRAM data from a NESBox/VBA-like save-state.

Please note that this script was written with assistance from an LLM (namely, Google Gemini). I have checked and rewritten/refactored lines of code as necessary myself, and all research prior to the script was done myself. None of the documentation in this README was written with an LLM.

I've only tested this with the Flash-based version of NESBox, but any version of it should use the same save-state format.

## Usage
Usage: `python3 extract_save.py /path/to/nesbox.save`
The input save-state can be either compressed or not. If compressed, the script will auto-decompress it for usage. If for whatever reason this fails you can also [manually decompress your save-state here](https://savefileconverter.com/#/utilities/advanced) (select zlib or gzip, both work fine).


## Explanation and instructions
[NESBox's Game Boy emulator](https://github.com/nesbox/libnesbox/blob/master/src/gb/core/gb/GB.cpp#L3619) uses a seemingly modified version of the [VisualBoyAdvance save-state format](https://github.com/visualboyadvance-m/visualboyadvance-m/blob/master/src/core/gb/gb.cpp#L3529) (version 12). With regard to Pokémon games, this data actually contains the SRAM data (what is used in a typical .sav file). 

Thus, this script:
1. Decompresses the NESBox save from its zlib compression, if necessary.
2. Searches the raw binary for strings of `00 80 00 00`. This should mark the start of SRAM (AKA the .sav) data for a Generation 1 Pokémon game in NESBox/VBA save-state format.
- If you end up having to do this manually in a hex editor, you'll see this appears a few times. Try to find the `00 80 00 00` near lots of other structured-looking data with `50`s near it. Per [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_I)#English), `50` is the English-language string terminator in Gen 1 games).
- 00 80 00 00 is VBA's format saying that the following SRAM data is 32,768 bytes (or, in hexadecimal, `8000` bytes) in size. It's not used by Pokémon saves themselves.
3. Extract the next 32 KiB (32,768 bytes) of data, as this is the size of Gen 1 SRAM data.
4. Output it as a .sav file, named batterysave-originalFilename.sav

For posterity, here's a quick writeup of how to then load the .sav file in VBA and mGBA. 
- VBA: File>Import>Battery file...>select outputted .sav file. Then, Emulation>Reset.
- mGBA: File>Load alternative save game...>select outputted .sav file. mGBA should auto-reset for you.
- Alternatively, or for most other emulators, simply name it the exact same name as your ROM (i.e., if your ROM is named "Pokémon Red (USA).gb", name your save "Pokémon Red (USA).sav"). Then launch or reload the game. The startup screen should show CONTINUE with your save.


## Special thanks
- Bulbapedia for their excellent [Gen 1 savedata breakdown](https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_I)) and [Gen 1 character encoding article](https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_I)#English).
- [Save File Converter](https://savefileconverter.com/#/utilities/advanced) for the zlib decompressor.
  - Strangely enough, VBA docs say it uses gzip, but changing it to zlib worked better in my code...I guess zlib doesn't put any magic-numbers. Gzip does, but our save-files don't add any to the header, so VBA/NESBox might just use zlib?
- [Hexed.it](https://hexed.it/), a very nice online hex-editor.
- The [NESBox](https://nesbox.com/) developer (particularly for the Flash version)
- The [VisualBoyAdvance](https://github.com/visualboyadvance-m) team.
