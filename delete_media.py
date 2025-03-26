import os
import shutil
from django.conf import settings
import django

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Fluroscence_backend.settings')
django.setup()

def delete_media():
    """
    Delete all files and subdirectories in the media directory
    while preserving the media directory itself.
    """
    media_root = settings.MEDIA_ROOT
    
    if not os.path.exists(media_root):
        print(f"Media directory does not exist: {media_root}")
        return
    
    # Count files before deletion
    file_count = 0
    for root, dirs, files in os.walk(media_root):
        file_count += len(files)
    
    # Delete all files and subdirectories in media directory
    for item in os.listdir(media_root):
        item_path = os.path.join(media_root, item)
        
        if os.path.isfile(item_path):
            os.remove(item_path)
            print(f"Deleted file: {item_path}")
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            print(f"Deleted directory: {item_path}")
    
    print(f"Successfully deleted {file_count} files from media directory.")

if __name__ == "__main__":
    # Execute when run directly
    delete_media()
