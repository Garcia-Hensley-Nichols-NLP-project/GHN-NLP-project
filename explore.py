'''

    explore.py

    Description: This file contains functions used for producing visualizations
        and conducting statistical tests in the final report notebook.

    Variables:

        None

    Functions:

        

'''

################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from wordcloud import WordCloud

################################################################################

def plot_most_frequent_words(df: pd.DataFrame) -> None:
    '''
        Create plots displaying the most frequent words for each programming 
        language.
    
        Parameters
        ----------
        df: DataFrame
            A pandas dataframe containing natural language data. The data should 
            ideally be prepared.
    '''

    n = 10
    fig, ax = plt.subplots(ncols = 1, nrows = 4, figsize = (14, 16))

    python_words = ' '.join(text for text in df[df.language == 'Python'].clean)
    cpp_words = ' '.join(text for text in df[df.language == 'C++'].clean)
    javascript_words = ' '.join(text for text in df[df.language == 'JavaScript'].clean).replace('&#9;', '')
    other_words = ' '.join(text for text in df[df.language == 'other'].clean).replace('&#9;', '')

    python_words_freq = pd.Series(python_words.split())
    python_words_freq.value_counts().head(n).plot.barh(ax = ax[0])

    cpp_words_freq = pd.Series(cpp_words.split())
    cpp_words_freq.value_counts().head(n).plot.barh(ax = ax[1])

    javascript_words_freq = pd.Series(javascript_words.split())
    javascript_words_freq.value_counts().head(n).plot.barh(ax = ax[2])

    other_words_freq = pd.Series(other_words.split())
    other_words_freq.value_counts().head(n).plot.barh(ax = ax[3])