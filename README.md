# Pure Python Image Processor

A small image processor written in **core Python only**. NumPy, OpenCV and Pillow are not used. An image is just a grid of numbers, and every operation here is plain Python loops over that grid. This is the same idea that image libraries and vehicle-perception pipelines (lane and obstacle detection) are built on.

## How an image is represented

A grayscale image is a list of lists. Each value is a brightness from 0 (black) to 255 (white), and pixels are accessed as `img[row][col]`.

```python
img = [
    [  0,   0, 255,   0,   0],
    [  0, 255, 255, 255,   0],
    [255, 255, 255, 255, 255],
    [  0, 255, 255, 255,   0],
    [  0,   0, 255,   0,   0],
]
```

> Replace the example above with the actual test image from your code.

## Design rule: no mutation

Every operation is its own function. It takes an image in and returns a **new** image. The original is never modified. This is checked in the demo by printing the original again after each operation.

## Project structure

```
.
├── imageproc.py   # all operations + demo
└── README.md
```

## How to run

Requires Python 3.10+. No installs needed.

```bash
python3 imageproc.py
```

## Functions

### Helpers

| Function | What it does |
|---|---|
| `print_image(img)` | Prints the grid in aligned columns so before/after can be compared by eye. |
| `clamp(value)` | Forces a value into the range 0 to 255. |

### Pixel-wise operations

Each output pixel depends only on the same pixel in the input.

| Function | What it does |
|---|---|
| `invert(img)` | Replaces each pixel `p` with `255 - p`. Dark becomes light and light becomes dark. |
| `adjust_brightness(img, amount)` | Adds `amount` to every pixel, clamped to 0 to 255. Negative values darken. |
| `threshold(img, cutoff)` | Pixels at or above `cutoff` become 255, the rest become 0, giving a black-and-white image. |

### Geometric operations

The values stay the same and their positions change.

| Function | What it does |
|---|---|
| `flip_horizontal(img)` | Mirrors the image left to right. |
| `flip_vertical(img)` | Mirrors the image top to bottom. |
| `rotate_90(img)` | Rotates 90° clockwise. Width and height swap. |
| `crop(img, top, left, height, width)` | Returns the selected rectangle. |

### Neighborhood operations

Each output pixel is computed from the pixel and its neighbors using a small grid of weights (a **kernel**).

| Function | What it does |
|---|---|
| `convolve(img, kernel)` | Slides the kernel over the image, multiplies each neighbor by its weight and sums the result. |
| `box_blur(img)` | Applies a 3x3 averaging kernel, which smooths the image. |
| `edge_detect(img)` | Applies a Sobel-style kernel, which highlights places where brightness changes sharply. |

#### Border handling

**Choice:** _(write your choice here: zero padding / edge replication / skip borders / shrink output)_

**Why:** _(explain in 2 to 3 sentences. For example: what happens to an edge pixel with missing neighbors, what trade-off your choice makes, and why it suits this use case.)_

## Output

Paste the real terminal output from your run under each heading, so a reader can verify it without running the code. Then add one or two sentences saying what to notice.

### Original

```
(paste output)
```

### Invert

```
(paste before/after)
```

What it shows: _(for example: every value is flipped around 127.5)_

### Brightness

```
(paste before/after)
```

What it shows: _(mention the clamping at 0 and 255)_

### Threshold

```
(paste before/after)
```

### Flip horizontal / vertical

```
(paste before/after)
```

### Rotate 90°

```
(paste before/after)
```

What it shows: _(use a non-square image so the dimension swap is visible)_

### Crop

```
(paste before/after)
```

### Box blur

```
(paste before/after)
```

What it shows: _(sharp transitions get softer; describe what happens at the borders)_

### Edge detection

```
(paste before/after)
```

What it shows: _(strong values appear where brightness changes, and flat regions go to 0)_

## Bonus (if completed)

- **PPM loading:** _(describe how the file is parsed: header, then pixel values)_
- **RGB support:** _(describe how operations are applied per channel)_

## What I learned / limitations

- Pure Python loops are slow on large images. Libraries like NumPy do the same work in optimized compiled code.
- _(add your own observation, for example about border effects or clamping)_

## Resources

- Setosa, *Image Kernels Explained Visually*: https://setosa.io/ev/image-kernels/
- Computerphile, *How Blurs & Filters Work* (YouTube)
- Wikipedia, *Kernel (image processing)* and *Netpbm format*
- MIT, *The Missing Semester of Your CS Education* (Shell & Git)
- The Odin Project, Git Basics
