"""
Simple artwork downloader using direct Wikimedia Commons file URLs
"""

import requests
from pathlib import Path
import time

BASE_DIR = Path(__file__).parent.parent / "data" / "artworks"

# Simplified URLs directly from Wikimedia Commons with proper escaping
SIMPLE_URLS = {
    "Picasso": {
        3: "https://collectionapi.metmuseum.org/api/collection/v1/iiif/490116/1156672/main-image",
        4: "https://www.artic.edu/iiif/2/e966799b-97ee-1cc6-bd2f-a94b4b8bb8f9/full/843,/0/default.jpg",
        5: "https://www.philamuseum.org/images/cagallery_detectors/227821-63-0-1.jpg",
        6: "https://www.clevelandart.org/sites/default/files/webpublic/1978.63_web_0.jpg",
        7: "https://ids.si.edu/ids/deliveryService/id/NPG_NPG201656_SQ",
        8: "https://images.metmuseum.org/CRDImages/ep/original/DT1567.jpg",
        9: "https://www.tate.org.uk/art/images/work/N/N05/N05857_10.jpg",
    },
    "Monet": {
        0: "https://images.metmuseum.org/CRDImages/ep/original/DT1932.jpg",
        3: "https://images.metmuseum.org/CRDImages/ep/original/DT2146.jpg",
        4: "https://images.metmuseum.org/CRDImages/ep/original/DT1505.jpg",
        5: "https://images.metmuseum.org/CRDImages/ep/original/DT2059.jpg",
        6: "https://www.artic.edu/iiif/2/3c27b499-af56-f0d5-93b5-a7f2f1ad5813/full/843,/0/default.jpg",
        7: "https://www.artic.edu/iiif/2/34745f60-0151-be94-61ad-56b24f30462c/full/843,/0/default.jpg",
        8: "https://images.metmuseum.org/CRDImages/ep/original/DT833.jpg",
        9: "https://www.artic.edu/iiif/2/47149a21-a8ed-dd4c-6c93-3dbf4d53aefe/full/843,/0/default.jpg",
    },
    "Rembrandt": {
        4: "https://upload.wikimedia.org/wikipedia/commons/7/7e/Rembrandt_Harmensz._van_Rijn_-_Danae_-_Google_Art_Project.jpg",
        5: "https://upload.wikimedia.org/wikipedia/commons/4/40/Rembrandt_-_De_Joodse_bruid.jpg",
        6: "https://upload.wikimedia.org/wikipedia/commons/d/d4/Rembrandt_Harmensz._van_Rijn_-_Batseba.jpg",
        8: "https://upload.wikimedia.org/wikipedia/commons/5/5e/Rembrandt_van_Rijn_-_Self-Portrait_%281669%29.jpg",
        9: "https://upload.wikimedia.org/wikipedia/commons/8/88/Rembrandt_-_Portrait_of_Jan_Six.jpg",
    },
    "Da_Vinci": {
        4: "https://upload.wikimedia.org/wikipedia/commons/b/b5/Leonardo_da_Vinci_-_Virgin_of_the_Rocks_%28Louvre%29.jpg",
        5: "https://collectionapi.metmuseum.org/api/collection/v1/iiif/437980/1546541/main-image",
        6: "https://upload.wikimedia.org/wikipedia/commons/4/46/Annunciation_%28Leonardo%29.jpg",
        9: "https://upload.wikimedia.org/wikipedia/commons/f/f6/Leonardo_da_Vinci_-_La_belle_ferroniere.jpg",
    },
}


def download_image(url: str, save_path: Path) -> bool:
    """Download image from URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/91.0.4472.124',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        }
        response = requests.get(url, headers=headers, timeout=30, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if save_path.stat().st_size < 10000:  # At least 10KB
            save_path.unlink()
            return False
            
        print(f"✓ {save_path.parent.name}/{save_path.name} ({save_path.stat().st_size // 1024}KB)")
        return True
    except Exception as e:
        print(f"✗ {save_path.parent.name}/{save_path.name}: {str(e)[:60]}")
        return False


def main():
    print("=" * 70)
    print("Downloading missing artworks from museums and Wikimedia")
    print("=" * 70)
    
    total = 0
    success = 0
    
    for artist, artworks in SIMPLE_URLS.items():
        artist_dir = BASE_DIR / artist
        artist_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, url in artworks.items():
            save_path = artist_dir / f"artwork_{idx}.jpg"
            total += 1
            
            if download_image(url, save_path):
                success += 1
            
            time.sleep(0.5)  # Be respectful
    
    print("\n" + "=" * 70)
    print(f"✓ Downloaded: {success}/{total} artworks")
    
    # Count total real images
    import subprocess
    result = subprocess.run(
        ["find", str(BASE_DIR), "-name", "artwork_*.jpg", "-size", "+100k"],
        capture_output=True, text=True
    )
    total_real = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    print(f"📊 Total real artworks (>100KB): {total_real}/50")
    print("=" * 70)


if __name__ == "__main__":
    main()
