import qrcode
import qrcode.image.svg

def qr(link):
    img = qrcode.make(link)
    img.save("qr.png")
    return "qr.png"