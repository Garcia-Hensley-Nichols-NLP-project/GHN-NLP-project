from os import terminal_size
import pandas as pd
#from prepare import basic_stem, tokenize, stem, lemmatize, remove_stopwords, prep_article_data, words
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split

# Import Decision Tree and Random Forest 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

################################################################################

def get_clean_splits(df):
    '''Takes in a prepared df, 
    and returns train, validate, and test splits with target variable, language, isolated.
    '''
    clean_df = df.copy()[['language', 'clean']]
    
    X_clean = clean_df[['clean']]
    y_clean = clean_df.language

    X_clean_train, X_clean_test, y_clean_train, y_clean_test = train_test_split(X_clean, y_clean, test_size=.2, random_state=302)
    X_clean_train, X_clean_validate, y_clean_train, y_clean_validate  = train_test_split(X_clean_train, y_clean_train, test_size=.3, random_state=302)

    return X_clean_train, y_clean_train, X_clean_validate, y_clean_validate, X_clean_test, y_clean_test

################################################################################

def get_stem_splits(df):
    '''Takes in a prepared df, 
    and returns train, validate, and test splits with target variable, language, isolated.
    '''
    stem_df = df.copy()[['language', 'stemmed']]
    
    X_stem = stem_df[['stemmed']]
    y_stem = stem_df.language

    X_stem_train, X_stem_test, y_stem_train, y_stem_test = train_test_split(X_stem, y_stem, test_size=.2, random_state=302)
    X_stem_train, X_stem_validate, y_stem_train, y_stem_validate  = train_test_split(X_stem_train, y_stem_train, test_size=.3, random_state=302)

    return X_stem_train, y_stem_train, X_stem_validate, y_stem_validate, X_stem_test, y_stem_test

################################################################################

def get_lem_splits(df):
    '''Takes in a prepared df, 
    and returns train, validate, and test splits with target variable, language, isolated.
    '''
    lem_df = df.copy()[['language', 'lemmatized']]
    
    X_lem = lem_df[['lemmatized']]
    y_lem = lem_df.language

    X_lem_train, X_lem_test, y_lem_train, y_lem_test = train_test_split(X_lem, y_lem, test_size=.2, random_state=302)
    X_lem_train, X_lem_validate, y_lem_train, y_lem_validate  = train_test_split(X_lem_train, y_lem_train, test_size=.3, random_state=302)

    return X_lem_train, y_lem_train, X_lem_validate, y_lem_validate, X_lem_test, y_lem_test

################################################################################

def get_vectorizer_dec_trees(text_data, target, max_depth):
    '''
    Takes in text data, a target, and a max depth argument (integer) for a Decision Tree,
    and returns bags of words, Decision Tree objects, and Decision Tree accuracy scores
    corresponding to Count Vectorizer and TF/IDF Vectorizer.
    '''

    # Make vectorizer objects
    cv = CountVectorizer()
    tfidf = TfidfVectorizer()
    
    # Make bags of word (bow)
    cv_bow = cv.fit_transform(text_data)
    tfidf_bow = tfidf.fit_transform(text_data)


    # Make and fit decision tree object for cv
    cv_tree = DecisionTreeClassifier(max_depth=max_depth)
    cv_tree.fit(cv_bow, target)

    #Make and fit decision tree object for tfidf
    tfidf_tree = DecisionTreeClassifier(max_depth=max_depth)
    tfidf_tree1.fit(tfidf_bow, target)

    # Get tree scores
    cv_tree_score = cv_tree.score(cv_bow, target)
    tfidf_tree_score = tfidf_tree.score(tfidf_bow, target)

    return cv_bow, tfidf_bow, cv_tree, tfidf_tree, cv_tree_score, tfidf_tree_score

################################################################################

def get_vectorizer_random_forests(text_data, target, n_estimators, max_depth):
    '''
    Takes in text data, a target, a number of estimators(n_estimators[integer]), and a max depth argument (integer) for a Decision Tree,
    and returns bags of words, Random Forest objects, and Random Forest accuracy scores
    corresponding to Count Vectorizer and TF/IDF Vectorizer.
    '''

    # Make vectorizer objects
    cv = CountVectorizer()
    tfidf = TfidfVectorizer()
    
    # Make bags of word (bow)
    cv_bow = cv.fit_transform(text_data)
    tfidf_bow = tfidf.fit_transform(text_data)


    # Make and fit random forest object for cv
    cv_rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    cv_rf.fit(cv_bow, target)

    #Make and fit decision rf object for tfidf
    tfidf_rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    tfidf_rf1.fit(tfidf_bow, target)

    # Get rf scores
    cv_rf_score = cv_rf.score(cv_bow, target)
    tfidf_rf_score = tfidf_rf.score(tfidf_bow, target)

    return cv_bow, tfidf_bow, cv_rf, tfidf_rf, cv_rf_score, tfidf_rf_score

