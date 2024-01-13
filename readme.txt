#######注意点#######

windows/python3の環境を想定しています。
stable diffusionの拡張ではありません。気が向いたら拡張として実装します。
stable diffusionをローカルで動かしている人たちならpython3.10.6などの環境で簡単に動かせると思います。
主な利用方法としてはwd-14-taggerなどで出力した.txtファイルをそのまま読み込ませることで大量のキャプションファイルを同時に組み分けできます。
どのような処理が行われたか見やすいようにordering.py内でprint処理を行っていますが、大量の文字列が出力されるため気になる人は書き換えてください。

readme.txtを読みましょう。大抵のことは書いておきました。
sample.txtというファイルがinputの中に入っています。
categories.txtやregex.txtにも仮のファイルは置いてあるので試したい方はどうぞ。

#######実装意図について#######

NovelAIV3やAnimagineXLで利用されたというキャプションのグループ化/固定化がLoRA学習にどのような影響を与えることができるのか。
これを調べるために一括でキャプションの組み合わせを変更できる簡易的なものを実装しました。
とても簡素なコードでかつ、自然言語による説明が多く含まれているため、ordering.pyファイルを直接覗いてみてもいいと思います。
現状のコードでは1girl/1boy/1otherなどのキャラクター/人物を学習するための設定となっています。
しかし、設定を少し編集すれば、特定のポーズや小物などにも応用が効くでしょう。
このコードは最高のLoRA学習のためのものではなく、画像生成モデルのキャプションをどう処理すればより効率的になるかを考えるためのコードです。

#######仕様について#######

ordering.pyを覗いてください。
入力されたファイルを一括で読み込み、NLTKと正規表現を用いて部分/一致検索を掛けているだけです。
その結果としてcategories.txtで設定した通りの順序で出力されます。
基本的に必要な設定はcategories.txtとregex.txtのみで行えます。
categories.txtやregex.txtともに扱われていない単語は仕様上ランダムに出力されます。
NLTKを用いて品詞ごとに区分し、並べ替えてはいますが、それ以上の処理をしていません。
なぜならLoRA学習において、全ての画像のキャプションを完全に一致させることがあまり良いことだと断言できないからです。
もし必要であれば、sort処理を追加することで簡単に実現可能ですが、既定のコードでは設定されていません。

#######インストール方法について#######

setup.batを起動してください。
もし上手くいかない場合は、下のコードを利用して仮想環境の作成、ライブラリのインストールを行ってください。

#仮想環境の作成

python -m venv venv
call venv\Scripts\activate

#必要なライブラリのインストール

pip install nltk

#NLTKの追加データのダウンロード

python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

#######実行する前にやるべきこと#######

1, wd-14-taggerなどで既にタグ付けされた.txtファイルをinputに入れる。
2, categories.txtとregex.txtを編集し、並び替えたいタグを入力する。

#######起動方法について#######

run.batを起動してください。
もし上手くいかない場合は、下のコードを利用しても構いません。.batファイルの内容と同じものです。

@echo off
cd caption_ordering_by_NLTK
call venv\Scripts\activate
python ordering.py
pause

#######基本的な記述方式について#######

#categories.txtの書式

カテゴリ名 コロン 半角スペース 単語 カンマ 半角スペース 単語
となっているため、半角スペースの入れ忘れや最後の単語の後にカンマを入れないことに注意してください。
入力ミスがある場合、読み込まれないか、エラーを吐きます。

#文字列の順序

categories.txtに存在するカテゴリ名を入れ替えることによって出力される文字列の順序を入れ替えることが可能です。
上に記載されているものから順に.txtファイルに出力されます。
正規表現を扱っているregex.txtのファイル名を入れ替える必要はありません。

character_pattern: 1girl
proper_nouns: c.c., code geass
verbs: eating

この場合、出力される文字列は"1girl, c.c., code geass, eating"となります。

verbs: eating
proper_nouns: c.c., code geass
character_pattern: 1girl

この場合、出力される文字列は"eating, c.c., code geass, 1girl"となります。

そして、ここで扱われているカテゴリ名はあくまでも便宜上定義されている名称に過ぎません。

verbs: 1girl
proper_nouns: eating 
character_pattern: 

このように変更してもカテゴリ名と矛盾しているような形式でも動作します。
前述の通り、文字列の順序がカテゴリ名に依存していることを理解した上で変更を行ってください。

#新規カテゴリの追加

categories.txtに上記の書式で追加することによって、新たなカテゴリを追加することができます。
正規表現を利用しない場合、regex.txtへの書き込みは不要です。categories.txtのみへの書き込みで動作します。
空欄のカテゴリを用意しても意味がないので、categories.txtやregex.txtを利用してタグを設定してください。

#######categories.txtのカテゴリ名について#######

#classfield_tag(NLTK利用部分のカテゴリ名)

classified_tags['adjectives'].append(tag)の[]の中のファイル名がcategories.txtと結びついています。
そのため、両方の名称が共通していれば、適当な名称に変更して問題ないはずです。
新規でカテゴリの追加が可能であるため、変更する必要はないと思います。
この手法は、proper_nouns: c.c., code geassのようにNLTKでは判断できない固有名詞に対して有効です。
現状では、NLTKを利用しているため、品詞の名称がついています。

            if last_pos.startswith('JJ'):
                classified_tags['adjectives'].append(tag)
            elif last_pos.startswith('NN'):
                classified_tags['nouns'].append(tag)
            elif last_pos.startswith('VB'):
                classified_tags['verbs'].append(tag)
            elif last_pos.startswith('RB'):
                classified_tags['adverbs'].append(tag)
            else:
                classified_tags['others'].append(tag)

形容詞:JJ(原形),JJR(比較級),JJS(最上級)
名詞:NN(単数),NNS(複数),NNP(単数の固有名詞),NNPS(複数の固有名詞)
副詞:RB(原形),RBR(比較級),RBS(最上級)
動詞:VB(原形),VBD(過去形),VBG(現在分詞),VBN(過去分詞),VBP(現在形系),VBZ(三人称単数の現在形)

以上の品詞の名称を利用することで、分類に利用する条件を変更することができます。
現状では、固有名詞、形容詞、名詞、動詞、副詞、それに当てはまらなかったものの6つに区分されます。

#######正規表現の利用について#######

#記述方法について

既定の設定において、categories.txtに含まれるcharacter_patternとquality_patternはregex.txtにて正規表現も扱っています。
注意点として、コードの仕様上categories.txtにてカテゴリ名を定義した後に扱う必要があります。
そのため、新規の正規表現カテゴリを増設する際はcategories.txtとの整合性をチェックする必要があります。
また、regex.txtの内容は空欄でも構いませんし、一つのカテゴリに複数の正規表現を扱うことも可能です。
記述方法はcategories.txtと変わりません。

character_pattern: 1(girl|boy|other), 2(girls|boys|others), 3(girls|boys|others)

#正規表現の凡例

A+girlという単語という組み合わせ→\b(\w+)\s+girl\b
A+Bという単語の組み合わせ→\b(\w+)(\s+)(\w+)\b
A+B+Cという組み合わせ→\b(\w+\s+)*(\w+)\b

よくわからない場合はChatGPTやMicrosoft Copilotにこの単語の組み合わせを正規表現にしたいと伝えればいいと思います。

#######なにかあれば#######

もしなにかあった場合には、Githubのissuesにどうぞ。
簡単なコードなので修正点や変更点とともにChatGPTやCopilotなどに与えても良いと思います。

