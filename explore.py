'''

    explore.py

    Description: This file contains functions used for producing visualizations
        and conducting statistical tests in the final report notebook.

    Variables:

        None

    Functions:

        plot_most_frequent_words(df)
        plot_readme_size_vs_language(df, group_column = 'language')
        one_sample_ttest(df, sample, column, alternative = 'two-sided')

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

    # Show the top 5 most frequent words.
    n = 5
    fig, ax = plt.subplots(ncols = 1, nrows = 3, figsize = (14, 8))

    # Get the top 20 most frequent words across all repos.
    clean_words = ' '.join(readme for readme in df.clean)
    clean_words_freq = pd.Series(clean_words.split()).value_counts().head(20)

    # Combine all words for each programming language into single strings.
    python_words = ' '.join(text for text in df[df.language == 'Python'].clean)
    cpp_words = ' '.join(text for text in df[df.language == 'C++'].clean)
    javascript_words = ' '.join(text for text in df[df.language == 'JavaScript'].clean).replace('&#9;', '')

    # Remove the top 20 most frequent words across all repos for each group.
    python_words = ' '.join(word for word in python_words.split() if word not in clean_words_freq)
    cpp_words = ' '.join(word for word in cpp_words.split() if word not in clean_words_freq)
    javascript_words = ' '.join(word for word in javascript_words.split() if word not in clean_words_freq)

    # Create plots for the most frequent words for each programming language

    python_words_freq = pd.Series(python_words.split())
    python_words_freq.value_counts().head(n).plot.barh(ax = ax[0])
    ax[0].set_title('Most Frequent Words in Python Repository READMEs')
    ax[0].set_xlabel('Word Count')
    ax[0].set_ylabel('Words')

    cpp_words_freq = pd.Series(cpp_words.split())
    cpp_words_freq.value_counts().head(n).plot.barh(ax = ax[1])
    ax[1].set_title('Most Frequent Words in C++ Repository READMEs')
    ax[1].set_xlabel('Word Count')
    ax[1].set_ylabel('Words')

    javascript_words_freq = pd.Series(javascript_words.split())
    javascript_words_freq.value_counts().head(n).plot.barh(ax = ax[2])
    ax[2].set_title('Most Frequent Words in JavaScript Repository READMEs')
    ax[2].set_xlabel('Word Count')
    ax[2].set_ylabel('Words')

    plt.tight_layout()

    plt.show()

################################################################################

def plot_contains_keywords(df: pd.DataFrame) -> None:
    '''
        Plot a distribution of the contains_keywords features for each 
        programming language.
    
        Parameters
        ----------
        df: DataFrame
            A pandas dataframe containing the readme data.
    '''

    fig, ax = plt.subplots(ncols = 3, nrows = 1, figsize = (14, 4))

    sns.histplot(data = df[df.language == 'Python'], x = 'contains_python_keywords', ax = ax[0])
    ax[0].set_title('Python Repositories')
    ax[0].set_xlabel('Contains Python Keywords')

    sns.histplot(data = df[df.language == 'C++'], x = 'contains_cpp_keywords', ax = ax[1])
    ax[1].set_title('C++ Repositories')
    ax[1].set_xlabel('Contains C++ Keywords')

    sns.histplot(data = df[df.language == 'JavaScript'], x = 'contains_js_keywords', ax = ax[2])
    ax[2].set_title('JavaScript Repositories')
    ax[2].set_xlabel('Contains JavaScript Keywords')

    plt.show()

################################################################################

def plot_readme_size_vs_language(df: pd.DataFrame, group_column: str = 'language') -> None:
    '''
        Create a plot that shows the average readme size grouping by the 
        group_column parameter. By default this will show the average readme 
        size for each programming language in the target variable.
    
        Parameters
        ----------
        df: DataFrame
            A pandas dataframe containing the readme data.

        group_column: str, optional
            The column to group the data by.
    '''

    plt.figure(figsize = (14, 4))

    df.groupby(group_column).readme_size.mean().plot.barh()
    plt.title('Average README file size by programming language')

    plt.xlabel('Average Character Count')
    plt.ylabel('Programming Language')

    plt.show()

################################################################################

def one_sample_ttest(df: pd.DataFrame, sample: pd.DataFrame, column: str, alternative: str = 'two-sided') -> None:
    '''
        Conduct a one sample t-test using the provided dataframe and sample 
        dataframe. The hypothesis is tested on the column parameter. By 
        default a two sided t-test is conducted.
    
        Parameters
        ----------
        df: DataFrame
            A pandas dataframe containing the full population of the data.

        sample: DataFrame
            A pandas dataframe containing the sample that is being tested.

        column: str
            The feature in the data that will be tested.

        alternative: str, optional
            The type of t-test to perform. The default is a two-sided t-test.
    '''

    alpha = 0.05

    t, p = stats.ttest_1samp(sample[column], df[column].mean(), alternative = alternative)

    if p < alpha:
        print('Fail to reject H0')
    else:
        print('Reject H0')