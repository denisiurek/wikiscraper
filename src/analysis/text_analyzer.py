import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from wordfreq import top_n_list
from wordfreq import word_frequency


class TextAnalyzer:
    @staticmethod
    def sum_word_occurrences(df: pd.DataFrame) -> pd.DataFrame:
        frequency_table = df.stack().value_counts().reset_index()
        frequency_table.columns = ['word', 'wiki freq']
        return frequency_table

    @staticmethod
    def update_word_counts_json(word_counts: pd.DataFrame, file_name: str):
        if os.path.exists(file_name):
            word_counts = pd.concat([pd.read_json(file_name), word_counts])
            word_counts = word_counts.groupby('word', as_index=False).sum()
            word_counts = word_counts.sort_values(by='wiki freq', ascending=False)
            word_counts.to_json(file_name, orient="records")
        else:
            word_counts.to_json(file_name, orient="records")
        return

    @staticmethod
    def analyze_rel_word_freq(mode: str, count: int, lang: str, json_path: str) -> pd.DataFrame:
        if not os.path.exists(json_path):
            raise FileNotFoundError("File not found: " + json_path)

        df_article = pd.read_json(json_path)
        df_article = df_article[['word', 'wiki freq']]
        if mode == "article":

            df_article['lang_freq'] = df_article['word'].apply(lambda x: word_frequency(x, lang))
            df_final = df_article.copy()
        else:
            top_words = top_n_list(lang, 1000)
            df_lang = pd.DataFrame(top_words, columns=['word'])
            df_lang['lang_freq'] = df_lang['word'].apply(lambda x: word_frequency(x, lang))

            df_final = pd.merge(df_lang, df_article, on='word', how='left')

        if not df_final['wiki freq'].dropna().empty:
            df_final['wiki freq'] = df_final['wiki freq'] / df_final['wiki freq'].max()
        else:
            df_final['wiki freq'] = df_final['wiki freq']

        if not df_final['lang_freq'].dropna().empty:
            df_final['lang freq'] = df_final['lang_freq'] / df_final['lang_freq'].max()
        else:
            df_final['lang freq'] = df_final['lang_freq']

        if mode == "article":
            df_final = df_final.sort_values(by='wiki freq', ascending=False)
        else:
            df_final = df_final.sort_values(by='lang_freq', ascending=False)

        return df_final[['word', 'wiki freq', 'lang freq']].head(count)

    @staticmethod
    def plot_rel_word_freq(df: pd.DataFrame, chart_path: str):
        words = df['word'].tolist()

        data_to_plot = {'Article': df['wiki freq'].fillna(0).tolist(),
                        'Language': df['lang freq'].fillna(0).tolist(), }

        x = np.arange(len(words))
        width = 0.35
        multiplier = 0

        fig, ax = plt.subplots(figsize=(12, 7), layout='constrained')

        for label, measurement in data_to_plot.items():
            offset = width * multiplier

            rects = ax.bar(x + offset, measurement, width, label=label)

            ax.bar_label(rects, padding=3, fmt='%.2f', fontsize=12)
            multiplier += 1

        ax.set_ylabel('Normalized Frequency (0.0 - 1.0)')
        ax.set_title('Relative Word Frequency: Article vs. General Language')

        ax.set_xticks(x + width / 2, words)
        ax.tick_params(axis='x', rotation=45)

        ax.legend(loc='upper right', ncols=2)

        ax.set_ylim(0, 1.2)

        plt.savefig(chart_path, dpi=600)
        plt.close()
        print(f"Chart saved to {chart_path}")
