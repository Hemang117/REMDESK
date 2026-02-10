import os
from PIL import Image

def convert_to_webp(directory):
    print(f"Scanning {directory}...")
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                webp_path = os.path.splitext(file_path)[0] + ".webp"
                
                try:
                    img = Image.open(file_path)
                    img.save(webp_path, 'webp', quality=80)
                    print(f"✅ Converted: {file} -> {os.path.basename(webp_path)}")
                except Exception as e:
                    print(f"❌ Failed: {file} ({e})")

if __name__ == "__main__":
    convert_to_webp("core/static")
    convert_to_webp("talenthub/static")