################################################################################

def get_bigram_vectorizer_dec_trees(text_data, target, max_depth):
    '''
    Takes in text data, a target, and a max depth argument (integer) for a Decision Tree,
    and returns bags of words, Decision Tree objects, and Decision Tree accuracy scores
    corresponding to Count Vectorizer and TF/IDF Vectorizer.
    '''

    # Make vectorizer objects
    cv = CountVectorizer(ngram_range(2,2)) 
    tfidf = TfidfVectorizer(ngram_range(2,2))
    
    # Make bags of word (bow)
    cv_bow = cv.fit_transform(text_data)
    tfidf_bow = tfidf.fit_transform(text_data)


    # Make and fit decision tree object for cv
    cv_tree = DecisionTreeClassifier(max_depth=max_depth)
    cv_tree.fit(cv_bow, target)

    #Make and fit decision tree object for tfidf
    tfidf_tree = DecisionTreeClassifier(max_depth=max_depth)
    tfidf_tree1.fit(tfidf_bow, target)

    # Get tree scores
    cv_tree_score = cv_tree.score(cv_bow, target)
    tfidf_tree_score = tfidf_tree.score(tfidf_bow, target)

    return cv_bow, tfidf_bow, cv_tree, tfidf_tree, cv_tree_score, tfidf_tree_score

################################################################################

def get_bigram_vectorizer_random_forests(text_data, target, n_estimators, max_depth):
    '''
    Takes in text data, a target, a number of estimators(n_estimators[integer]), and a max depth argument (integer) for a Decision Tree,
    and returns bags of words, Random Forest objects, and Random Forest accuracy scores
    corresponding to Count Vectorizer and TF/IDF Vectorizer.
    '''

    # Make vectorizer objects
    cv = CountVectorizer(ngram_range=(2,2))
    tfidf = TfidfVectorizer(ngram_range=(2,2))
    
    # Make bags of word (bow)
    cv_bow = cv.fit_transform(text_data)
    tfidf_bow = tfidf.fit_transform(text_data)


    # Make and fit random forest object for cv
    cv_rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    cv_rf.fit(cv_bow, target)

    #Make and fit decision rf object for tfidf
    tfidf_rf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    tfidf_rf.fit(tfidf_bow, target)

    # Get rf scores
    cv_rf_score = cv_rf.score(cv_bow, target)
    tfidf_rf_score = tfidf_rf.score(tfidf_bow, target)

    return cv_bow, tfidf_bow, cv_rf, tfidf_rf, cv_rf_score, tfidf_rf_score

################################################################################

def get_dt_valtest_score(bow, train_data, valtest_data, target, model):
    '''
    Takes in a previously fit_transformed vectorizer(bag of words[bow]), train data,  validate or test data, a matching target, and a previously 
    fitted model,
    and returns an accuracy score for the model against the unseen text data.
    '''
    
    # Vectorizer object
    bow = TfidfVectorizer()
    bow.fit_transform(train_data)
    # Transform bow on text_data
    bow = bow.transform(valtest_data)
    # Evaluate model accuracy
    model_score = model.score(bow, target)

    return model_score

################################################################################

