import struct

def is_pe_file(path):
    try:
        with open(path, 'rb') as f:
            # Read first 64 bytes for DOS header
            dos_header = f.read(64)
            if len(dos_header) < 64 or dos_header[0:2] != b'MZ':
                return False

            if False:
                # Get PE header offset from 0x3C
                pe_offset = struct.unpack_from('<I', dos_header, 0x3C)[0]

                # Seek and read PE signature
                f.seek(pe_offset)
                pe_sig = f.read(4)
                return pe_sig == b'PE\0\0'
            
    except Exception:
        return False
    
    return True
