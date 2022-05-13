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



___

## Project Planning

<details><summary><i>Click to expand</i></summary>

### Project Goals



### Project Description



### Initial Questions



</details>

___

## Data Dictionary

<details><summary><i>Click to expand</i></summary>


| Variable              | Meaning      |
| --------------------- | ------------ |
| repo | Path to repository on github.com |
| language | Primary programming language in repository |
| readme_contents | Contains full contents of the repostitories "README.md" |

</details>

___

## Outline of Project Plan

The following outlines the process taken through the Data Science Pipeline to complete this project.
<br>
Plan &#8594; Acquire &#8594; Prepare &#8594; Explore &#8594; Model &#8594; Deliver

---
### Data Acquisition

<details><summary><i>Click to expand</i></summary>

**Acquisition Files:**
- test.ipynb, pulls list of repositories matching search term "binance:
- acquire.py, pulls repo path, language, and readme from list of repo's in test.ipynb

**Steps Taken:**
- The data is collected from several repositories on github.com via the sites API.
- A list of repo's is generated from search results for "bitcoin".
- The readme's from each repo are pulled through the API and compiled to return a .json file with the aforementioned keys and values.

</details>

### Data Preparation

<details><summary><i>Click to expand</i></summary>

**Preparation Files:**
prepare.ipynb, testing of prepare.py
prepare.py, prepares the readme's for exploration and modeling

**Steps Taken:**
All data is prepared for natural language processing by:

- lowering the case of all words
- removing punctuation
- tokenization
- removing stop words

Additional preparations include:

- stemming
- lemmatization

</details>

### Exploratory Analysis

<details><summary><i>Click to expand</i></summary>

**Exploratory Analysis Files:**
explore.ipynb,

**Steps Taken:**

- explore readme's by language
- analyze word frequency by language
- bi-gram analysis
- 

</details>

### Modeling

<details><summary><i>Click to expand</i></summary>

**Modeling Files:**

model.ipynb
model.py

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

Clone this repository into your local machine using the following command:
git clone git@github.com:Garcia-Hensley-Nichols-NLP-project/GHN-NLP-project.git
You will need Natural Language Tool Kit (NLKT), Pandas, Numpy, Matplotlib, Seaborn, and SKLearn installed on your machine.
Please run `python acquire.py` in a terminal to acquire the `data.json` file. Now you can start a Jupyter Notebook session and execute the code blocks in the `final_report.ipynb` notebook.

</details>

[Back to top]()
