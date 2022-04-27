import qrcode
import qrcode.image.svg

def qr(link, filetype):
    img = qrcode.make(link)
    if filetype == "png":
        filename = "./qr/png"
    elif filetype == "svg":
        filename = "./qr/svg"
    img.save(filename)
    return filename