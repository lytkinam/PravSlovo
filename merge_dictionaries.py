#!/usr/bin/env python3
"""
Скрипт для объединения всех полных словарей в один файл
Объединяет part_1_full - part_7_full в dict_full/dictionary.txt

Использование:
python merge_dictionaries.py
"""

from pathlib import Path
from typing import Set

def parse_dictionary_file(filepath: str) -> Set[str]:
    """Извлекает термины из файла словаря Gboard"""
    terms = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # ИСПРАВЛЕНИЕ: Удаляем только переносы строк, сохраняя \t
                line = line.rstrip('\r\n')
                
                # Пропускаем комментарии и пустые строки
                if line.startswith('#') or not line.strip():
                    continue
                    
                # Извлекаем термин (второе поле после TAB)
                parts = line.split('\t')
                
                # Формат Gboard: shortcut \t word \t language \t pos
                if len(parts) >= 2 and parts[1].strip():
                    terms.add(parts[1].strip())
                    
    except FileNotFoundError:
        print(f"   ⚠️ Файл не найден: {filepath}")
    
    return terms

def merge_all_dictionaries():
    """Объединяет все словари в один"""
    print("="*80)
    print("ОБЪЕДИНЕНИЕ ВСЕХ СЛОВАРЕЙ В ОДИН ФАЙЛ")
    print("="*80)
    
    partitions = [
        'part_1_full',
        'part_2_full',
        'part_3_full',
        'part_4_full',
        'part_5_full',
        'part_6_full',
        'part_7_full',
    ]
    
    all_terms = set()
    stats_counts = {}  # ИСПРАВЛЕНИЕ: Кэшируем статистику для избежания повторного чтения
    
    for part_name in partitions:
        dict_path = f"{part_name}/dictionary.txt"
        print(f"\n📖 Чтение: {dict_path}")
        
        terms = parse_dictionary_file(dict_path)
        stats_counts[part_name] = len(terms)
        
        if terms:
            print(f"   Найдено терминов: {len(terms)}")
            all_terms.update(terms)
        else:
            print(f"   ⚠️ Нет данных")
    
    print(f"\n📊 Всего уникальных терминов: {len(all_terms)}")
    
    # Создаём выходной каталог
    output_dir = Path("dict_full")
    output_dir.mkdir(exist_ok=True)
    
    # Сортируем термины
    sorted_terms = sorted(all_terms)
    output_file = output_dir / "dictionary.txt"
    
    # Записываем объединённый словарь
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Gboard Dictionary version:2\n")
        f.write("# Gboard Dictionary format:shortcut\tword\tlanguage_tag\tpos_tag\n")
        f.write(f"# Полный словарь православных терминов со склонениями\n")
        f.write(f"# Всего терминов: {len(sorted_terms)}\n")
        
        for term in sorted_terms:
            f.write(f"\t{term}\tru-RU\t\n")
    
    print(f"\n✅ Объединённый словарь сохранён: {output_file}")
    print(f"   Всего записей: {len(sorted_terms)}")
    
    # Создаём файл статистики
    stats_file = output_dir / "statistics.txt"
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("СТАТИСТИКА ОБЪЕДИНЁННОГО СЛОВАРЯ\n")
        f.write("="*80 + "\n\n")
        f.write(f"Всего уникальных словоформ: {len(sorted_terms)}\n\n")
        f.write("Источники:\n")
        
        # Используем сохраненные данные
        for part_name in partitions:
            f.write(f"  - {part_name}: {stats_counts[part_name]} терминов\n")
        
        f.write(f"\nВыходной файл: dict_full/dictionary.txt\n")
        f.write(f"Формат: Gboard Dictionary (для импорта в Gboard)\n")
    
    print(f"✅ Статистика сохранена: {stats_file}")
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print(f"\n📂 Объединённый словарь: dict_full/dictionary.txt")
    print(f"📊 Статистика: dict_full/statistics.txt")
    print(f"\n💡 Импортируйте dict_full/dictionary.txt в Gboard для использования!")

if __name__ == "__main__":
    merge_all_dictionaries()
