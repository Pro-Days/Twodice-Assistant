from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Sample data similar to the provided image
data = {
    "Rank": range(11, 21),
    "Name": [
        "_dice__",
        "RaPhic",
        "GOLD_yo",
        "AnyGate_124",
        "Doridor2_",
        "ONUNE",
        "dio7777",
        "Jajusamdasu",
        "toppvp",
        "Pro_Days",
    ],
    "Class": [
        "검객",
        "월사",
        "월사",
        "자객",
        "창술사",
        "자객",
        "법사",
        "검객",
        "월사",
        "검객",
    ],
    "Level": [
        "Lv.196",
        "Lv.196",
        "Lv.196",
        "Lv.196",
        "Lv.195",
        "Lv.195",
        "Lv.195",
        "Lv.195",
        "Lv.195",
        "Lv.195",
    ],
    "Registered": [
        True,
        True,
        False,
        True,
        False,
        False,
        True,
        True,
        False,
        True,
    ],
}

# Load sample images to simulate avatars
avatar_images = [
    "assets\\player_heads\\face.png",
] * 20
registered_true_image_path = "assets\\registered_true.png"
registered_false_image_path = "assets\\registered_false.png"

# Create a DataFrame
df = pd.DataFrame(data)

header_text = ["순위", "닉네임", "직업", "레벨", "등록"]
header_widths = [50, 250, 100, 100, 50]

# Image dimensions
header_height = 50
row_height = 50
avatar_size = 40
regi_size = 40
width, height = sum(header_widths), row_height * 10 + header_height

# Create a new image with white background
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.truetype("NanumGothic.ttf", 20)

# Draw the header
x_offset = -5
for i, text in enumerate(header_text):
    if i == 2:
        x_offset += 4
    elif i == 4:
        x_offset -= 4

    draw.text((x_offset + 12, 13), text, fill="black", font=font)
    x_offset += header_widths[i]


# Draw rows
for i, row in df.iterrows():
    y_offset = header_height + i * row_height
    x_offset = 0

    # Draw rank
    draw.text((x_offset + 12, y_offset + 13), str(row["Rank"]), fill="black", font=font)
    x_offset += header_widths[0]

    # Draw name and avatar
    avatar_image = Image.open(avatar_images[i % len(avatar_images)])
    avatar_image = avatar_image.resize((avatar_size, avatar_size))
    image.paste(avatar_image, (x_offset + 6, y_offset + 6))
    draw.text((x_offset + 62, y_offset + 13), row["Name"], fill="black", font=font)
    x_offset += header_widths[1]

    # Draw class
    draw.text((x_offset + 12, y_offset + 13), row["Class"], fill="black", font=font)
    x_offset += header_widths[2]

    # Draw level
    draw.text((x_offset + 12, y_offset + 13), row["Level"], fill="black", font=font)
    x_offset += header_widths[2]

    if row["Registered"]:
        registered_image = Image.open(registered_true_image_path).convert("RGBA")
    else:
        registered_image = Image.open(registered_false_image_path).convert("RGBA")
    registered_image = registered_image.resize((regi_size, regi_size))
    image.paste(registered_image, (x_offset + 6, y_offset + 6), registered_image)

    draw.line(
        [(header_widths[0], y_offset), (header_widths[0], y_offset + row_height)],
        fill="black",
        width=1,
    )
    draw.line(
        [
            (header_widths[0] + header_widths[1], y_offset),
            (header_widths[0] + header_widths[1], y_offset + row_height),
        ],
        fill="black",
        width=1,
    )
    draw.line(
        [
            (header_widths[0] + header_widths[1] + header_widths[2], y_offset),
            (
                header_widths[0] + header_widths[1] + header_widths[2],
                y_offset + row_height,
            ),
        ],
        fill="black",
        width=1,
    )
    draw.line(
        [
            (
                header_widths[0]
                + header_widths[1]
                + header_widths[2]
                + header_widths[3],
                y_offset,
            ),
            (
                header_widths[0]
                + header_widths[1]
                + header_widths[2]
                + header_widths[3],
                y_offset + row_height,
            ),
        ],
        fill="black",
        width=1,
    )

    draw.line(
        [
            (0, y_offset),
            (width, y_offset),
        ],
        fill="black",
        width=1,
    )

# Save the image
image.save("images\\rank_info.png")
