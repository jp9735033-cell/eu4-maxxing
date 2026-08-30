import os

loc_dir = 'localisation'
for root, dirs, files in os.walk(loc_dir):
    for f in files:
        if f.endswith('.yml'):
            p = os.path.join(root, f)
            with open(p, 'rb') as fp:
                data = fp.read()
            if not data.startswith(b'\xef\xbb\xbf'):
                print(f"Adding UTF-8 BOM to {p}")
                with open(p, 'wb') as fp:
                    fp.write(b'\xef\xbb\xbf' + data)
            else:
                print(f"OK (has BOM): {p}")
