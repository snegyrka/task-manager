import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.py') and not f.startswith('fix'):
            path = os.path.join(root, f)
            try:
                with open(path, 'rb') as file:
                    data = file.read()
                text = data.decode('cp1251')
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(text)
                print(f'Fixed: {path}')
            except Exception as e:
                print(f'Skip: {path} ({e})')

print('Done!')