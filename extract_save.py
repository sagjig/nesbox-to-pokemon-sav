import sys
import os
import zlib

def extract_sram():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_save.py path/to/nesbox.save")
        return

    input_path = sys.argv[1]
    
    with open(input_path, 'rb') as f:
        raw_content = f.read()


    marker_nesbox_pk_savestate = b'\x0c\x00\x00\x00' # 0C 00 00 00
    
    marker_gen1_sram_start = b"\x00\x80\x00\x00" # 00 80 00 00
    size_gen1_sram = 32768 # 32 KiB


    decompress_file = True
    if (raw_content.startswith(marker_nesbox_pk_savestate)): # The 0C 00 00 00 marker denotes the start of a Pokemon save file (Gen 1,2)
        decompress_file = False
    
    if decompress_file:
        prior_size = sys.getsizeof(raw_content)
        data = zlib.decompress(raw_content)
        decomp_size = sys.getsizeof(data)
        print("Decompressed savestate file from " + str(prior_size) + " bytes to " + str(decomp_size) + " bytes.")
    else:
        data = raw_content

    # LLM: Construct the output name: batterysave_(original_name).sav
    dirname, full_filename = os.path.split(input_path)
    filename_base = os.path.splitext(full_filename)[0].replace(" ","_")
    output_name = f"batterysave_{filename_base}.sav"
    output_path = os.path.join(dirname, output_name)



    # LLM: Search for the SRAM block using the provided loop logic.
    for i in range(len(data) - size_gen1_sram): # For Gen 1, the SRAM block is 32 KiB (32,768 bytes) in size.
        if data[i : i + 4] == marker_gen1_sram_start: # For Gen 1, the marker is 00 80 00 00.
            offset = hex(i + 4)
            # LLM: Verify the tail size makes sense (SRAM is usually near the end)
            tail_size = len(data) - (i + 4 + size_gen1_sram)
            
            if 0 < tail_size < 1000: # TODO: There's some sweet-spot here that makes this work well with Gen 1 and 2 games. Find it
                sram_data = data[i + 4 : i + 4 + size_gen1_sram]
                
                with open(output_path, "wb") as f_out:
                    f_out.write(sram_data)
                
                print(f"SUCCESS: Extracted 32KB SRAM to '{output_path}'. Address: {offset}")
                break
            else:
                print(f"\tMarker at {offset} ignored (Tail size {tail_size} too large).")

if __name__ == "__main__":
    extract_sram()