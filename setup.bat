@echo off
REM caption_ordering_by_NLTKのセットアップスクリプト

REM 仮想環境の作成
python -m venv venv
call venv\Scripts\activate

REM 必要なライブラリのインストール
pip install nltk

REM NLTKの追加データのダウンロード
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

REM 仮想環境の終了
call venv\Scripts\deactivate

echo.
echo セットアップが完了しました。
pause
