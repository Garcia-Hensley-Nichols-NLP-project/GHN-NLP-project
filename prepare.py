# prepare.py

from imports import *

################################################################################

python_keywords = [
    'python',
    'pip',
    'pddataframe',
    'python3',
    'pandas',
    'matplotlib',
    'seaborn',
    'bitcoinlib',
    'cryptocompare',
    'cryptofeed',
    'freqtrade',
    'ccxt',
    'pytest'
]

cpp_keywords = [
    'c\+\+',
    'c',
    'blackbird',
    'gnu',
    'g\+\+',
    'make'
]

js_keywords = [
    'js',
    'docker',
    'npm',
    'javascript',
    'node',
    'react',
    'nodejs',
    'reactjs',
    'node.js',
    'react.js'
    'ccxt'
]

################################################################################


def basic_clean(original):
	'''
	takes an original string and outputs a tidy "article"
	'''
	article=original.lower()
	article = unicodedata.normalize('NFKD', article).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	article = re.sub(r"[^a-z\s\+]", '', article)
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

    df['contains_python_keywords'] = df.clean.str.contains(''.join(fr'({keyword})|' for keyword in python_keywords).rstrip('|'), regex = True).astype(int)
    df['contains_cpp_keywords'] = df.clean.str.contains(''.join(fr'({keyword})|' for keyword in cpp_keywords).rstrip('|'), regex = True).astype(int)
    df['contains_js_keywords'] = df.clean.str.contains(''.join(fr'({keyword})|' for keyword in js_keywords).rstrip('|'), regex = True).astype(int)
    df['readme_size'] = df.clean.apply(len)

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

def classi_bow(X_lem_train,y_lem_train,X_stem_train,y_stem_train,X_clean_train,y_clean_train):

    # Make vectorizer objects for bags of words (clean_df)
    cv_clean = CountVectorizer()
    tfidf_clean = TfidfVectorizer()

    #Bags of words
    cv_clean_bow = cv_clean.fit_transform(X_clean_train[['clean']].clean)
    tf_clean_bow = tfidf_clean.fit_transform(X_clean_train[['clean']].clean)
    
    # Make and fit decision tree object for cv_clean_bow
    cv_tree1 = DecisionTreeClassifier(max_depth=5)
    cv_tree1.fit(cv_clean_bow, y_clean_train)

    #Make and fit decision tree object for tf_clean_bow
    tf_tree1 = DecisionTreeClassifier(max_depth=5)
    tf_tree1.fit(tf_clean_bow, y_clean_train)


    # "Stemmed" models
    cv_stem = CountVectorizer()
    tfidf_stem = TfidfVectorizer()

    # Bags
    cv_stem_bow = cv_stem.fit_transform(X_stem_train[['stemmed']].stemmed)
    tf_stem_bow = tfidf_stem.fit_transform(X_stem_train[['stemmed']].stemmed)

    # Make and fit decision tree object for cv_stem_bow
    cv_tree2 = DecisionTreeClassifier(max_depth=5)
    cv_tree2.fit(cv_stem_bow, y_stem_train)

    # Make and fit decision tree object for tf_stem_bow
    tf_tree2 = DecisionTreeClassifier(max_depth=5)
    tf_tree2.fit(tf_stem_bow, y_stem_train)


    # "Lemmatized" models
    cv_lem = CountVectorizer()
    tfidf_lem = TfidfVectorizer()

    # Bags
    cv_lem_bow = cv_lem.fit_transform(X_lem_train[['lemmatized']].lemmatized)
    tf_lem_bow = tfidf_lem.fit_transform(X_lem_train[['lemmatized']].lemmatized)

    # Make and fit decision tree object for cv_lem_bow
    cv_tree3 = DecisionTreeClassifier(max_depth=5)
    cv_tree3.fit(cv_lem_bow, y_lem_train)

    #Make and fit decision tree object for tf_lem_bow
    tf_tree3 = DecisionTreeClassifier(max_depth=5)
    tf_tree3.fit(tf_lem_bow, y_lem_train)


    dec_tree_training_scores=pd.Series({
        'CV_clean': cv_tree1.score(cv_clean_bow, y_clean_train),
        'CV_stem': cv_tree2.score(cv_stem_bow, y_stem_train),
        'CV_lem': cv_tree3.score(cv_lem_bow, y_lem_train),
        'TFIDF_clean': tf_tree1.score(tf_clean_bow, y_clean_train),
        'TFIDF_stem': tf_tree2.score(tf_stem_bow, y_stem_train),
        'TFIDF_lem': tf_tree3.score(tf_lem_bow, y_lem_train)
    })

    return dec_tree_training_scores