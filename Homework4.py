#Shruti Kumar Homework 4
"""
This purpose of this file is find establishments with the maximum number of
critical violations observed within a specified distance.
"""

import pandas as pd
import sys

def join_data(inspfile, estfile):
    """
    Reads an inspection file and an establishment file in order to merge
    the two dataframes.

    Args:
        inspfile: the food inspection dataset file.
        estfile: the establishment dataset file.

    Returns:
        df1 (df): the dataframe with two merged dataframes.
    """
    info = pd.read_csv(inspfile) #reads inspection file
    place = pd.read_csv(estfile) #reads establishment file
    df1 = pd.merge(info, place, on="Establishment_id") #merges dataframes
    return df1

def filter_inspections(df, maxdist):
    """
    Take a dataframe and returns rows in which Inspection_type is Comprehensive
    or Monitoring, Distance_to_McKeldin is less than maxdist and
    inspection_results is equal to Critical Violations observed.

    Args:
        df (df): a merged dataframe with all establishment and inspection info
        maxdist (float): the max distance in miles

    Returns:
        df2 (df): the filtered dataframe
    """
    df2 = df.loc[((df['Inspection_type'] == 'Comprehensive') |
                (df['Inspection_type'] == 'Monitoring')) &
                (df['Distance_to_McKeldin'] < float(maxdist)) &
                (df['Inspection_results'] == 'Critical Violations observed')]
                #filters inspections
    return df2

def count_violations(dataframe):
    """
    Finds the number of violations for each establishment ID.

    Args:
        dataframe (df): a merged, filtered dataframe

    Returns:
        ser (ser): a series with the Establishment_id as the index and number
        of violations as the corresponding value.
    """
    counts = dataframe.groupby('Establishment_id')['Inspection_results'].count()
    #counts the number of rows for each establishment id
    ser = pd.Series(counts) #creates a series for counts
    return ser

def most_violations(dataframe):
    """
    Finds the establishment IDs of establishments with the max critical
    violations.

    Args:
        dataframe (df): a merged, filtered dataframe

    Returns:
        max_ests (list): a list of all establishment IDs with the max number of
        critical violations.
    """
    counts = count_violations(dataframe) #calls count_violations
    max_counts = counts.max() #finds establishment id with max count violations
    max_ests = counts[lambda row: row == max_counts].index.tolist() #makes
    #a list containing all establishments that have the max number of
    #critical violations
    return max_ests

def main(inspfile, estfile, maxdist):
    """
    Creates a list of the establishments with the max number of critical
    violations.

    Args:
        inspfile: the inspection dataset file.
        estfile: the establishment dataset file.
        maxdist (float): the max distance in miles
    """
    dfmain = join_data(inspfile, estfile)
    filtermain = filter_inspections(dfmain, maxdist)
    mostviolmain = most_violations(filtermain)
    est = dfmain.loc[dfmain['Establishment_id'].isin(mostviolmain)]['Name']
    #finds the name of establishments from dfmain in mostviolmain
    unique_ests = est.unique().tolist() #for unique names in a list format
    for i in unique_ests:
        print(i) #prints a list of the establishment names with max critical
        #violations within the specified distance

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
