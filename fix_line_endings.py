import os

for root, dirs, files in os.walk('app'):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'rb') as file:
                data = file.read()
            # Убираем \r, оставляем только \n
            data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
            with open(path, 'wb') as file:
                file.write(data)
            print(f'Fixed: {path}')

print('Done!')