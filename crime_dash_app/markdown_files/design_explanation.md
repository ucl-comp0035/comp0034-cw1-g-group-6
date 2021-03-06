# Visualisations Design Explanations

In this project, we set out to create an insightful and well-functioning Dash App for our dataset. To achieve this, we made three different visualisations to answer our target audience questions.
In coursework 1 of COMP0035, we detailed these questions relating to the Metropolitan Police dataset and have been listed below:

    1. How has drug crime evolved in London over the two recorded years?
    2. Which type of crime is the highest and lowest in London?
    3. How does sexual offence fluctuate over the four seasons?
    4. Which borough has the highest crime rates in London?

To answer these questions, we narrowed the scope of our data exploration to three categories visualisations. These were:

    1. A chloropleth map
    2. A histogram
    3. A line chart

We also found that the standard method of reporting Crime Statistics is with a "Crime Rate per 1000 population" [(UKCrimeStats, 2014)](https://ukcrimestats.com/blog/faqs/what-exactly-does-crime-rate-mean-and-how-do-you-calculate-it/)
which requires both the number of committed crimes and the area population. However, the given data only provides us with the total number of reported crimes for respective Boroughs, Crime Types, and Months.

So, to provide the target audience relevant statistics they can compare with statistics from other articles or websites, we decided to use two additional datasets:

#### Daytime Population by Borough
* The dataset provides us with a Total Daytime Population which includes tourism and Workday Population which excludes them for year 2014. This is 
particularly useful to understand the crime rates of Boroughs that have a high Daytime population but relatively low residential population, 
as it adjusts the reported crimes.
* The dataset does not contain any personal information on persons but rather general statistics on ares in London
* The dataset is licensed under [UK Open Government License](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/), which allows for free 
  * Copying, publishing, distributing, and transmitting the Information
  * Adapting the Information
  * Exploiting the Information commercially and non-commercially
* The dataset is available on [London Datastore](https://data.london.gov.uk/dataset/daytime-population-borough)


#### Population Density by Borough
* The dataset provides us with GLA estimates for residential population throughout Boroughs and residential population statistics from 2011 Census Data. 
This can be useful to calculate the traditional crime rate statistics per 1000 residents.
* The dataset does not contain any personal information on persons but rather general statistics on areas in London
* The dataset is licensed under [UK Open Government License](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/), which allows for free 
  * Copying, publishing, distributing, and transmitting the Information
  * Adapting the Information
  * Exploiting the Information commercially and non-commercially
* The dataset is available on [London Datastore](https://data.london.gov.uk/dataset/land-area-and-population-density-ward-and-borough)


With the population data included, webapp users will be able to select whichever statistics that are most useful to them:
* Raw Reported Numbers of Crimes
* Crime Rate per 1000 residents, adjusted with 2020 GLA resident population estimate
* Crime Rate per 1000 residents, adjusted with 2011 Census resident population statistics
* Crime Rate per 1000 daytime population, adjusted with Total Daytime Population including tourists
* Crime Rate per 1000 daytime population, adjusted only with Working Daytime Population excluding tourists (which might be most appropriate for the COVID-19 period)

Each of the mentioned visualizations will change based on selected data and is able to answer one or multiple of the aforementioned target audience questions.
To explain the design of our visualizations clearly, we will first obtain a solid understanding of our target audience and their needs.

### 1. Target Audience

![Persona](../assets/persona.png)

Our target audience for the webapp, are university students who are new to London and looking for accommodation. 
They are generally not familiar with population densities, economic conditions, and variations in population composition of the London Boroughs, 
as those are recognized as some factors that impact the crime rates by the FBI, so they can struggle to make informed judgements on the safety of the Boroughs. 
Therefore, they rely on websites and articles reporting crime rates and quantifying borough safety.

The webapp would be useful to the target audience as it would allow them to explore the claims made by various other sources
and compare those claims with statistics. 

Moreover, based on personal preferences, they would be able to tailor their searches to the crimes they are the most concerned about for Boroughs they're interested in,
understand how those crime rates change over seasons/years, and see the crime rate forecasts for the next 6 months.

### 2. Software Engineering Process - CRISP DM

In our application development process we adhered to the 6 CRISP-DM Phases outlined by the 
[Data Science Process Alliance](https://www.datascience-pm.com/crisp-dm-2/) and used an agile approach, iterating on multiple phases without necessarily locking on a previous one.

#### Business Understanding
* **Determine business objective:**
Part of this was already done by the teammate whose dataset we selected in Coursework 1 and Coursework 2 for COMP0035. Together we refined the goals and requirements of the target group and how could we achieve them.


* **Assess situation:**
When assessing the situation we paid attention both to the requirements of our target customers and the coursework grading criteria, to determine which solutions would lead to the best results.


* **Determine data mining goals:**
We iterated that one of the main requirements our target audience had is being able to access standard Crime Rate per 1000 population statistical metric, so we found appropriate datasets to include in our app in order to satisfy that condition.


* **Produce Project plan:**
Initially many of our resources were spent on the business understanding. We needed to make sure that all parties of the group knew the objective of this task (this involved removing biases, creating objectives, and reviewing modalities of the data).
After agreeing on the business understanding, we developed a mix of visual and numerical solutions that would display the data in way most understandable to the target customer.

#### Data Understanding
* **Collect initial data:**
We used 3 categories of data: 
  * Crime data (which was already provided) 
  * London geojson data, used to create the choropleth visualization
  * Population data, which we had to research and find out, and was used together with Crime Data to create standard Crime Rate per 1000 population statistics metrics


* **Describe data:**
  * Crime Data has 26 columns (First one representing Boroughs, Second one representing Crime Types, and all the other representing different Months) and 298 rows
  * London geojson data is a dictionary with coordinates for each London borough
  * Population data:
    * Daytime Population data had 3 columns (Borough, Total Daytime Population, Workday Population) and 34 rows, representing the number of people that is in a borough throughout the day
    * Resident Population data had 3 columns (Borough, Population 2020 GLA Estimate, Population 2011 Census) and 34 rows, representing the number of residents in each Borough


* **Explore data:**
As our app is based on exploration of the dataset, the three visualizations we designed are meant to help our target audience to understand the data.


* **Verify data quality:**
None of our datasets had any missing values and was generally clean, except Crime Data, where the months were written as a string and not in a datetime format. 

#### Data preparation

* **Select data**
As mentioned above we're using 3 types of datasets: Crime Data, London geojson, and Population data.


* **Clean data**
Our data was already cleaned, so the only thing we had to do is, after reformatting it, change the dates from a string into a datetime format.


* **Construct data**
We added calculated metrics such as Total Crime Rate and Average Crime Rate to our datasets.


* **Integrate data**
We integrated the Crime Data and Population Data into 4 new datasets based on different ways of reporting Crime Rate statistics per 1000 people:
  * Crime Rate per 1000 residents based on 2020 GLA Population Estimate 
  * Crime Rate per 1000 residents based on 2011 Census Population statistics
  * Crime Rate per 1000 daytime population based on Total Daytime Population, including tourists
  * Crime Rate per 1000 workday population based on Total Workday Population, excluding tourists


* **Format data**
To get the datasets into the correct format for choropleth and line visualizations we had to pivot the dataset, so instead of the columns representing the dates and the rows the crime types, dates were aggregated into a Date column and the columns now represent the crime types. 
We also did some filtering and smaller reformatting when necessary. 

#### Modelling
* Because our solution is mainly based around creating interactive visualizations so the app user can explore the data in an intuitive manner, the project didn't focus on
developing any models or algorithms. 

* However, we did use Facebook's Prophet time series predicting model in order to forecast the crime rate for the next 6 months. But the model is already trained
by Facebook, so we only fitted the data.

* In our case, developing unique forecasting algorithms would most likely not yield great results as we only had about 2 years worth of monthly data as data-points which is far too few to properly train a predictive algorithm.


#### Evolution 
* Looking at the final delivery from a business perspective, we believe the app and app visualizations answer all the target customers' requirements.
However, to see if that really is the case the app should be presented to stakeholders and target customers to get their feedback on it, and then further
iterate and improve the app based on their feedback


* At this stage we conducted two types of tests. We tested the dash app features to verify that the interface was working as planned with 11 distinct tests which was done using selenium. We also created Unit tests to check for a specific response to a set of inputs. After, we integrated this with GitHub Actions to create a workflow to run the tests. These tests verified a good functionality of the dash app. Information on the specific tests conducted can be found in part 6. 

#### Deployment

- The dash app is ready to use and should aid prospective home-renters in London to find a safe area if they are concerned about crime levels.
However, any further discussion of the app's deployment is beyond the scope of this project.


### 3. Visualisation 1: The Map

[Visualisation 1: Link to design explanation and evaluation](visualisation_1.md)

### 4. Visualisation 2: The Histogram

[Visualisation 2: Link to design explanation and evaluation](visualisation_2.md)

### 5. Visualisation 3: The Line Chart

[Visualisation 3: Link to design explanation and evaluation](visualisation_3.md)

### 6. Testing the Dash App

To test the dash app, we came up with 11 separate tests using selenium.
The tests check if the interactivity of Display Settings panel (left) updates the graphs correctly.
They check if the map visual and its statistics are updated correctly when selecting a particular data, crime, time frame and/or boroughs.
They also check to see if the line visual and its statistics are updated correctly when selecting crime, borough and/or data.

The histogram part of the app is the only one not tested for, as the elements of the histogram graph don't help distinguish between
when different boroughs and time ranges are selected. This could be improved by implementing different elements in the app that report 
the changes to the histogram, however, due to time constraints we decided not to perform app tests for the histogram.


We also created 8 unit tests to test all functions of all() class in visualizations.py file.

It tests if the data imports and data reformatting work by checking the data shapes,
if returned crime, borough and/or date lists are correct. It also tests for if the get_highlights returns the correct subsection of the
geojson given a particular borough, and if test_map_statistics returns the correct specific values.

What is not tested are the functions that return various plotly visualizations.

### 7. Link to Video

[Link to Video](https://youtu.be/ufafiY_zjP0)


### 8. Weekly Progress reports

We decided to have a Google doc as a way of reporting what we discussed in the meetings, what we have done, and what we need to do next.
Google doc instead of moodle was used so all teammates have access to the TODO list and can write what they have done / plan to do.
On top of that we had about two meetings per week to catch up and update the TODO list, and we had a WhatsApp group that was used to communicate and helps each other in case we faced issues that could be solved by another team member.

The contents of that doc are available bellow:
#### Week 1
![Week 1](../assets/Week%201.png)

#### Week 2
![Week 2](../assets/Week%202.png)

#### Week 3
![Week 3](../assets/Week%203.png)

#### Week 4
![Week 4](../assets/Week%204.png)

#### Week 5
![Week 5](../assets/Week%205.png)

#### Week 6
![Week 6](../assets/Week%206.png)









