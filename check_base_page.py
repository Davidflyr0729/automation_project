print('🔍 CONTENIDO DE pages/base_page.py:')
print('=' * 50)

with open('pages/base_page.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Verificar elementos clave
checks = [
    ('class BasePage', 'Clase BasePage'),
    ('take_full_page_screenshot', 'Screenshot página completa'),
    ('take_screenshot_with_url', 'Screenshot con URL'),
    ('get_page_info', 'Información de página'),
    ('find_element', 'Método find_element'),
    ('click_element', 'Método click_element'),
    ('wait_for_url', 'Método wait_for_url')
]

print('✅ ELEMENTOS ENCONTRADOS:')
for check, description in checks:
    if check in content:
        print(f'   ✅ {description}')
    else:
        print(f'   ❌ {description}')

# Verificar imports necesarios
print('\n📦 IMPORTS:')
imports = [
    'WebDriverWait',
    'expected_conditions',
    'TimeoutException', 
    'os',
    'datetime'
]
for imp in imports:
    if imp in content:
        print(f'   ✅ {imp}')
    else:
        print(f'   ❌ {imp}')