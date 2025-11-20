"""
Download Additional Artworks to fill gaps
"""

import requests
from pathlib import Path
import time

BASE_DIR = Path(__file__).parent.parent / "data" / "artworks"

# Additional URLs for missing artworks
ADDITIONAL_ARTWORKS = {
    "Picasso": {
        3: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Pablo_Picasso_-_Girl_before_a_Mirror.jpg/800px-Pablo_Picasso_-_Girl_before_a_Mirror.jpg",
        4: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Old_guitarist_chicago.jpg/600px-Old_guitarist_chicago.jpg",
        5: "https://upload.wikimedia.org/wikipedia/en/0/0e/Picasso_three_musicians_moma_2006.jpg",
        6: "https://upload.wikimedia.org/wikipedia/en/6/6c/La_Vie_by_Pablo_Picasso.jpg",
        7: "https://upload.wikimedia.org/wikipedia/en/a/a6/Pablo_Picasso%2C_1905%2C_Woman_with_a_Fan%2C_oil_on_canvas%2C_100.3_x_81.3_cm%2C_National_Gallery_of_Art%2C_Washington%2C_DC.jpg",
        8: "https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/Pablo_Picasso%2C_1932%2C_Le_R%C3%AAve_%28The_Dream%29%2C_oil_on_canvas%2C_130_x_97_cm%2C_private_collection.jpg/600px-thumbnail.jpg",
        9: "https://upload.wikimedia.org/wikipedia/en/thumb/8/8a/Pablo_Picasso_1927_Seated_Woman.jpg/600px-Pablo_Picasso_1927_Seated_Woman.jpg",
    },
    "Monet": {
        0: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Claude_Monet%2C_French_-_Water_Lilies_-_Google_Art_Project.jpg/1280px-Claude_Monet%2C_French_-_Water_Lilies_-_Google_Art_Project.jpg",
        3: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Monet_poppies.JPG/1280px-Monet_poppies.JPG",
        4: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Claude_Monet_-_Le_Bassin_Aux_Nymph%C3%A9as%2C_Harmonie_Rose.jpg/1280px-Claude_Monet_-_Le_Bassin_Aux_Nymph%C3%A9as%2C_Harmonie_Rose.jpg",
        5: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Claude_Monet_-_Rouen_Cathedral%2C_Facade_%28Sunset%29.jpg/800px-Claude_Monet_-_Rouen_Cathedral%2C_Facade_%28Sunset%29.jpg",
        6: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Claude_Monet_-_Meules%2C_milieu_du_jour.jpg/1280px-Claude_Monet_-_Meules%2C_milieu_du_jour.jpg",
        7: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Claude_Monet_-_The_Houses_of_Parliament%2C_Sunset.jpg/1280px-Claude_Monet_-_The_Houses_of_Parliament%2C_Sunset.jpg",
        8: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Monet_-_jardin-a-sainte-adresse.jpg/1280px-Monet_-_jardin-a-sainte-adresse.jpg",
        9: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29.jpg/1280px-Claude_Monet_-_Stacks_of_Wheat_%28End_of_Summer%29.jpg",
    },
    "Rembrandt": {
        4: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Rembrandt_Harmensz._van_Rijn_-_Danae_-_Google_Art_Project.jpg/1280px-Rembrandt_Harmensz._van_Rijn_-_Danae_-_Google_Art_Project.jpg",
        5: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Rembrandt_-_De_Joodse_bruid.jpg/1280px-Rembrandt_-_De_Joodse_bruid.jpg",
        6: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Rembrandt_Harmensz._van_Rijn_-_Bathsheba_at_Her_Bath_-_WGA19090.jpg/800px-Rembrandt_Harmensz._van_Rijn_-_Bathsheba_at_Her_Bath_-_WGA19090.jpg",
        8: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Rembrandt_van_Rijn_-_Self-Portrait_%281669%29.jpg/800px-Rembrandt_van_Rijn_-_Self-Portrait_%281669%29.jpg",
        9: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Rembrandt_-_Portrait_of_Jan_Six.jpg/800px-Rembrandt_-_Portrait_of_Jan_Six.jpg",
    },
    "Da_Vinci": {
        4: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Leonardo_da_Vinci_-_Virgin_of_the_Rocks_%28Louvre%29.jpg/800px-Leonardo_da_Vinci_-_Virgin_of_the_Rocks_%28Louvre%29.jpg",
        5: "https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/Leonardo_da_Vinci%2C_Salvator_Mundi%2C_c.1500%2C_oil_on_walnut%2C_45.4_%C3%97_65.6_cm.jpg/600px-thumbnail.jpg",
        6: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Annunciation_%28Leonardo%29.jpg/1280px-Annunciation_%28Leonardo%29.jpg",
        9: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Leonardo_da_Vinci_-_La_belle_ferroniere.jpg/800px-Leonardo_da_Vinci_-_La_belle_ferroniere.jpg",
    },
}


def download_image(url: str, save_path: Path) -> bool:
    """Download image from URL."""
    try:
        headers = {'User-Agent': 'ArtGuideBot/1.0'}
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        if save_path.stat().st_size < 5000:
            save_path.unlink()
            return False
            
        print(f"✓ {save_path.parent.name}/{save_path.name} ({save_path.stat().st_size // 1024}KB)")
        return True
    except Exception as e:
        print(f"✗ {save_path.parent.name}/{save_path.name}: {str(e)[:40]}")
        return False


def main():
    print("=" * 70)
    print("Filling gaps in artwork collection")
    print("=" * 70)
    
    total = 0
    success = 0
    
    for artist, artworks in ADDITIONAL_ARTWORKS.items():
        artist_dir = BASE_DIR / artist
        artist_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, url in artworks.items():
            save_path = artist_dir / f"artwork_{idx}.jpg"
            total += 1
            
            if download_image(url, save_path):
                success += 1
            
            time.sleep(0.3)
    
    print("\n" + "=" * 70)
    print(f"✓ Downloaded: {success}/{total} missing artworks")
    print("=" * 70)


if __name__ == "__main__":
    main()
