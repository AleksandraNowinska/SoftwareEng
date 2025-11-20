"""
Download Real Artwork Images
This script downloads actual artwork images from WikiArt for 5 famous artists.
Each artist will have 10 representative paintings downloaded.

Artists: Van Gogh, Picasso, Monet, Rembrandt, Da Vinci
"""

import os
import requests
from pathlib import Path
import time

# Target directory
BASE_DIR = Path(__file__).parent.parent / "data" / "artworks"

# Artwork URLs from WikiArt and public domain sources
ARTWORKS = {
    "Van_Gogh": [
        ("The Starry Night", "https://uploads0.wikiart.org/images/vincent-van-gogh/the-starry-night-1889.jpg"),
        ("Sunflowers", "https://uploads1.wikiart.org/images/vincent-van-gogh/sunflowers-1889.jpg"),
        ("Irises", "https://uploads2.wikiart.org/images/vincent-van-gogh/irises-1889.jpg"),
        ("The Bedroom", "https://uploads3.wikiart.org/images/vincent-van-gogh/bedroom-in-arles-1888.jpg"),
        ("Café Terrace at Night", "https://uploads4.wikiart.org/images/vincent-van-gogh/cafe-terrace-place-du-forum-arles-1888.jpg"),
        ("Almond Blossoms", "https://uploads5.wikiart.org/images/vincent-van-gogh/almond-blossom-1890.jpg"),
        ("Wheat Field with Cypresses", "https://uploads6.wikiart.org/images/vincent-van-gogh/wheat-field-with-cypresses-1889.jpg"),
        ("The Night Café", "https://uploads7.wikiart.org/images/vincent-van-gogh/the-night-cafe-1888.jpg"),
        ("Self-Portrait", "https://uploads8.wikiart.org/images/vincent-van-gogh/self-portrait-1889.jpg"),
        ("The Potato Eaters", "https://uploads0.wikiart.org/images/vincent-van-gogh/the-potato-eaters-1885.jpg"),
    ],
    "Picasso": [
        ("Guernica", "https://uploads1.wikiart.org/images/pablo-picasso/guernica-1937.jpg"),
        ("The Weeping Woman", "https://uploads2.wikiart.org/images/pablo-picasso/the-weeping-woman-1937.jpg"),
        ("Les Demoiselles d'Avignon", "https://uploads3.wikiart.org/images/pablo-picasso/les-demoiselles-d-avignon-1907.jpg"),
        ("Girl before a Mirror", "https://uploads4.wikiart.org/images/pablo-picasso/girl-before-a-mirror-1932.jpg"),
        ("The Old Guitarist", "https://uploads5.wikiart.org/images/pablo-picasso/the-old-guitarist-1903.jpg"),
        ("Three Musicians", "https://uploads6.wikiart.org/images/pablo-picasso/three-musicians-1921.jpg"),
        ("La Vie", "https://uploads7.wikiart.org/images/pablo-picasso/la-vie-the-life-1903.jpg"),
        ("Woman with a Flower", "https://uploads8.wikiart.org/images/pablo-picasso/woman-with-a-flower-1930.jpg"),
        ("The Dream", "https://uploads0.wikiart.org/images/pablo-picasso/the-dream-1932.jpg"),
        ("Seated Woman", "https://uploads1.wikiart.org/images/pablo-picasso/seated-woman-1927.jpg"),
    ],
    "Monet": [
        ("Water Lilies", "https://uploads2.wikiart.org/images/claude-monet/water-lilies-1916.jpg"),
        ("Impression Sunrise", "https://uploads3.wikiart.org/images/claude-monet/impression-sunrise.jpg"),
        ("Woman with a Parasol", "https://uploads4.wikiart.org/images/claude-monet/woman-with-a-parasol-1875.jpg"),
        ("Poppies", "https://uploads5.wikiart.org/images/claude-monet/poppy-field-1873.jpg"),
        ("The Japanese Bridge", "https://uploads6.wikiart.org/images/claude-monet/the-water-lily-pond-1899.jpg"),
        ("Rouen Cathedral", "https://uploads7.wikiart.org/images/claude-monet/rouen-cathedral-facade-and-tour-d-albane-morning-effect-1894.jpg"),
        ("Haystacks", "https://uploads8.wikiart.org/images/claude-monet/haystacks-end-of-summer-1891.jpg"),
        ("Houses of Parliament", "https://uploads0.wikiart.org/images/claude-monet/houses-of-parliament-london-1904.jpg"),
        ("The Garden at Sainte-Adresse", "https://uploads1.wikiart.org/images/claude-monet/garden-at-sainte-adresse-1867.jpg"),
        ("Wheatstacks", "https://uploads2.wikiart.org/images/claude-monet/wheatstacks-snow-effect-morning-1891.jpg"),
    ],
    "Rembrandt": [
        ("The Night Watch", "https://uploads3.wikiart.org/images/rembrandt/the-night-watch-1642.jpg"),
        ("Self-Portrait", "https://uploads4.wikiart.org/images/rembrandt/self-portrait-1659.jpg"),
        ("The Storm on the Sea of Galilee", "https://uploads5.wikiart.org/images/rembrandt/the-storm-on-the-sea-of-galilee-1633.jpg"),
        ("Anatomy Lesson", "https://uploads6.wikiart.org/images/rembrandt/the-anatomy-lesson-of-dr-nicolaes-tulp-1632.jpg"),
        ("Danae", "https://uploads7.wikiart.org/images/rembrandt/danae-1636.jpg"),
        ("The Jewish Bride", "https://uploads8.wikiart.org/images/rembrandt/the-jewish-bride-1667.jpg"),
        ("Bathsheba at Her Bath", "https://uploads0.wikiart.org/images/rembrandt/bathsheba-at-her-bath-1654.jpg"),
        ("The Return of the Prodigal Son", "https://uploads1.wikiart.org/images/rembrandt/return-of-the-prodigal-son-1669.jpg"),
        ("Self-Portrait with Two Circles", "https://uploads2.wikiart.org/images/rembrandt/self-portrait-with-two-circles-1660.jpg"),
        ("Portrait of Jan Six", "https://uploads3.wikiart.org/images/rembrandt/portrait-of-jan-six-1654.jpg"),
    ],
    "Da_Vinci": [
        ("Mona Lisa", "https://uploads4.wikiart.org/images/leonardo-da-vinci/mona-lisa.jpg"),
        ("The Last Supper", "https://uploads5.wikiart.org/images/leonardo-da-vinci/the-last-supper.jpg"),
        ("Vitruvian Man", "https://uploads6.wikiart.org/images/leonardo-da-vinci/the-vitruvian-man.jpg"),
        ("Lady with an Ermine", "https://uploads7.wikiart.org/images/leonardo-da-vinci/lady-with-an-ermine-1490.jpg"),
        ("The Virgin of the Rocks", "https://uploads8.wikiart.org/images/leonardo-da-vinci/the-virgin-of-the-rocks-1485.jpg"),
        ("Salvator Mundi", "https://uploads0.wikiart.org/images/leonardo-da-vinci/salvator-mundi.jpg"),
        ("Annunciation", "https://uploads1.wikiart.org/images/leonardo-da-vinci/annunciation-1475.jpg"),
        ("St. John the Baptist", "https://uploads2.wikiart.org/images/leonardo-da-vinci/st-john-the-baptist.jpg"),
        ("Portrait of Ginevra de' Benci", "https://uploads3.wikiart.org/images/leonardo-da-vinci/ginevra-de-benci.jpg"),
        ("La belle ferronnière", "https://uploads4.wikiart.org/images/leonardo-da-vinci/la-belle-ferronni-re.jpg"),
    ],
}


