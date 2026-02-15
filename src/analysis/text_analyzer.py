import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from wordfreq import top_n_list
from wordfreq import word_frequency
import seaborn as sns


class TextAnalyzer:
    @staticmethod
    def sum_word_occurrences(df: pd.DataFrame) -> pd.DataFrame:
        frequency_table = df.stack().value_counts().reset_index()
        frequency_table.columns = ['word', 'wiki freq']
        return frequency_table

    @staticmethod
    def update_word_counts_json(word_counts: pd.DataFrame, file_path: Path):
        if os.path.exists(file_path):
            word_counts = pd.concat([pd.read_json(file_path), word_counts])
            word_counts = word_counts.groupby('word', as_index=False).sum()
            word_counts = word_counts.sort_values(by='wiki freq', ascending=False)
            word_counts.to_json(file_path, orient="records")
        else:
            word_counts.to_json(file_path, orient="records")
        return

    @staticmethod
    def analyze_rel_word_freq(mode: str, count: int, lang: str, json_path: Path) -> pd.DataFrame:
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        df_json = pd.read_json(path)
        df_json = df_json[['word', 'wiki freq']].set_index('word')

        if mode == "article":
            target_words = df_json.index.tolist()
        else:
            target_words = top_n_list(lang, 1000)

        df = pd.DataFrame({'word': target_words})

        df['wiki freq'] = df['word'].map(df_json['wiki freq']).fillna(0)
        df['lang freq'] = [word_frequency(w, lang) for w in df['word']]

        for col in ['wiki freq', 'lang freq']:
            max_val = df[col].max()
            if max_val > 0:
                df[col] = df[col] / max_val

        sort_column = 'wiki freq' if mode == "article" else 'lang freq'

        return df.sort_values(by=sort_column, ascending=False).head(count).reset_index(drop=True)

    @staticmethod
    def plot_rel_word_freq(df: pd.DataFrame, chart_path: Path):
        df_melted = df.melt(id_vars=['word'], value_vars=['wiki freq', 'lang freq'],
                            var_name='source', value_name='frequency')

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))

        ax = sns.barplot(x="word", y="frequency", hue="source", data=df_melted)

        ax.tick_params(axis='x', rotation=55)

        plt.title("Relative Word Frequency: Wiki vs Language")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
