"""
Download Real Artwork Images - Version 2
Uses alternative public domain sources including Wikimedia Commons, Google Arts & Culture, etc.
"""

import os
import requests
from pathlib import Path
import time
from urllib.parse import quote

BASE_DIR = Path(__file__).parent.parent / "data" / "artworks"

# Famous artworks with direct Wikimedia Commons links (public domain)
ARTWORKS = {
    "Van_Gogh": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Vincent_Willem_van_Gogh_127.jpg/800px-Vincent_Willem_van_Gogh_127.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Irises-Vincent_van_Gogh.jpg/1024px-Irises-Vincent_van_Gogh.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Vincent_van_Gogh_-_De_slaapkamer_-_Google_Art_Project.jpg/1280px-Vincent_van_Gogh_-_De_slaapkamer_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Vincent_Willem_van_Gogh_-_Cafe_Terrace_at_Night_%28Yorck%29.jpg/800px-Vincent_Willem_van_Gogh_-_Cafe_Terrace_at_Night_%28Yorck%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Vincent_van_Gogh_-_Almond_blossom_-_Google_Art_Project.jpg/1280px-Vincent_van_Gogh_-_Almond_blossom_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Wheat-Field-with-Cypresses-%281889%29-Vincent-van-Gogh-Met.jpg/1280px-Wheat-Field-with-Cypresses-%281889%29-Vincent-van-Gogh-Met.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Van_Gogh_-_Terrasse_des_Caf%C3%A9s_an_der_Place_du_Forum_in_Arles_am_Abend1.jpeg/800px-Van_Gogh_-_Terrasse_des_Caf%C3%A9s_an_der_Place_du_Forum_in_Arles_am_Abend1.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg/800px-Vincent_van_Gogh_-_Self-Portrait_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Van-willem-vincent-gogh-die-kartoffelesser-03850.jpg/1280px-Van-willem-vincent-gogh-die-kartoffelesser-03850.jpg",
    ],
    "Picasso": [
        "https://upload.wikimedia.org/wikipedia/en/7/74/PicassoGuernica.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/1/14/Picasso_The_Weeping_Woman_Tate_identifier_T05010_10.jpg/800px-Picasso_The_Weeping_Woman_Tate_identifier_T05010_10.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Les_Demoiselles_d%27Avignon.jpg/800px-Les_Demoiselles_d%27Avignon.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/Pablo_Picasso%2C_1910%2C_Girl_with_a_Mandolin_%28Fanny_Tellier%29%2C_oil_on_canvas%2C_100.3_x_73.6_cm%2C_Museum_of_Modern_Art_New_York..jpg/600px-thumbnail.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/2/28/Pablo_Picasso%2C_1903-04%2C_The_Old_Guitarist%2C_oil_on_panel%2C_122.9_x_82.6_cm%2C_Art_Institute_of_Chicago.jpg/600px-thumbnail.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/3/3c/Pablo_Picasso%2C_1921%2C_Nous_autres_musiciens_%28Three_Musicians%29%2C_oil_on_canvas%2C_200.7_x_222.9_cm%2C_Philadelphia_Museum_of_Art.jpg/800px-thumbnail.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Pablo_Picasso%2C_1903%2C_La_Vie_%28Life%29%2C_oil_on_canvas%2C_196.5_x_129.2_cm%2C_Cleveland_Museum_of_Art.jpg/600px-thumbnail.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/dd/Pablo_Picasso%2C_1932%2C_Girl_before_a_Mirror%2C_oil_on_canvas%2C_162.3_x_130.2_cm%2C_Museum_of_Modern_Art%2C_New_York.jpg/600px-thumbnail.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Le_R%C3%AAve.jpg/600px-Le_R%C3%AAve.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/9/9c/Pablo_Picasso%2C_1909-10%2C_Figure_dans_un_Fauteuil_%28Seated_Nude%2C_Femme_nue_assise%29%2C_oil_on_canvas%2C_92.1_x_73_cm%2C_Tate_Modern%2C_London.jpg/600px-thumbnail.jpg",
    ],
    "Monet": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Claude_Monet_-_Water_Lilies_-_1906%2C_Ryerson.jpg/1280px-Claude_Monet_-_Water_Lilies_-_1906%2C_Ryerson.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Monet_-_Impression%2C_Sunrise.jpg/1280px-Monet_-_Impression%2C_Sunrise.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Claude_Monet_-_Woman_with_a_Parasol_-_Madame_Monet_and_Her_Son_-_Google_Art_Project.jpg/800px-Claude_Monet_-_Woman_with_a_Parasol_-_Madame_Monet_and_Her_Son_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Claude_Monet_-_Coquelicots%2C_La_promenade_%28Argenteuil%29.jpg/1280px-Claude_Monet_-_Coquelicots%2C_La_promenade_%28Argenteuil%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Monet_-_Seerosen5.jpg/1280px-Monet_-_Seerosen5.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Claude_Monet_-_Rouen_Cathedral%2C_Portal_and_Tower_of_Saint-Romain%2C_Full_Sunlight.jpg/800px-Claude_Monet_-_Rouen_Cathedral%2C_Portal_and_Tower_of_Saint-Romain%2C_Full_Sunlight.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Claude_Monet_-_Haystacks%2C_end_of_Summer_-_Google_Art_Project.jpg/1280px-Claude_Monet_-_Haystacks%2C_end_of_Summer_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Claude_Monet%2C_Saint-Georges_majeur_au_cr%C3%A9puscule.jpg/1280px-Claude_Monet%2C_Saint-Georges_majeur_au_cr%C3%A9puscule.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Claude_Monet_-_Garden_at_Sainte-Adresse_-_Google_Art_Project.jpg/1280px-Claude_Monet_-_Garden_at_Sainte-Adresse_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Claude_Monet_-_Graystaks_I.JPG/1280px-Claude_Monet_-_Graystaks_I.JPG",
    ],
    "Rembrandt": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/The_Night_Watch_-_HD.jpg/1280px-The_Night_Watch_-_HD.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg/800px-Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Rembrandt_Christ_in_the_Storm_on_the_Lake_of_Galilee.jpg/1280px-Rembrandt_Christ_in_the_Storm_on_the_Lake_of_Galilee.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg/1280px-Rembrandt_-_The_Anatomy_Lesson_of_Dr_Nicolaes_Tulp.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Rembrandt_Harmensz._van_Rijn_026.jpg/800px-Rembrandt_Harmensz._van_Rijn_026.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Rembrandt_Harmensz._van_Rijn_019.jpg/1280px-Rembrandt_Harmensz._van_Rijn_019.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Rembrandt_Harmensz._van_Rijn_-_Batseba.jpg/800px-Rembrandt_Harmensz._van_Rijn_-_Batseba.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Rembrandt_Harmensz_van_Rijn_-_Return_of_the_Prodigal_Son_-_Google_Art_Project.jpg/1280px-Rembrandt_Harmensz_van_Rijn_-_Return_of_the_Prodigal_Son_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Rembrandt_-_Self-Portrait_-_WGA19206.jpg/800px-Rembrandt_-_Self-Portrait_-_WGA19206.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Rembrandt_Harmensz._van_Rijn_018.jpg/800px-Rembrandt_Harmensz._van_Rijn_018.jpg",
    ],
    "Da_Vinci": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/800px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/%C3%9Altima_Cena_-_Da_Vinci_5.jpg/1280px-%C3%9Altima_Cena_-_Da_Vinci_5.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Da_Vinci_Vitruve_Luc_Viatour.jpg/800px-Da_Vinci_Vitruve_Luc_Viatour.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/Lady_with_an_Ermine_-_Leonardo_da_Vinci_-_Google_Art_Project.jpg/800px-Lady_with_an_Ermine_-_Leonardo_da_Vinci_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Leonardo_da_Vinci_-_Virgin_of_the_Rocks_%28National_Gallery_London%29.jpg/800px-Leonardo_da_Vinci_-_Virgin_of_the_Rocks_%28National_Gallery_London%29.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Leonardo_da_Vinci_-_Salvator_Mundi_-_Google_Art_Project.jpg/800px-Leonardo_da_Vinci_-_Salvator_Mundi_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Leonardo_da_Vinci_-_Annunciazione_-_Google_Art_Project.jpg/1280px-Leonardo_da_Vinci_-_Annunciazione_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Leonardo_da_Vinci_-_Saint_John_the_Baptist_C2RMF_retouched.jpg/800px-Leonardo_da_Vinci_-_Saint_John_the_Baptist_C2RMF_retouched.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Leonardo_da_Vinci_-_Ginevra_de%27_Benci_-_Google_Art_Project.jpg/800px-Leonardo_da_Vinci_-_Ginevra_de%27_Benci_-_Google_Art_Project.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Leonardo_da_Vinci_-_La_belle_ferronni%C3%A8re.jpg/800px-Leonardo_da_Vinci_-_La_belle_ferronni%C3%A8re.jpg",
    ],
}