def download_image(url: str, save_path: Path) -> bool:
    """Download image from URL to local path."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {save_path.name}")
        return True
    except Exception as e:
        print(f"✗ Failed {save_path.name}: {str(e)}")
        return False


def main():
    """Download all artworks."""
    print("=" * 70)
    print("Downloading Real Artwork Images from WikiArt")
    print("=" * 70)
    
    total_downloaded = 0
    total_failed = 0
    
    for artist, artworks in ARTWORKS.items():
        print(f"\n📁 {artist.replace('_', ' ')} ({len(artworks)} artworks)")
        print("-" * 70)
        
        artist_dir = BASE_DIR / artist
        artist_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, (title, url) in enumerate(artworks):
            save_path = artist_dir / f"artwork_{idx}.jpg"
            
            if download_image(url, save_path):
                total_downloaded += 1
            else:
                total_failed += 1
            
            # Be nice to the server
            time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print(f"✓ Downloaded: {total_downloaded} images")
    print(f"✗ Failed: {total_failed} images")
    print("=" * 70)
    
    if total_downloaded >= 45:  # At least 90% success
        print("\n✅ SUCCESS: Enough artworks downloaded to rebuild the dataset!")
        print("Next step: Run 'python scripts/prepare_dataset.py' to rebuild FAISS index")
    else:
        print("\n⚠️  WARNING: Some downloads failed. Check network connection.")


if __name__ == "__main__":
    main()
