from PIL import Image, ImageOps
import os, json

src_main = r'C:\Users\Hari Viswaa\Downloads\wetransfer_untitled-transfer_2026-02-16_1237'
dst = r'D:\nikitha-portfolio\images\projects'

# Clean old images
for f in os.listdir(dst):
    os.remove(os.path.join(dst, f))

categories = {
    # TOTES & HANDBAGS
    '1.png': ('totes', 'Patent Leather Tote', 'Glossy patent leather tote with minimalist silhouette'),
    'DSC02529.JPG': ('totes', 'Tan Leather Satchel', 'Soft distressed leather satchel with adjustable strap'),
    'DSC02632.JPG': ('totes', 'Black Leather Tote', 'Structured black leather tote with slim handles'),
    'DSC02646.JPG': ('totes', 'Tan Fold-Over Tote', 'Elegant fold-over tote in warm tan leather'),
    'DSC02770.JPG': ('totes', 'Everyday Tote', 'Spacious everyday tote with woven handle tabs'),
    'DSC02657.JPG': ('totes', 'Statement Tote', 'Bold structured tote with architectural form'),
    'DSC02657 copy.png': ('totes', 'Statement Tote Detail', 'Close-up detail of architectural tote design'),
    'DSC07929.JPG': ('totes', 'Monochrome Woven Tote', 'Black leather and woven textile tote'),
    'DSC07317.JPG': ('totes', 'Graphic Weave Tote', 'Bold graphic weave pattern tote'),
    # CROSSBODY & SHOULDER
    'DSC02541.JPG': ('crossbody', 'Leather Shoulder Bag', 'Refined leather shoulder bag with clean lines'),
    'DSC02562.JPG': ('crossbody', 'Tan Crossbody', 'Minimalist tan crossbody with metal rings'),
    'DSC02602.JPG': ('crossbody', 'Structured Crossbody', 'Structured crossbody with polished hardware'),
    'DSC03150.JPG': ('crossbody', 'Woven Crossbody', 'Dark brown intrecciato woven crossbody'),
    'DSC04853.JPG': ('crossbody', 'Bucket Shoulder Bag', 'Classic bucket silhouette in warm cognac'),
    'DSC05686.JPG': ('crossbody', 'Everyday Crossbody', 'Versatile everyday crossbody bag'),
    'DSC05754.JPG': ('crossbody', 'Leather Messenger', 'Sleek leather messenger bag'),
    'DSC05755.JPG': ('crossbody', 'Messenger Detail', 'Detailed view of messenger construction'),
    'DSC06553.JPG': ('crossbody', 'Urban Crossbody', 'Black leather urban crossbody with branded strap'),
    'DSC09630.JPG': ('crossbody', 'Mini Crossbody', 'Compact mini crossbody bag'),
    'DSC09631.JPG': ('crossbody', 'Mini Crossbody Alt', 'Mini crossbody alternate angle'),
    'DSC09632.JPG': ('crossbody', 'Mini Crossbody Detail', 'Mini crossbody hardware detail'),
    'DSC09633.JPG': ('crossbody', 'Mini Crossbody Back', 'Mini crossbody back panel'),
    'DSC09635.JPG': ('crossbody', 'Crossbody Collection', 'Crossbody collection piece'),
    # BACKPACKS
    'DSC04864.JPG': ('backpacks', 'Leather Backpack', 'Tan leather roll-top backpack with side zip'),
    'DSC06419.JPG': ('backpacks', 'Black Utility Backpack', 'Sleek black utility backpack'),
    'DSC06420.JPG': ('backpacks', 'Utility Backpack Detail', 'Side detail of utility backpack'),
    'DSC06422.JPG': ('backpacks', 'Utility Backpack Interior', 'Interior organization of backpack'),
    'DSC06423.JPG': ('backpacks', 'Utility Backpack Back', 'Ergonomic back panel design'),
    'DSC06430.JPG': ('backpacks', 'Backpack Hardware', 'Premium hardware and closure detail'),
    'DSC06641.JPG': ('backpacks', 'Explorer Backpack', 'Full leather explorer backpack with buckle closures'),
    'DSC06643.JPG': ('backpacks', 'Explorer Top View', 'Top view of explorer backpack'),
    'DSC06644.JPG': ('backpacks', 'Explorer Side', 'Side profile of explorer backpack'),
    # POUCHES & CLUTCHES
    'DSC02551.JPG': ('pouches', 'Woven Panel Pouch', 'Dark leather pouch with woven panel detail'),
    'DSC02583.JPG': ('pouches', 'Envelope Clutch', 'Tan leather envelope clutch with curved flap'),
    'DSC02693.JPG': ('pouches', 'Leather Wristlet', 'Tan leather wristlet with embossed logo'),
    'DSC02785.JPG': ('pouches', 'Document Sleeve', 'Premium leather document sleeve'),
    'DSC08083.JPG': ('pouches', 'Striped Canvas Pouch', 'Navy and white striped canvas zip pouch'),
    'DSC08089.JPG': ('pouches', 'Canvas Pouch Detail', 'Canvas pouch leather zipper pull'),
    'DSC09391.JPG': ('pouches', 'Travel Pouch', 'Compact travel pouch'),
    'DSC09393.JPG': ('pouches', 'Travel Pouch Alt', 'Travel pouch alternate view'),
    'DSC09395.JPG': ('pouches', 'Zip Pouch', 'Slim zip pouch'),
    'DSC09397.JPG': ('pouches', 'Zip Pouch Detail', 'Zip pouch interior detail'),
    # SMALL LEATHER GOODS
    'DSC01663.JPG': ('slg', 'Classic Belt', 'Black leather belt with brushed silver buckle'),
    'DSC02627.JPG': ('slg', 'Leather Keychain', 'Hand-stitched leather keychain with brass clip'),
    'DSC03007.JPG': ('slg', 'Card Holder', 'Compact card holder with diagonal pocket design'),
    'DSC04356.JPG': ('slg', 'Leather Organizer', 'Multi-compartment leather travel organizer'),
    'DSC04361.JPG': ('slg', 'Organizer Interior', 'Interior view of travel organizer'),
    'DSC04373.JPG': ('slg', 'Compact Wallet', 'Minimalist compact leather wallet'),
    'DSC09459.JPG': ('slg', 'Leather Accessory', 'Artisan leather accessory'),
    'DSC09669.JPG': ('slg', 'Leather Goods Set', 'Coordinated leather goods collection'),
    # WOVEN & TEXTILE
    'DSC05071.JPG': ('woven', 'Woven Cosmetic Case', 'White woven leather cosmetic case with ABLE tag'),
    'DSC07480.JPG': ('woven', 'Textile Craft Bag', 'Handcrafted textile bag'),
    'DSC07496.JPG': ('woven', 'Crochet Bag', 'Artisan crochet bag'),
    'DSC07513.JPG': ('woven', 'Woven Tote', 'Natural fiber woven tote'),
    'DSC07526.JPG': ('woven', 'Raffia Grid Tote', 'Raffia tote with grid pattern and leather handles'),
    'DSC07557.JPG': ('woven', 'Raffia Shoulder Bag', 'Natural raffia shoulder bag'),
    'DSC07631.JPG': ('woven', 'Handwoven Piece', 'Artisan handwoven bag'),
    'DSC07891.JPG': ('woven', 'Woven Collection', 'Woven collection highlight'),
    'DSC08167.JPG': ('woven', 'Textile Tote', 'Textile combination tote'),
    'DSC08194.JPG': ('woven', 'Craft Bag Detail', 'Detail of artisan craft bag'),
    'DSC08346.JPG': ('woven', 'Mixed Media Bag', 'Leather and textile mixed media bag'),
    'DSC08354.JPG': ('woven', 'Mixed Media Detail', 'Detail view of mixed media construction'),
    'DSC08514.JPG': ('woven', 'Embroidered Art Tote', 'Leather tote with hand-embroidered art panel'),
    'DSC08611.JPG': ('woven', 'Artisan Textile', 'Artisan textile bag'),
    'DSC08723.JPG': ('woven', 'Woven Accessory', 'Woven textile accessory'),
    # UTILITY & TRAVEL
    'DSC05797.JPG': ('utility', 'Military Utility Bag', 'Olive nylon utility bag with snap pockets'),
    'DSC06126.JPG': ('utility', 'Tactical Belt Bag', 'Olive tactical belt bag with buckle closure'),
    'DSC06128.JPG': ('utility', 'Belt Bag Detail', 'Detail of tactical belt bag hardware'),
    'DSC06585.JPG': ('utility', 'Utility Crossbody', 'Functional utility crossbody'),
    'DSC06862.JPG': ('utility', 'Nylon Duffle', 'Utility nylon duffle bag'),
    'DSC09304.JPG': ('utility', 'Sling Pack', 'Compact sling pack for urban commute'),
    'DSC09306.JPG': ('utility', 'Sling Pack Detail', 'Sling pack strap detail'),
    'DSC09307.JPG': ('utility', 'Sling Pack Alt', 'Sling pack alternate view'),
    'DSC09843.JPG': ('utility', 'Travel Bag', 'Versatile travel bag'),
    'DSC07946.JPG': ('utility', 'Utility Piece', 'Utility collection piece'),
    'DSC07959.JPG': ('utility', 'Utility Detail', 'Utility bag detail'),
    'DSC07978.JPG': ('utility', 'Travel Accessory', 'Travel accessory design'),
}

