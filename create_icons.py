import struct
import zlib

def create_png(width, height, r, g, b, filename):
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    # width(4), height(4), bit_depth(1), color_type(1), compression(1), filter(1), interlace(1)
    # color_type 2 is Truecolor
    ihdr_data = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data) & 0xffffffff
    png += struct.pack("!I", len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack("!I", ihdr_crc)
    
    # IDAT chunk
    # Just a solid color. Uncompressed data:
    # Each row is: filter_type(1 byte) + pixel_data(width * 3 bytes)
    row = b'\x00' + bytes([r, g, b]) * width
    raw_data = row * height
    compressed_data = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed_data) & 0xffffffff
    png += struct.pack("!I", len(compressed_data)) + b'IDAT' + compressed_data + struct.pack("!I", idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND') & 0xffffffff
    png += struct.pack("!I", 0) + b'IEND' + struct.pack("!I", iend_crc)
    
    with open(filename, 'wb') as f:
        f.write(png)

create_png(192, 192, 10, 13, 17, 'icon-192.png')
create_png(512, 512, 10, 13, 17, 'icon-512.png')
print("Icons created.")
