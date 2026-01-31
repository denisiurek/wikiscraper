import pandas as pd


class TextAnalyzer:
    @staticmethod
    def sum_word_occurences(df: pd.DataFrame) -> pd.DataFrame:
        frequency_table = df.stack().value_counts().reset_index()
        frequency_table.columns = ['Phrase', 'Times Occurred']
        return frequency_table
