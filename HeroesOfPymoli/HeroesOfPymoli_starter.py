#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[4]:


# Dependencies and Setup
import pandas as pd

# File to Load
purchase_path = "Resources/game_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_df = pd.read_csv(purchase_path)
purchase_df.head()


# ## Player Count

# * Display the total number of players
# 

# In[5]:


#find number of unique SNs to find actual player count
player_count = len(purchase_df["SN"].unique())
player_count_df = pd.DataFrame({"Total Players" : [player_count]})
player_count_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[6]:


#etablish variables to be used for summary_df
uni_items = len(purchase_df["Item ID"].unique())
avg_price = round(purchase_df["Price"].mean(), 2)
num_purchases = len(purchase_df)
total_revenue = sum(purchase_df["Price"])

#create a data frame with named columns
summary_df = pd.DataFrame({"Number of Unique Items" : [uni_items], "Average Price" : [avg_price],
                         "Number of Purchases" : [num_purchases], "Total Revenue" : [total_revenue]})

#format data frame
summary_df["Average Price"] = summary_df["Average Price"].map("${:.2f}".format)
summary_df["Total Revenue"] = summary_df["Total Revenue"].map("${:,.2f}".format)

summary_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[7]:


# establish variables to be used in calculations regarding male, female, and other (I now inderstand this may have been the long way...)
male_df = purchase_df.loc[purchase_df["Gender"] == "Male", :]
male_count = len(male_df["SN"].unique())
male_percentage = round((male_count / player_count) * 100, 2)
male_purchase = round(male_df["Gender"].value_counts())
male_avg_price = round(male_df["Price"].mean(), 2)
male_total = round(male_df["Price"].sum(), 2)
male_avg_person = round((male_total / male_count), 2)

female_df = purchase_df.loc[purchase_df["Gender"] == "Female", :]
female_count = len(female_df["SN"].unique())
female_percentage = round((female_count / player_count) * 100, 2)
female_purchase = female_df["Gender"].value_counts()
female_avg_price = round(female_df["Price"].mean(), 2)
female_total = round(female_df["Price"].sum(), 2)
female_avg_person = round((female_total / female_count), 2)

other_df = purchase_df.loc[purchase_df["Gender"] == "Other / Non-Disclosed", :]
other_count = len(other_df["SN"].unique())
other_percentage = round((other_count / player_count) * 100, 2)
other_purchase = other_df["Gender"].value_counts()
other_avg_price = round(other_df["Price"].mean(), 2)
other_total = round(other_df["Price"].sum(), 2)
other_avg_person = round((other_total / other_count), 2)


# In[8]:


#can do a group by ["Gender"], then create a new Data frame with the columns using the count & % variables, and then set index 
grouped_df = purchase_df.groupby(["Gender"])

#create a data frame with named columns
gender_summary_df = pd.DataFrame({"Total Count" : [male_count, female_count, other_count],
                                "Percentage of Players" : [male_percentage ,female_percentage,other_percentage]
                                                          },index = ["Male", "Female", "Other / Non-Discolsed"])
#format data frame
gender_summary_df["Percentage of Players"] = gender_summary_df["Percentage of Players"].astype(str).add("%")

gender_summary_df


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[10]:


#create new groupby
new_grouped_df = purchase_df.groupby(["Gender"])

#turn group by into a new data frame with named columns
gender_summary_df = pd.DataFrame({"Purchase Count" : [female_purchase, male_purchase, other_purchase],
                                "Average Purchase Price" : [female_avg_price,male_avg_price,other_avg_price],
                                 "Total Purchase Value" : [female_total,male_total,other_total],
                                 "Avg Total Purchase per Person" : [female_avg_person,male_avg_person,other_avg_person]
                                  }, index = ["Female", "Male", "Other / Non-Discolsed"])

gender_summary_df.index.name = "Gender"

#format data frame
gender_summary_df["Purchase Count"] = gender_summary_df["Purchase Count"].astype(int)
gender_summary_df["Average Purchase Price"] = gender_summary_df["Average Purchase Price"].map("${:.2f}".format)
gender_summary_df["Total Purchase Value"] = gender_summary_df["Total Purchase Value"].map("${:,.2f}".format)
gender_summary_df["Avg Total Purchase per Person"] = gender_summary_df["Avg Total Purchase per Person"].map("${:.2f}".format)

gender_summary_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[11]:


#copying dataframe to new datframe for easier and filtered calculations
player_demographics = purchase_df.loc[: ,["Gender", "SN", "Age"]]
player_demographics = player_demographics.drop_duplicates()
player_demographics = player_demographics.reset_index(drop=True)


# In[12]:


#set up bins and labels
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 49.9]
age_labels = ["<10", "10-14", "15-19","20-24", "25-29", "30-34", "35-39", "40+"]
pd.cut(player_demographics["Age"], bins, labels=age_labels).head()
player_demographics["Age Group"] = pd.cut(player_demographics["Age"], bins, labels=age_labels)

