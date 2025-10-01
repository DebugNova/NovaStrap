"""
NovaStrap Icon Creator
Converts the NovaStrap logo to .ico format for Windows application
"""
from PIL import Image
import os

def create_icon_from_image(image_path, output_path='novastrap.ico'):
    """
    Convert an image to Windows .ico format with multiple sizes.
    
    Args:
        image_path: Path to source image
        output_path: Path for output .ico file
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create icon with multiple sizes (Windows standard)
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Save as .ico with multiple sizes
        img.save(
            output_path,
            format='ICO',
            sizes=icon_sizes
        )
        
        print(f"[OK] Icon created successfully: {output_path}")
        print(f"  Sizes included: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating icon: {e}")
        return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("NovaStrap Icon Creator")
    print("=" * 60)
    print()
    
    # Check if logo file exists
    logo_files = ['novastrap_logo.png', 'logo.png', 'icon.png', 'novastrap.png']
    source_image = None
    
    for logo_file in logo_files:
        if os.path.exists(logo_file):
            source_image = logo_file
            break
    
    if not source_image:
        print("Please place your NovaStrap logo image in this folder as:")
        print("  - novastrap_logo.png (recommended)")
        print("  - logo.png")
        print("  - icon.png")
        print()
        print("Then run this script again.")
        return 1
    
    print(f"Found logo: {source_image}")
    print()
    
    # Create the icon
    if create_icon_from_image(source_image, 'novastrap.ico'):
        print()
        print("[OK] Icon is ready!")
        print()
        print("Next steps:")
        print("1. Run: pyinstaller NovaStrap.spec")
        print("2. Find your app in: dist/NovaStrap.exe")
        print("3. Double-click to run - no console window!")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())

