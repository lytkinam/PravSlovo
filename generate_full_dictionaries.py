
"""
Скрипт для создания полных словарей православных терминов со склонениями
Обрабатывает партии part_1 - part_7 и создаёт каталоги part_[N]_full
"""

import pymorphy3
import re
from pathlib import Path
from typing import List, Set

# Инициализация морфологического анализатора
morph = pymorphy3.MorphAnalyzer()

def parse_dictionary_file(filepath: str) -> List[str]:
    """Извлекает термины из файла словаря Gboard"""
    terms = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
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
    print(f"\n📖 Обработка: {input_file}")

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
        else:
            all_forms.update(inflected)

    # Сортируем для удобства
    sorted_forms = sorted(all_forms)

    print(f"   Сгенерировано словоформ: {len(sorted_forms)}")

    # Записываем в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Gboard Dictionary version:2\n")
        f.write("# Gboard Dictionary format:shortcut\tword\tlanguage_tag\tpos_tag\n")
        for form in sorted_forms:
            f.write(f"\t{form}\tru-RU\t\n")

    print(f"   ✅ Сохранено в: {output_file}")
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

    print("\n" + "="*80)
    print(f"ВСЕГО СГЕНЕРИРОВАНО: {total_forms} словоформ")
    print("="*80)

if __name__ == "__main__":
    main()