# Add New folder images
new_folder_imgs = [
    'DSC05667.jpg', 'DSC05670.jpg', 'DSC05682.jpg', 'DSC05684.jpg',
    'DSC05746.JPG', 'DSC05747.JPG', 'DSC05756.JPG', 'DSC05799.JPG',
    'DSC05800.JPG', 'DSC06040.JPG', 'DSC06042.JPG', 'DSC06046.JPG',
    'DSC06123.JPG', 'DSC06127.JPG', 'DSC06131.JPG', 'DSC06555.JPG',
    'DSC06556.JPG', 'DSC06876.JPG', 'DSC08074.JPG', 'DSC09302.JPG',
    'DSC09303.JPG', 'DSC09309.JPG', 'DSC09392.JPG', 'DSC09670.JPG',
    'DSC09672.JPG', 'DSC09673.JPG'
]

for i, img in enumerate(new_folder_imgs):
    num = int(img.split('.')[0].replace('DSC', ''))
    if num < 6000:
        cat, name, desc = 'crossbody', f'Shoulder Bag {i+1}', 'Leather shoulder bag from collection'
    elif num < 7000:
        cat, name, desc = 'utility', f'Utility Design {i+1}', 'Utility collection piece'
    elif num < 9000:
        cat, name, desc = 'woven', f'Textile Piece {i+1}', 'Textile and craft collection piece'
    else:
        cat, name, desc = 'pouches', f'Accessory {i+1}', 'Small accessory from collection'
    categories[f'New folder/{img}'] = (cat, name, desc)

