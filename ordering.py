import os
import re
from collections import defaultdict
import nltk
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize

def load_categories(file_path):
    categories = {}
    category_order = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, values = line.strip().split(':')
            values_list = values.split(',')
            categories[key] = values_list
            for i, value in enumerate(values_list):
                category_order[value] = i
    return categories, category_order

def load_ordered_categories(file_path):
    ordered_categories = []
    with open(file_path, 'r') as file:
        for line in file:
            key = line.strip().split(':')[0]
            ordered_categories.append(key)
    return ordered_categories

def load_regex_patterns(file_path):
    patterns = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, pattern_str = line.strip().split(':')
            pattern_list = [re.compile(p.strip()) for p in pattern_str.split(',')]
            patterns[key] = pattern_list
    return patterns

# カテゴリと順序付きカテゴリのファイルパスを指定
categories_file_path = './categories/categories.txt'
regex_file_path = './categories/regex.txt'

# ファイルからカテゴリを読み込む
categories, category_order = load_categories(categories_file_path)
ordered_categories = load_ordered_categories(categories_file_path)
regex_patterns = load_regex_patterns(regex_file_path)

# 入力タグファイルのディレクトリを指定
tags_files_directory = './input'

# 出力ディレクトリを指定
output_directory = './output'

# ディレクトリ内のファイル名を取得し、.txtファイルのみをフィルタリング
tags_files_paths = [os.path.join(tags_files_directory, file) for file in os.listdir(tags_files_directory) if file.endswith('.txt')]

for tags_file_path in tags_files_paths:
    # 入力ファイルの名前を取得し、出力ファイル名を生成
    tags_file_name = os.path.basename(tags_file_path)
    output_file_name = f"{tags_file_name}"
    output_file_path = os.path.join(output_directory, output_file_name)

    # 入力ファイルをUTF-8エンコーディングで開く
    with open(tags_file_path, 'r', encoding='utf-8') as file:
        tags = file.read().strip().split(',')

    # 分類されたタグを格納する辞書を初期化
    classified_tags = defaultdict(list)
    for i, tag in enumerate(tags):
        matched = False
        for pattern_name, patterns in regex_patterns.items():
            for pattern in patterns:
                if pattern.search(tag):
                    classified_tags[pattern_name].append(tag)
                    matched = True
                    break

        if matched:
            continue

        # カテゴリファイルからの単語に基づいて分類
        categorized = False
        for category, words in categories.items():
            if tag in words:
                classified_tags[category].append(tag)
                categorized = True
                break

        # タグをトークナイズし、品詞を割り当てる
        words = word_tokenize(tag)
        tagged_words = pos_tag(words)

        # タグ内の単語の品詞を評価
        if not categorized and len(tagged_words) > 0:
            for word, pos in tagged_words:

            # 固有名詞をカテゴリとして分類
                if pos in ['NNP', 'NNPS']:
                    classified_tags['proper_nouns'].append(tag)
                    break

                elif pos.startswith('VB'):
                    classified_tags['verbs'].append(tag)
                    break
                elif pos.startswith('JJ'):
                    classified_tags['adjectives'].append(tag)
                    break
                elif pos.startswith('RB'):
                    classified_tags['adverbs'].append(tag)
                    break
                elif pos.startswith('NN'):
                    classified_tags['nouns'].append(tag)
                    break
            else:
                classified_tags['others'].append(tag)

    # カテゴリごとにタグを取得し、それらをカンマで区切った文字列に結合する
    ordered_tags = []
    for category in ordered_categories:
         category_tags = sorted(classified_tags[category], key=lambda tag: category_order.get(tag, float('inf')))
         ordered_tags.extend(category_tags)

    # 最終的なタグの文字列を生成
    formatted_tags = ', '.join(ordered_tags)
    with open(output_file_path, 'w', encoding='utf-8') as file:
          file.write(formatted_tags)
          print(formatted_tags)

