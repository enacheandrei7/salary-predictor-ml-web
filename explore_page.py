"""
Explore page for viewing the data
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    """
    Selects the countries with more than a certain number of entries in order to not confuse the model with too litle values for certain zones.
    Args:
        categories: DataFrame with the countries and number of entries
        cutoff: The minimum number of entries for each country
    Returns:
        categorical_map: DataFrame
    """
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    """
    Transforms the string experience types of more than 50 years and less than 1 year in numerical values.
    """
    if x == 'More than 50 years':
        return 51
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    """
    Changes the educattion types in 4 distinct categories
    """
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache
def load_data():
    """
    Loads the data from the csv and preprocess it. The data is cached for shorter execution time.
    Returns:
        df: DataFrame
    """
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df ['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write(""" ### Stack Overflow Developer Survey 2020""")
    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal") # Equal aspect ratio ensures that the pie is drawn as a circle

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)

    st.write("""### Mean Salary based On Country""")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)


    st.write("""### Mean Salary based On Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)