def download_image(url: str, save_path: Path) -> bool:
    """Download image from URL."""
    try:
        headers = {
            'User-Agent': 'ArtGuideBot/1.0 (Educational Project; TU/e)'
        }
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify it's an actual image (> 5KB)
        if save_path.stat().st_size < 5000:
            save_path.unlink()
            return False
            
        print(f"✓ {save_path.name} ({save_path.stat().st_size // 1024}KB)")
        return True
    except Exception as e:
        print(f"✗ {save_path.name}: {str(e)[:50]}")
        return False


def main():
    """Download all artworks."""
    print("=" * 70)
    print("Downloading Real Artworks from Wikimedia Commons")
    print("=" * 70)
    
    total_downloaded = 0
    total_failed = 0
    
    for artist, urls in ARTWORKS.items():
        print(f"\n📁 {artist.replace('_', ' ')} ({len(urls)} artworks)")
        print("-" * 70)
        
        artist_dir = BASE_DIR / artist
        artist_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, url in enumerate(urls):
            save_path = artist_dir / f"artwork_{idx}.jpg"
            
            if download_image(url, save_path):
                total_downloaded += 1
            else:
                total_failed += 1
            
            time.sleep(0.3)  # Be nice to Wikimedia
    
    print("\n" + "=" * 70)
    print(f"✓ Downloaded: {total_downloaded} images")
    print(f"✗ Failed: {total_failed} images")
    print(f"Success rate: {100 * total_downloaded / (total_downloaded + total_failed):.1f}%")
    print("=" * 70)
    
    if total_downloaded >= 40:
        print("\n✅ SUCCESS! Enough artworks downloaded.")
        print("Next: Run 'python scripts/prepare_dataset.py' to rebuild FAISS index")
    else:
        print(f"\n⚠️  WARNING: Only {total_downloaded}/50 images downloaded.")


if __name__ == "__main__":
    main()
