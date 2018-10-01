# The intended use for this script is to review a CSV file containing First Name, Last Name, and Email addresses,
# with a goal of eliminating as many duplicate records as possible without human intervention.

# Limitations: (1) The original data source this was designed around contains event registration records from multiple
# years of the same event that has many repeat attendees. As such, some attendees may have used different email
# addresses at different times, and the one selected by the script may not be the best one. (2) If registrants
# provided different first name values that don't share a starting letter (eg. Alexander vs Xander), duplicates will
# still get through.

import pandas
import numpy

# Read in the source file, and index by email address
df = pandas.read_csv('registrants.csv')

# Set appropriate case for each column
df['First Name'] = df['First Name'].str.title()
df['Last Name'] = df['Last Name'].str.title()
df['Email'] = df['Email'].str.lower()

# Create new column of last name + First Name, to make it easier to perform manual duplicate checks
df['Full Name'] = df['Last Name'] + ' ' + df["First Name"]

# If duplicate emails or full names are found, keep the first occurence and drop the rest
df = df.drop_duplicates(['Email'], keep='first')
df = df.drop_duplicates(['Full Name'], keep='first')

# If the Last Name, and the first letter of the First Name are duplicate, flag for a manual check
df['First Initial'] = df['First Name'].str[0]
df['LN FI']= df['Last Name'] + ' ' + df['First Initial']
df['Possible']= df.duplicated(['LN FI'], keep=False)

# Output results
df.to_csv(r"results.csv")

# Original list: 1429
# Result: 667
# Result after manual analysis: 663

# References (in no particular order)
# https://realpython.com/python-csv/#parsing-csv-files-with-the-pandas-library
# https://medium.com/@kasiarachuta/dealing-with-duplicates-in-pandas-dataframe-789894a28911
# https://stackoverflow.com/questions/45497835/how-to-drop-duplicates-based-on-two-or-more-subsets-criteria-in-pandas-data-fram
# https://stackoverflow.com/questions/35552874/get-first-letter-of-a-string-from-column
# https://stackoverflow.com/questions/38319249/splitting-duplicates-into-separate-table-pandas
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.capitalize.html
# http://pandas.pydata.org/pandas-docs/version/0.17.1/generated/pandas.DataFrame.drop_duplicates.html
# https://github.com/arditsulceteaching/thepythonmegacourse
