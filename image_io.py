
import struct
import zlib


def _read_header_tokens(data, count):
   
    words = []
    i = 0
    n = len(data)
    while len(words) < count:
        while i < n and data[i] in b" \t\r\n":      # skip spaces / newlines
            i += 1
        if i < n and data[i] == ord("#"):           # skip a comment line
            while i < n and data[i] != ord("\n"):
                i += 1
            continue
        start = i
        while i < n and data[i] not in b" \t\r\n":  # read one word
            i += 1
        words.append(data[start:i].decode("ascii"))
    return words, i


def load_pgm(path):
    """
    Load a grayscale PGM file (P2 text or P5 binary) and return the image
    as a list of lists with values 0..255.
    """
    with open(path, "rb") as f:
        data = f.read()

    (magic, width, height, maxval), pos = _read_header_tokens(data, 4)
    width, height, maxval = int(width), int(height), int(maxval)

    if magic == "P5":
        pos += 1                                   # exactly one space after maxval
        pixels = list(data[pos:pos + width * height])   # each byte = one pixel
    elif magic == "P2":
        pixels = [int(word) for word in data[pos:].split()]
    else:
        raise ValueError("Not a grayscale PGM file (expected P2 or P5, got " + magic + ")")

    if len(pixels) != width * height:
        raise ValueError("File is damaged: wrong number of pixels")

    if maxval != 255:                              # rescale to our 0..255 range
        pixels = [round(p * 255 / maxval) for p in pixels]

    # Cut the long flat list into rows of `width` pixels.
    return [pixels[r * width:(r + 1) * width] for r in range(height)]


def save_pgm(image, path):
    """Save an image (list of lists) as a binary PGM (P5) file."""
    height = len(image)
    width = len(image[0])
    with open(path, "wb") as f:
        f.write(("P5\n" + str(width) + " " + str(height) + "\n255\n").encode("ascii"))
        for row in image:
            f.write(bytes(row))                    # list of ints 0..255 -> bytes


def _png_chunk(tag, body):
    """One PNG 'chunk': length + name + data + checksum."""
    return (struct.pack(">I", len(body)) + tag + body
            + struct.pack(">I", zlib.crc32(tag + body) & 0xFFFFFFFF))


def save_png(image, path):
  
    height = len(image)
    width = len(image[0])
    # Each PNG row starts with a "filter type" byte; 0 means "no filter".
    raw = b"".join(b"\x00" + bytes(row) for row in image)
    header = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)  # 8-bit grayscale
    png = (b"\x89PNG\r\n\x1a\n"
           + _png_chunk(b"IHDR", header)
           + _png_chunk(b"IDAT", zlib.compress(raw))
           + _png_chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
