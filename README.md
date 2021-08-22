# ADR-Taskphase
This is a code for a basic regression implementation where i try to find the best model to predict the
GDP of a country based on the dataset containing GDP of countries from 1960s.

The dataset was found on kaggle.com (The dataset is uploaded as well in the ML_Project branch)

The working of code:
The code first starts with importing all the required libraries, mostly from sklearn, and also matplotlib to plot the graphs for EDA.

Then we use the melt function from pandas to convert the wide dataset, into a long dataset by pivoting those values to the rows.
At the end of this operation we will hve a dataset that is longer and with fewer columns/features.
We then convert the data in the 'Year' column to integer typ and then drop all null values from the dataset.

We then remove the unwanted variables like 'Country Code', 'Indicator Name' and 'Indicator code'

We also go through the dataset, and find unwanted countries, (those that are grouped in the dataset for a better understanding while interpretting the GDP
contribution of areas like 'South America' or 'UAE' which are not countries but are reffered to as a whole set) and proceed to remove those from the dataset.

We then save the GDP values of the clean data and save it in a new file.

Next we take the countiry that we want to predict the GDP for, and allocate the x and y variables accordingly.

We then use the train_test_split function to get a split of training and testing data

The next part of the code is to apply the regression methods with different methods and calculate the R2 score .

The results of each regression method are commented and documented in the code. The best R2 score was given by 
polynomial regression, with a score of 0.997752.
