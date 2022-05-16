# prepare.py

from imports import *


def basic_clean(original):
	'''
	takes an original string and outputs a tidy "article"
	'''
	article=original.lower()
	article = unicodedata.normalize('NFKD', article).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	article = re.sub(r"[^a-z\s]", '', article)
	return article

def tokenize(article):
	'''
	tokenizes an "article"
	'''
	tokenizer = nltk.tokenize.ToktokTokenizer()
	article_token=tokenizer.tokenize(article, return_str=True)
	return article_token


def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    
    # Join our lists of words into a string again and assign to a variable.
    string = ' '.join(stems)
    
    return string

def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string.
    words = string.split()
    
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords

def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''

    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(stem)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    
    return df[['repo','language', column,'clean', 'stemmed', 'lemmatized']]

def words_explore(df):
    '''
    !!!  please run `python aquire.py` in terminal prior to utilizing 'prepare.py' !!!
    ---
    this function returns 'readme's' for the first 100 repos returned by the search term "bitcoin" on github. 
    the results include 'repo', 'language', and 'readme'.
    'readme' is a string which is cleaned, trimmed, and lemmetized for exploration and modeling.
    '''
    # rename columns
    df=df.rename(columns={'readme_contents':'readme'})
    # clean readme contents and return cleaned, trimmed, and lemmetized versions
    df=prep_article_data(df,'readme')
    # consolidate languages other than the top 3 into 'other'
    rows=(df.language!='Python')&(df.language!='C++')&(df.language!='JavaScript')
    df.loc[rows,'language']='other'

    return df

def words(df):
    '''
    !!!  please run `python aquire.py` in terminal prior to utilizing 'prepare.py' !!!
    ---
    this function returns 'readme's' for the first 100 repos returned by the search term "bitcoin" on github. 
    the results include 'repo', 'language', and 'readme'.
    'readme' is a string which is cleaned, trimmed, and lemmetized for exploration and modeling.
    '''
    # rename columns
    df=df.rename(columns={'readme_contents':'readme'})
    # clean readme contents and return cleaned, trimmed, and lemmetized versions
    df=prep_article_data(df,'readme')
    # consolidate languages other than the top 3 into 'other'
    rows=(df.language!='Python')&(df.language!='C++')&(df.language!='JavaScript')
    df.loc[rows,'language']='other'

    df['contains_python_keywords'] = df.clean.str.contains(r'(python)|(import)|(pip)|(pddataframe)|(python3)', regex = True).astype(int)
    df['contains_cpp_keywords'] = df.clean.str.contains(r'(windows)|(linux)|(blackbird)', regex = True).astype(int)
    df['contains_js_keywords'] = df.clean.str.contains(r'(js)|(docker)|(ccxt)|(npm)', regex = True).astype(int)

    return df

def model_prep(df):
	# Make copies of df with prepared columns and target
	clean_df = df.copy()[['language', 'clean']]
	stem_df = df.copy()[['language', 'stemmed']]
	lem_df = df.copy()[['language', 'lemmatized']]

	# Get splits for each of the above dfs and isolate target
	X_clean = clean_df[['clean']]
	y_clean = clean_df.language

	X_clean_train, X_clean_test, y_clean_train, y_clean_test = train_test_split(X_clean, y_clean, test_size=.2, random_state=302)
	X_clean_train, X_clean_validate, y_clean_train, y_clean_validate  = train_test_split(X_clean_train, y_clean_train, test_size=.3, random_state=302)

	X_stem = stem_df[['stemmed']]
	y_stem = stem_df.language

	X_stem_train, X_stem_test, y_stem_train, y_stem_test = train_test_split(X_stem, y_stem, test_size=.2, random_state=302)
	X_stem_train, X_stem_validate, y_stem_train, y_stem_validate  = train_test_split(X_stem_train, y_stem_train, test_size=.3, random_state=302)

	X_lem = lem_df[['lemmatized']]
	y_lem = lem_df.language

	X_lem_train, X_lem_test, y_lem_train, y_lem_test = train_test_split(X_lem, y_lem, test_size=.2, random_state=302)
	X_lem_train, X_lem_validate, y_lem_train, y_lem_validate  = train_test_split(X_lem_train, y_lem_train, test_size=.3, random_state=302)

	return (X_lem_train,
	X_lem_validate,
	X_lem_test,
	y_lem_train,
	y_lem_validate,
	y_lem_test,
	X_stem_train,
	X_stem_validate,
	X_stem_test,
	y_stem_train,
	y_stem_validate,
	y_stem_test,
	X_clean_train,
	X_clean_validate,
	X_clean_test,
	y_clean_train,
	y_clean_validate,
	y_clean_test)