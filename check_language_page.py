print('🔍 CONTENIDO DE pages/language_page.py:')
print('=' * 50)

with open('pages/language_page.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Verificar elementos clave
checks = [
    ('class LanguagePage', 'Clase LanguagePage'),
    ('BasePage', 'Hereda de BasePage'),
    ('LANGUAGE_MAP', 'Mapeo de idiomas'),
    ('select_language', 'Método select_language'),
    ('get_current_language', 'Método get_current_language'),
    ('open_language_menu', 'Método open_language_menu'),
    ('take_screenshot_with_url', 'Screenshots completos'),
    ('get_page_info', 'Información de página')
]

print('✅ ELEMENTOS ENCONTRADOS:')
for check, description in checks:
    if check in content:
        print(f'   ✅ {description}')
    else:
        print(f'   ❌ {description}')

# Verificar mapeo de idiomas
if 'LANGUAGE_MAP' in content:
    print('\n🗺️  MAPEO DE IDIOMAS:')
    # Extraer el mapeo
    import re
    map_match = re.search(r'LANGUAGE_MAP\s*=\s*{([^}]+)}', content)
    if map_match:
        map_content = map_match.group(1)
        idiomas = ['español', 'english', 'francais', 'portugues']
        for idioma in idiomas:
            if f"'{idioma}'" in map_content or f'"{idioma}"' in map_content:
                print(f'   ✅ {idioma}')
            else:
                print(f'   ❌ {idioma}')
else:
    print('\n❌ No se encontró LANGUAGE_MAP')