results = []
count = 0
errors = 0

for filename, (cat, name, desc) in categories.items():
    src_path = os.path.join(src_main, filename)
    if not os.path.exists(src_path):
        print(f'MISS: {filename}')
        errors += 1
        continue
    try:
        img = Image.open(src_path)
        img = ImageOps.exif_transpose(img)
        img.thumbnail((1000, 1000), Image.LANCZOS)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        safe = filename.replace('/', '_').replace('\\', '_').replace(' ', '-')
        safe = safe.lower()
        if safe.endswith('.png'):
            safe = safe[:-4] + '.jpg'
        if not safe.endswith('.jpg'):
            safe = safe + '.jpg'
        out_path = os.path.join(dst, safe)
        img.save(out_path, 'JPEG', quality=82, optimize=True)
        results.append({
            'file': safe,
            'cat': cat,
            'name': name,
            'desc': desc,
            'w': img.width,
            'h': img.height
        })
        count += 1
    except Exception as e:
        print(f'ERR: {filename}: {e}')
        errors += 1

with open(r'D:\nikitha-portfolio\image_manifest.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f'\nProcessed: {count} | Errors: {errors}')
for cat in sorted(set(r['cat'] for r in results)):
    cc = len([r for r in results if r['cat'] == cat])
    print(f'  {cat}: {cc}')
