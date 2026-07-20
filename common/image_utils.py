from PIL import Image, ImageChops


def autocrop_blank_margin(image, padding=10, threshold=30):
    """Crop away a uniform blank/background margin around the subject.

    The background color is sampled from the image's four corners. Pixels
    that differ from it by more than `threshold` are treated as the subject;
    the crop box is expanded by `padding` pixels (clamped to the image
    bounds). Returns the original image unchanged if no such margin is found.
    """
    rgb_image = image.convert("RGB") if image.mode != "RGB" else image

    corners = [
        rgb_image.getpixel((0, 0)),
        rgb_image.getpixel((rgb_image.width - 1, 0)),
        rgb_image.getpixel((0, rgb_image.height - 1)),
        rgb_image.getpixel((rgb_image.width - 1, rgb_image.height - 1)),
    ]
    bg_color = tuple(sum(channel) // len(corners) for channel in zip(*corners))

    background = Image.new("RGB", rgb_image.size, bg_color)
    diff = ImageChops.difference(rgb_image, background)
    diff = ImageChops.add(diff, diff, 2.0, -threshold)
    bbox = diff.getbbox()

    if bbox is None:
        return image

    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)

    return image.crop((left, top, right, bottom))
