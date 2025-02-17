import imghdr



ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp","jpeg.jpg"}
@staticmethod
def isAllowedFile(file):
        if not file:
             return False
     
        file_bytes = file.stream.read()
        file.seek(0)  # Reset file pointer after reading
    
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        return ext in ALLOWED_EXTENSIONS and imghdr.what(None, file_bytes) is not None