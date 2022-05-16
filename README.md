# NLP Project

This repository contains all files, and ipython notebooks, used in the NLP Project. A full outline of all the files with descriptions can be found below.

___

## Table of Contents

- [NLP Project](#nlp-project)
  - [Table of Contents](#table-of-contents)
  - [Project Summary](#project-summary)
  - [Project Planning](#project-planning)
    - [Project Goals](#project-goals)
    - [Project Description](#project-description)
    - [Initial Questions](#initial-questions)
  - [Data Dictionary](#data-dictionary)
  - [Outline of Project Plan](#outline-of-project-plan)
    - [Data Acquisition](#data-acquisition)
    - [Data Preparation](#data-preparation)
    - [Exploratory Analysis](#exploratory-analysis)
    - [Modeling](#modeling)
  - [Conclusion](#conclusion)
  - [Instructions For Recreating This Project](#instructions-for-recreating-this-project)

___

## Project Summary

Data from the `README.md` files of 100 GitHub repositories (repo's) are analyzed in order to attempt prediction of their primary programming language.

___

## Project Planning

<details><summary><i>Click to expand</i></summary>

### Project Goals

Determine the primary programming language of a GitHub repository by using natural language processing (NLP) techniques on their `README.md`.

### Project Description

GitHub is where over 83 million developers shape the future of software, together. This software is hosted on the site in "repositories". Aside from from acting as a home for open source coding, GitHub offers several interesting features in the repo's. One particular feature, that we will be investigating in this project, is the programming language percentage.

The programming language percentage is an infographic on the home page of every repo on GitHub. It indicates the percentage of each programming language in that particular repo. For most repo's there is a clear primary programming language (many have only 1 language).

Another common attribute of GitHub repo's is the `README.md`. The `README.md` is a file that generally contains an introduction to the repo, explains the purpose of the code, and shares instructions for running the code.

In this project, we will attempt to use data from the `README.md` to predict what language that repo is primarilly coded in. We are specifically interested in repo's related to the search term "bitcoin". We use the top 500 results for the search term "bitcoin" to obtain the data used for this project.

### Initial Questions

1. Can we predict the programming language of a repo by using NLP on the `README.md`?
2. Is there a statistically significant difference between `README.md` lengths for the top 3 most common languages?
3. Can the presence of certain keywords be used to identify the main programming language for a repository?
4. Are there bi-grams that are unique to one of the top 3 most common programming languages?
5. Is there a statistically significant difference in sentiment analysis between `REAMDE.md` files for the top 3 most common languages?

</details>

___

## Data Dictionary

<details><summary><i>Click to expand</i></summary>


| Variable              | Meaning      |
| --------------------- | ------------ |
| repo | Path to repository on github.com |
| language | Primary programming language in repository |
| readme | Contains full contents of the repository's "README.md" |
| clean | Contains the normalized, and tokenized, contents of the repository's "README.md" with stopwords removed |
| stemmed | Contains the stemmed words from the clean "README.md" text |
| lemmatized | Contains the lemmatized words from the clean "README.md" text |
| contains_python_keywords | Whether or not a README contains keywords common to Python repositories |
| contains_cpp_keywords | Whether or not a README contains keywords common to C++ repositories |
| contains_js_keywords | Whether or not a README contains keywords common to JavaScript repositories |

</details>

___

## Outline of Project Plan

The following outlines the process taken through the Data Science Pipeline to complete this project.

Plan &#8594; Acquire &#8594; Prepare &#8594; Explore &#8594; Model &#8594; Deliver

---
### Data Acquisition

<details><summary><i>Click to expand</i></summary>

**Acquisition Files:**

- acquire_urls.ipynb: Contains instructions for pulling a list of repository URLs matching the search term "bitcoin". It should be noted that this script was executed on May 16, 2022 and may produce different results at a later date. For reproducibility, a cache file containing the specific URLs used for this project is provided with the repository.
- urls.csv: A cache file containing URLs for the repositories used for this project.
- acquire.py: A python script containing code that pulls the repo path, language, and readme from list of repo's in urls.csv.

**Steps Taken:**

- This search is done via GitHub's API and a list is extracted that contains the url path to 500 related repos.
- A list of URLs for repositories matching the search term "bitcoin" is collected using the Github API. In order to have ample data to work with N URLs are acquired.
- The list of URLs is used to acquire the `README.md` file and primary programming language for each repository using the Github API. This can be a time consuming process.
- The readme's from each repo are pulled through the API and compiled to return a .json file with the aforementioned keys and values.

</details>

### Data Preparation

<details><summary><i>Click to expand</i></summary>

**Preparation Files:**

- prepare.ipynb: Contains instructions for preparing the data and testing the prepare.py module.
- prepare.py: Contains functions used for preparing the readme's for exploration and modeling.
- preprocessing.py: Contains functions used for preprocessing data for exploration and modeling such as splitting data.

**Steps Taken:**

- Now begins the challenge of quantizing communications in the english lanuage. NLP attempts to do just that by utilizing cutting edge computational power. Common parsing techniques are used on the original corpus collected from GitHub.
- In this project, the contents of an individual `README.md` are treated as a document. Each document is changed to all lower case letters, has punctuation removed, is tokenized, and has stop-words removed as a function of basic cleaning. Below are all the steps in preparing the data:
  - lowering the case of all words
  - removing punctuation
  - tokenization
  - removing stop words
  - column name changed
  - languages other than top 3 consolidated to 'other'
- The top 3 programming languages are Python, C++, and JavaScript which are each given their own classification class.
- Further preprocessing includes stemming and lemmetization.
- Column names are changed for convenience and all languages other than the top 3 are consolidated into the category 'other'.
- The tidied strings are returned in a single Pandas dataframe.

</details>

### Exploratory Analysis

<details><summary><i>Click to expand</i></summary>

**Exploratory Analysis Files:**

- explore.ipynb: Contains all steps taken and decisions made in the exploration phase with key takeaways.
- explore.py: Contains functions used for producing visualizations and conducting statistical tests in the final report notebook.

**Steps Taken:**

- First the data is split into three datasets: train, validate, and test. The training dataset is explored in the explore notebook and used later for training machine learning models. The validate and test datasets are used as unseen data to determine how the machine learning models perform on unseen data.
- The overall word frequencies are explored for the clean, stemmed, and lemmatized text to determine if there is any difference in word frequencies for each prepared README data.
- The word frequencies for each target class (Python, C++, JavaScript, and Other) are explored to determine if there are common words unique to each programming language.
- Bi-gram and Tri-gram analysis is conducted to determine if there are unique bi-grams or tri-grams for any of the target classes.
- Word clouds are produced for presentation purposes.
- The length of the README files is compared for each target class to determine if READMEs on average vary in size for different primary programming languages.
- Sentiment analysis is conducted for all target classes to determine if there is any significant difference in sentiment for each programming lanugage.

</details>

### Modeling

<details><summary><i>Click to expand</i></summary>

**Modeling Files:**

- model.ipynb: Contains all steps taken and decisions made in the modeling phase with key takeaways.
- Nichols_work.ipynb: 
- model.py: 

**Steps Taken:**

The following modelling techniques are implemented:

- Term Frequency (TF)
- Inverse Document Frequency (IDF)
- TF-IDF w/ SKLearn
- Classification Machine Learning Model

</details>

___

## Conclusion

<details><summary><i>Click to expand</i></summary>



</details>

___

## Instructions For Recreating This Project

<details><summary><i>Click to expand</i></summary>

1. Clone this repository into your local machine using the following command:
git clone git@github.com:Garcia-Hensley-Nichols-NLP-project/GHN-NLP-project.git
2. You will need Natural Language Tool Kit (NLKT), Pandas, Numpy, Matplotlib, Seaborn, and SKLearn installed on your machine.
3. Please run `python acquire.py` in a terminal to acquire the `data.json` file.
4. Now you can start a Jupyter Notebook session and execute the code blocks in the `final_report.ipynb` notebook.

</details>

[Back to top]()
