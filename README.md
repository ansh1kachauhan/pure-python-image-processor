# Pure Python Image Processor

A small image processor written in **core Python only**. NumPy, OpenCV and Pillow are not used. An image is just a grid of numbers, and every operation here is plain Python loops over that grid. This is the same idea that image libraries and vehicle-perception pipelines (lane and obstacle detection) are built on.

## How an image is represented

A grayscale image is a list of lists. Each value is a brightness from 0 (black) to 255 (white), and pixels are accessed as `img[row][col]`.

```python
img = [
        [255, 10,  10,  10,  10],
        [10,  10,  200, 200, 10],
        [10,  10,  200, 200, 10],
        [10,  10,  10,  10,  10],
        [10,  10,  10,  10,  60],
    
]
```

> e.

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


## Output

### Original

```
<img width="1876" height="891" alt="original" src="https://github.com/user-attachments/assets/37da7800-408a-4f7a-ad3a-285490760fae" />


```

### Invert

```
<img width="1876" height="891" alt="invert" src="https://github.com/user-attachments/assets/1fd23608-8be5-452e-8bc6-e4e1fb1ae3bd" />

```

What it shows: _(for example: every value is flipped around 127.5)_

### Brightness

```
<img width="1876" height="891" alt="brightness_plus_60" src="https://github.com/user-attachments/assets/b187b15f-d2e4-4257-874e-321a3242ad2b" />

```

What it shows: _(mention the clamping at 0 and 255)_

### Threshold

```
<img width="1876" height="891" alt="threshold_128" src="https://github.com/user-attachments/assets/b5f3d708-44fc-4274-b9a3-bc573b983d6c" />

```

### Flip horizontal / vertical

```
<img width="1876" height="891" alt="flip_horizontal" src="https://github.com/user-attachments/assets/7eb593b8-e937-4389-9dc4-ddd51f20cc5d" />

```

### Rotate 90°

```
<img width="891" height="1876" alt="rotate_90" src="https://github.com/user-attachments/assets/79b35252-e677-49d3-ae97-62903decf435" />

```

What it shows: _(use a non-square image so the dimension swap is visible)_

### Crop

```
<img width="938" height="445" alt="crop_center" src="https://github.com/user-attachments/assets/8c0c2add-76bc-4917-b7e0-6a0b2435f271" />

```

### Box blur

```
<img width="1876" height="891" alt="box_blur" src="https://github.com/user-attachments/assets/e0dbdd4e-15d9-476c-a9b6-c40da24d9f3f" />

```

What it shows: _(sharp transitions get softer; describe what happens at the borders)_

### Edge detection

```
<img width="1876" height="891" alt="edge_detect" src="https://github.com/user-attachments/assets/1ea18dea-41a6-4f55-83d6-2ec283ccc358" />

```

What it shows: _(strong values appear where brightness changes, and flat regions go to 0)_


## What I learned / limitations

- Pure Python loops are slow on large images. Libraries like NumPy do the same work in optimized compiled code.
-

## Resources

- Setosa, *Image Kernels Explained Visually*: https://setosa.io/ev/image-kernels/
- Computerphile, *How Blurs & Filters Work* (YouTube)
- Wikipedia, *Kernel (image processing)* and *Netpbm format*
- MIT, *The Missing Semester of Your CS Education* (Shell & Git)
- The Odin Project, Git Basics
