import base64

def encode(filename):
    """Encode a file with a content which any other word reader/text editor cannot read unless decoded"""
    with open(filename, "rb") as file:
        data = file.read()
    return base64.b64encode(data)

def decode(filename):
    """Decode a file so that the encoded content can be decoded/decrypted to make it readable."""
    with open(filename, "rb") as file:
        data = file.read()
    return base64.b64decode(data)