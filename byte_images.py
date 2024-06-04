import io
from PIL import Image

# Open the PNG image
image = Image.open('/home/tg0014/Downloads/fruits.png')
# Create a byte stream
byte_stream = io.BytesIO()
image.save(byte_stream, format='PNG')

# Get the byte stream value
byte_stream_value = byte_stream.getvalue()

# You can use byte_stream_value as needed, for example, to write to a file or send over a network
print(byte_stream_value)
