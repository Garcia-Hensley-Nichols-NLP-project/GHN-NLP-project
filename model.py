from os import terminal_size
import pandas as pd
from prepare import basic_stem, tokenize, stem, lemmatize, remove_stopwords, prep_article_data, words
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split

# Import Decision Tree and Random Forest 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier



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



def get_dt_valtest_score(bow, text_data, target, model):
    '''
    Takes in a previously fit_transformed vectorizer(bag of words[bow]), text data that is NOT from the train split, a matching target, and a previously 
    fitted model,
    and returns an accuracy score for the model against the unseen text data.
    '''

    # Transform bow on text_data
    bow = bow.transform(text_data)
    # Evaluate model accuracy
    model_score = model.score(bow, target)

    return model_score



