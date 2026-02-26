#!/usr/bin/env python3
"""
Скрипт для объединения всех полных словарей в один файл
Объединяет part_1_full - part_7_full в dict_full/dictionary.txt

Использование:
python merge_dictionaries.py
"""

<<<<<<< Updated upstream
import pymorphy2, pymorphy3
import re
=======
>>>>>>> Stashed changes
from pathlib import Path
from typing import Set

def parse_dictionary_file(filepath: str) -> Set[str]:
    """Извлекает термины из файла словаря Gboard"""
<<<<<<< Updated upstream
    terms = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Убираем только перевод строки, но НЕ табы
            line = line.rstrip('\r\n')
            # Пропускаем комментарии и пустые строки
            if line.startswith('#') or not line:
                continue
            # Извлекаем термин (второе поле после TAB)
            parts = line.split('\t')
            if len(parts) >= 2 and parts[1]:
                terms.append(parts[1])
    return terms

def is_capitalizable(term: str) -> bool:
    """Проверяет, начинается ли термин с заглавной буквы"""
    return term and term[0].isupper()

def capitalize_if_needed(word: str, original_word: str) -> str:
    """Сохраняет регистр первой буквы как в оригинале"""
    if is_capitalizable(original_word):
        return word.capitalize()
    return word.lower()

def inflect_single_word(word: str, case: str, number: str, original_word: str) -> str:
    """
    Склоняет одно слово
    case: 'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct'
    number: 'sing', 'plur'
    """
    parsed = morph.parse(word.lower())[0]

    # Проверяем, склоняется ли слово
    if 'NOUN' not in parsed.tag and 'ADJF' not in parsed.tag and 'NPRO' not in parsed.tag:
        # Для несклоняемых слов возвращаем исходную форму
        return capitalize_if_needed(word, original_word)

    try:
        inflected = parsed.inflect({case, number})
        if inflected:
            result = inflected.word
            return capitalize_if_needed(result, original_word)
    except:
        pass

    # Если не удалось просклонять, возвращаем исходную форму
    return capitalize_if_needed(word, original_word)

def inflect_phrase(phrase: str) -> Set[str]:
    """
    Склоняет фразу по всем падежам и числам
    Возвращает множество всех уникальных форм
    """
    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
    numbers = ['sing', 'plur']

    forms = set()
    words = phrase.split()

    for number in numbers:
        for case in cases:
            inflected_words = []
            for word in words:
                inflected = inflect_single_word(word, case, number, word)
                inflected_words.append(inflected)

            inflected_phrase = ' '.join(inflected_words)
            forms.add(inflected_phrase)

    return forms

def should_skip_plural(term: str) -> bool:
    """
    Проверяет, нужно ли пропустить множественное число для термина
    Пропускаем для неизменяемых слов и некоторых абстрактных понятий
    """
    # Проверяем первое слово термина
    first_word = term.split()[0].lower()
    parsed = morph.parse(first_word)[0]

    # Если слово не склоняется (неизменяемое)
    if parsed.tag.POS not in ['NOUN', 'ADJF', 'NPRO']:
        return True

    # Проверяем, есть ли у слова форма множественного числа
    plural_form = parsed.inflect({'plur', 'nomn'})
    if not plural_form:
        return True

    return False

def generate_full_dictionary(input_file: str, output_file: str):
    """Генерирует полный словарь со склонениями"""
    print(f"\n[*] Обработка: {input_file}")

    # Читаем исходные термины
    terms = parse_dictionary_file(input_file)
    print(f"   Найдено терминов: {len(terms)}")

    # Генерируем все словоформы
    all_forms = set()

    for term in terms:
        # Добавляем базовую форму
        all_forms.add(term)

        # Генерируем склонения
        inflected = inflect_phrase(term)

        # Если нужно пропустить множественное число, фильтруем
        if should_skip_plural(term):
            # Оставляем только формы единственного числа
            cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
            sing_forms = set()
            words = term.split()

            for case in cases:
                inflected_words = []
                for word in words:
                    infl = inflect_single_word(word, case, 'sing', word)
                    inflected_words.append(infl)
                sing_forms.add(' '.join(inflected_words))

            all_forms.update(sing_forms)
=======
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
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        for form in sorted_forms:
            f.write(f"\t{form}\tru-RU\t\n")

    print(f"   [OK] Сохранено в: {output_file}")
    return len(sorted_forms)

def main():
    """Основная функция обработки всех партий"""
    print("="*80)
    print("ГЕНЕРАЦИЯ ПОЛНЫХ СЛОВАРЕЙ СО СКЛОНЕНИЯМИ")
    print("="*80)

    # Партии для обработки: part_1, part_2, ..., part_7
    partitions = [
        ('part_1', 'dictionary.txt', 'part_1_full'),
        ('part_2', 'dictionary.txt', 'part_2_full'),
        ('part_3', 'dictionary.txt', 'part_3_full'),
        ('part_4', 'dictionary.txt', 'part_4_full'),
        ('part_5', 'dictionary.txt', 'part_5_full'),
        ('part_6', 'dictionary.txt', 'part_6_full'),
        ('part_7', 'dictionary.txt', 'part_7_full'),
    ]

    total_forms = 0

    for part_name, dict_file, output_dir_name in partitions:
        # Путь к исходному файлу
        input_path = f"{part_name}/{dict_file}"

        # Создаём каталог для полного словаря
        Path(output_dir_name).mkdir(exist_ok=True)

        # Путь к выходному файлу
        output_path = f"{output_dir_name}/dictionary.txt"

        # Генерируем словарь
        forms_count = generate_full_dictionary(input_path, output_path)
        total_forms += forms_count

=======
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
>>>>>>> Stashed changes
    print("\n" + "="*80)
    print("ГОТОВО!")
    print("="*80)
    print(f"\n📂 Объединённый словарь: dict_full/dictionary.txt")
    print(f"📊 Статистика: dict_full/statistics.txt")
    print(f"\n💡 Импортируйте dict_full/dictionary.txt в Gboard для использования!")

if __name__ == "__main__":
    merge_all_dictionaries()
