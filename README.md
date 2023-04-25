# College Mobility Streamlit App 

## Overview 
This is a Streamlit Application based on College Mobility Data.
This app allows users to explore colleges in the United States.
It allows you to filter colleges by various criteria and visualize the results.
Specifically, it allows you to:
* ***Filter*** colleges based on the selected criteria (e.g. SAT scores, tuition, median income)
* ***Visualize*** the filtered colleges in interactive charts
* Provide ***detailed*** information on the specific college selected
* Display a ***table*** containing full information of the filtered colleges

## Overview of the College Mobility Data
* This data track the income of students and their parents focusing on ***1980-1982 birth cohorts***
* Parental income is obtained based on the income of the parents at the time of the student's admission to college.
* Child income is obtained based on the income of the student ~10 years after graduation.
* Mobility rate is the fraction of students who move from the bottom 20% of parental income to the top 20% (or 1%) of child income.
* When year is not specified, it usually refers to the cohort of early 2000s.
* Please visit [Opportunity Insights Web Page](https://opportunityinsights.org/paper/mobilityreportcards/) for more information

## How to Access the College Mobility App

### Visit the Online App

If you want to use this app without any modification, you can simply visit the
[College Mobility App](https://college-mobility.streamlit.app/) hosted by [streamlit.io](https://streamlit.io/)

### Clone and run the app locally

If you want to clone this repository and run on your computer (possibly with modifications), you can follow the instruction below.

```
## you need git installed on your computer
git clone https://github.com/brucedarkspoon/college_stream.git  

cd college_stream

## you need python3 installed on your computer
pip3 install pandas streamlit 

streamlit run app.py
```