def classi_bow(X_lem_train,y_lem_train,X_stem_train,y_stem_train,X_clean_train,y_clean_train):

    # Make vectorizer objects for bags of words (clean_df)
    cv_clean = CountVectorizer()
    tfidf_clean = TfidfVectorizer()

    #Bags of words
    cv_clean_bow = cv_clean.fit_transform(X_clean_train[['clean']].clean)
    tf_clean_bow = tfidf_clean.fit_transform(X_clean_train[['clean']].clean)
    
    # Make and fit decision tree object for cv_clean_bow
    cv_tree1 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    cv_tree1.fit(cv_clean_bow, y_clean_train)

    #Make and fit decision tree object for tf_clean_bow
    tf_tree1 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    tf_tree1.fit(tf_clean_bow, y_clean_train)


    # "Stemmed" models
    cv_stem = CountVectorizer()
    tfidf_stem = TfidfVectorizer()

    # Bags
    cv_stem_bow = cv_stem.fit_transform(X_stem_train[['stemmed']].stemmed)
    tf_stem_bow = tfidf_stem.fit_transform(X_stem_train[['stemmed']].stemmed)

    # Make and fit decision tree object for cv_stem_bow
    cv_tree2 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    cv_tree2.fit(cv_stem_bow, y_stem_train)

    # Make and fit decision tree object for tf_stem_bow
    tf_tree2 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    tf_tree2.fit(tf_stem_bow, y_stem_train)


    # "Lemmatized" models
    cv_lem = CountVectorizer()
    tfidf_lem = TfidfVectorizer()

    # Bags
    cv_lem_bow = cv_lem.fit_transform(X_lem_train[['lemmatized']].lemmatized)
    tf_lem_bow = tfidf_lem.fit_transform(X_lem_train[['lemmatized']].lemmatized)

    # Make and fit decision tree object for cv_lem_bow
    cv_tree3 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    cv_tree3.fit(cv_lem_bow, y_lem_train)

    #Make and fit decision tree object for tf_lem_bow
    tf_tree3 = DecisionTreeClassifier(max_depth=5, random_state = 302)
    tf_tree3.fit(tf_lem_bow, y_lem_train)


    dec_tree_training_scores=pd.Series({
        'CV_clean': cv_tree1.score(cv_clean_bow, y_clean_train),
        'CV_stem': cv_tree2.score(cv_stem_bow, y_stem_train),
        'CV_lem': cv_tree3.score(cv_lem_bow, y_lem_train),
        'TFIDF_clean': tf_tree1.score(tf_clean_bow, y_clean_train),
        'TFIDF_stem': tf_tree2.score(tf_stem_bow, y_stem_train),
        'TFIDF_lem': tf_tree3.score(tf_lem_bow, y_lem_train)
    })

    models = {
        'CV_clean' : {
            'vectorizer' : cv_clean,
            'model' : cv_tree1
        },
        'CV_stem' : {
            'vectorizer' : cv_stem,
            'model' : cv_tree2
        },
        'CV_lem' : {
            'vectorizer' : cv_lem,
            'model' : cv_tree3
        },
        'TFIDF_clean' : {
            'vectorizer' : tfidf_clean,
            'model' : tf_tree1
        },
        'TFIDF_stem' : {
            'vectorizer' : tfidf_stem,
            'model' : tf_tree2
        },
        'TFIDF_lem' : {
            'vectorizer' : tfidf_lem,
            'model' : tf_tree3
        }
    }

    return dec_tree_training_scores, models

################################################################################

def establish_classification_baseline(target: pd.DataFrame) -> pd.Series:
    '''
        Returns a pandas series containing the most common value in the target 
        variable that is of the same size as the provided target. This series 
        serves as the baseline model to which to compare any machine learning 
        models.

        Parameters
        ----------
        target: DataFrame
            A pandas series containing the target variable for a machine 
            learning project.

        Returns
        -------
        Series: A pandas series with the same size as target filled with the 
            most common value in target.
    '''

    most_common_value = target.mode()[0]
    return pd.Series(most_common_value, index = target.index)

################################################################################

def append_results(index: str, results: dict, evaluate_df: pd.DataFrame = None) -> pd.DataFrame:
    '''
        Append the evaluation results to the evaluate_df or if an evaluate_df 
        is not provided, create one and append the results.
    
        Parameters
        ----------
        index: str
            The index to assign to the results entry provided. A string provides 
            a more descriptive index, but any valid dataframe index is acceptable.
        results: dict[str : float]
            The results of the model evaluation in the form of a dictionary with 
            the metric as the key and the result as a float.
        evaluate_df: DataFrame, optional
            The evaluation dataframe to append the results to. Default is to 
            create a new dataframe.
    
        Returns
        -------
        DataFrame: The evaluate_df with the results appended.
    '''

    if evaluate_df is None:
        evaluate_df = pd.DataFrame()

    df = pd.DataFrame(results, index = [index])
    
    return evaluate_df.append(df)