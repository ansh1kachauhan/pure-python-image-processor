def make_sample_image():
    return [
        [255, 10,  10,  10,  10],
        [10,  10,  200, 200, 10],
        [10,  10,  200, 200, 10],
        [10,  10,  10,  10,  10],
        [10,  10,  10,  10,  60],
    ]


def print_image(title, image):
    print(title)
    for row in image:
        line = ""
        for value in row:
            line += "{:>4}".format(value)
        print(line)
    print()


def clamp(value):
    value = int(round(value))
    if value < 0:
        return 0
    if value > 255:
        return 255
    return value


def copy_image(image):
    return [row[:] for row in image]


def images_equal(a, b):
    return a == b


def invert(image):
    result = []
    for row in image:
        new_row = []
        for value in row:
            new_row.append(255 - value)
        result.append(new_row)
    return result


def adjust_brightness(image, amount):
    result = []
    for row in image:
        new_row = []
        for value in row:
            new_row.append(clamp(value + amount))
        result.append(new_row)
    return result


def threshold(image, cutoff):
    result = []
    for row in image:
        new_row = []
        for value in row:
            if value > cutoff:
                new_row.append(255)
            else:
                new_row.append(0)
        result.append(new_row)
    return result


def flip_horizontal(image):
    return [row[::-1] for row in image]


def rotate_90_clockwise(image):
    old_rows = len(image)
    old_cols = len(image[0])
    result = []
    for c in range(old_cols):
        new_row = []
        for r in range(old_rows - 1, -1, -1):
            new_row.append(image[r][c])
        result.append(new_row)
    return result


def crop(image, top, left, height, width):
    result = []
    for r in range(top, top + height):
        result.append(image[r][left:left + width])
    return result


def get_pixel(image, r, c, border="replicate"):
    rows = len(image)
    cols = len(image[0])
    inside = 0 <= r < rows and 0 <= c < cols
    if inside:
        return image[r][c]
    if border == "zero":
        return 0
    r = max(0, min(r, rows - 1))
    c = max(0, min(c, cols - 1))
    return image[r][c]


def apply_kernel(image, kernel, divisor=1, border="replicate"):
    rows = len(image)
    cols = len(image[0])
    result = []
    for r in range(rows):
        new_row = []
        for c in range(cols):
            total = 0
            for kr in range(-1, 2):
                for kc in range(-1, 2):
                    neighbor = get_pixel(image, r + kr, c + kc, border)
                    weight = kernel[kr + 1][kc + 1]
                    total += neighbor * weight
            new_row.append(clamp(total / divisor))
        result.append(new_row)
    return result


def box_blur(image, border="replicate"):
    kernel = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
    return apply_kernel(image, kernel, divisor=9, border=border)


def edge_detect(image, border="replicate"):
    kernel = [
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0],
    ]
    return apply_kernel(image, kernel, divisor=1, border=border)


def show(title, operation_name, before, after):
    print("=" * 50)
    print(title)
    print("=" * 50)
    print_image("BEFORE:", before)
    print_image("AFTER  (" + operation_name + "):", after)


def main():
    original = make_sample_image()
    backup = copy_image(original)

    print_image("ORIGINAL 5x5 IMAGE (0 = black, 255 = white):", original)

    show("1) INVERT", "255 - value", original, invert(original))
    show("2) BRIGHTNESS +50 (values clamped at 255)", "value + 50",
         original, adjust_brightness(original, 50))
    show("3) THRESHOLD at 100 (above 100 -> 255, else 0)", "threshold 100",
         original, threshold(original, 100))

    show("4) FLIP HORIZONTAL (mirror left/right)", "flip",
         original, flip_horizontal(original))
    show("5) ROTATE 90 DEGREES CLOCKWISE", "rotate",
         original, rotate_90_clockwise(original))
    show("6) CROP the 2x2 bright block (top=1, left=2, 2x2)", "crop",
         original, crop(original, 1, 2, 2, 2))

    show("7) BOX BLUR 3x3, border = replicate", "blur",
         original, box_blur(original, border="replicate"))
    show("8) EDGE DETECTION 3x3, border = replicate", "edges",
         original, edge_detect(original, border="replicate"))

    print("=" * 50)
    print("9) BORDER COMPARISON on the blur")
    print("=" * 50)
    print("Look at the corners and edges: 'zero' pulls them toward black,")
    print("'replicate' keeps them closer to the real neighbors.\n")
    print_image("Blur with border = replicate:", box_blur(original, "replicate"))
    print_image("Blur with border = zero:", box_blur(original, "zero"))

    print("=" * 50)
    print("10) CHECK: original unchanged?")
    print("=" * 50)
    print("Original still equals the backup:", images_equal(original, backup))


if __name__ == "__main__":
    main()