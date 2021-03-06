from PIL import Image

def main():
    MAX_WIDTH = 512
    MAX_HEIGHT = 512

    p = 1
    q = 1

    im = Image.open('WilliamPittSelfie.jpg').convert('1')
    width = im.width
    height = im.height
    yModifier = (height - MAX_WIDTH) / 2
    xModifier = (width - MAX_HEIGHT) / 2
    top = yModifier
    bottom = height - yModifier
    left = xModifier
    right = width - xModifier
    cropped = im.crop((left, top, right, bottom))
    cropped.save('binary.png')

    new = Image.new('1', (cropped.width, cropped.height))

    for y in range(cropped.height):
        for x in range(cropped.width):
            px = cropped.getpixel((x, y))
            N = cropped.width
            newX = (x + y * p) % N
            newY = (x * q + y * (p * q + 1)) % N
            new.putpixel((newX, newY), px)

    new.save('copied.png')

    count_width = int(cropped.width / 4)
    count_height = int(cropped.height / 4)

    count = Image.new('1', (count_width, count_height))

    for y in range(0, new.height, 4):
        for x in range(0, new.width, 4):
            pix_sum = 0
            for i in range(16):
                coords = (x + (i % 4), y + int(i / 4))
                add = new.getpixel(coords)
                pix_sum += add
            count.putpixel((int(x / 4), int(y / 4)),
                           1 if pix_sum % 2 == 0 else 0)

    count.save('final.png')
    count = Image.open('final.png').convert('1')

    zag = Image.new('1', (count.height, count.width))

    x = 0
    y = 0
    xDir = 1
    yDir = 1
    passedCorner = False
    for i in range(count.width**2):
        zag.putpixel((i % count.width, int(i / count.width)),
                     count.getpixel((x, y)))

        doSwapY = y - yDir < 0 or y - yDir >= count.height
        doSwapX = x + xDir >= count.width or x + xDir < 0

        if doSwapX and doSwapY:
            passedCorner = True
            x -= xDir

        if not doSwapX:
            if passedCorner and doSwapY:
                x -= xDir
            else:
                x += xDir
        if not doSwapY:
            if passedCorner and doSwapX:
                y += yDir
            else:
                y -= yDir

        if doSwapX or doSwapY:
            yDir *= -1
            xDir *= -1

    zag.save('zag.png')


main()