#create new groupby
age_group = player_demographics.groupby(["Age Group"])
player_count = player_demographics["SN"].count()
age_count = age_group["SN"].count()

#turn group by into a new data frame with named columns
age_demo_df = pd.DataFrame({"Total Count" : age_group["SN"].count()})
age_demo_df["Percentage of Players"] = round((age_count/player_count) * 100, 2)

#format data frame
age_demo_df["Percentage of Players"] = age_demo_df["Percentage of Players"].astype(str).add("%")

age_demo_df


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[13]:


player_demographics2 = purchase_df.loc[: ,["Purchase ID", "SN", "Age", "Price"]]
player_demographics2 = player_demographics2.reset_index(drop=True)
# player_demographics2


# In[21]:


#establish bins to be used for grouped by Age DF
bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 49.9]
age_labels = ["<10", "10-14", "15-19","20-24", "25-29", "30-34", "35-39", "40+"]
pd.cut(player_demographics2["Age"], bins, labels=age_labels).head()
player_demographics2["Age Ranges"] = pd.cut(player_demographics2["Age"], bins, labels=age_labels)

#create new groupby
age_ranges = player_demographics2.groupby(["Age Ranges"])

#turn group by into a new data frame with named columns
age_ranges_df = pd.DataFrame({"Total Count" : age_ranges["SN"].count()})
age_ranges_df["Average Purchase Price"] = age_ranges["Price"].mean()
age_ranges_df["Total Purchase Value"] = age_ranges["Price"].sum()
age_ranges_df["Avg Total Purchase per Person"] = age_ranges_df["Total Purchase Value"] / age_demo_df["Total Count"]

#format data frame
age_ranges_df["Average Purchase Price"] = age_ranges_df["Average Purchase Price"].map("${:.2f}".format)
age_ranges_df["Total Purchase Value"] = age_ranges_df["Total Purchase Value"].map("${:,.2f}".format)
age_ranges_df["Avg Total Purchase per Person"] = age_ranges_df["Avg Total Purchase per Person"].map("${:,.2f}".format)

age_ranges_df


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[22]:


#create new groupby
sn_group = purchase_df.groupby(["SN"])

#turn group by into a new data frame with named columns
sn_df = pd.DataFrame({"Purchase Count" : sn_group["SN"].count()})
sn_df["Average Purchase Price"] = sn_group["Price"].mean()
sn_df["Total Purchase Value"] = sn_group["Price"].sum()

#sort datafram...BEFORE FORMATTING!
sn_df = sn_df.sort_values("Total Purchase Value", ascending = False)

#format sorted data frame
sn_df["Average Purchase Price"] = sn_df["Average Purchase Price"].map("${:.2f}".format)
sn_df["Total Purchase Value"] = sn_df["Total Purchase Value"].map("${:.2f}".format)

sn_df.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[37]:


#new df "Item" and "Price"
most_pop_df = purchase_df.loc[: ,["Item ID", "Item Name", "Price"]]

#create new groupby
pop_group = most_pop_df.groupby(["Item ID" , "Item Name"])

#turn group by into a new data frame with named columns
pop_df = pd.DataFrame({"Purchase Count" : pop_group["Item ID"].count()})
pop_df["Item Price"] = pop_group["Price"].mean()
pop_df["Total Purchase Value"] = pop_group["Price"].sum()

#sort datafram...BEFORE FORMATTING!
pop_df = pop_df.sort_values("Purchase Count", ascending = False)

#format sorted data frame
pop_df["Item Price"] = pop_df["Item Price"].map("${:.2f}".format)
pop_df["Total Purchase Value"] = pop_df["Total Purchase Value"].map("${:.2f}".format)

pop_df.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[47]:


#new df "Item" and "Price"
most_prof_df = purchase_df.loc[: ,["Item ID", "Item Name", "Price"]]

#create new groupby
prof_group = most_prof_df.groupby(["Item ID" , "Item Name"])

#turn group by into a new data frame with named columns
prof_df = pd.DataFrame({"Purchase Count" : pop_group["Item ID"].count()})
prof_df["Item Price"] = pop_group["Price"].mean()
prof_df["Total Purchase Value"] = pop_group["Price"].sum()

#sort datafram...BEFORE FORMATTING!
prof_df = prof_df.sort_values("Total Purchase Value", ascending = False)

#format sorted data frame
prof_df["Item Price"] = prof_df["Item Price"].map("${:.2f}".format)
prof_df["Total Purchase Value"] = prof_df["Total Purchase Value"].map("${:.2f}".format)

prof_df.head()


# ### Observable Trends
# * Males purchase a much higher percentage of games
# * People age 20-24 purchase and play the most games 
# * Females tend to purchase more more expensive games as whole and individually
