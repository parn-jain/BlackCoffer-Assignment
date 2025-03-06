Tools and technologies 
Backend and API : Django and DRF
Database : sqlite3
fron-end: bootstrap
charts: Plotly

Data Preprocessing 
There we too many empty data , making it defficult to make any meaningfull conclusion and inference
Handelling missing data from start year : 690/1000 were empty in start_year
I make the Published year as the start year if start_year was missing
as a result 60/1000 remains empty and meaningfull and logical patterns in the graphs started to show

End year :
there were 742/1000 empty data for end_year 
I left the end year untched adn done all the analysis based on start year 
filling end_year witht the current year was not correct as it was the prediction for the future and incorrect predicted
info could be impactfull hence better to leave empty then filign any incorrect value


missing values in relevance, likelihood were very less and replaced by mode value

missign vaule in topics and sectors were not in the range to replaced by loss, either we could diatributed them 
equally or can be classified as unknows 
i calssified them as unknown

You can see all the preprocessign and data ananlysis steps in Preprocessing-and-analysis.ipynb file


Main project
Created Data Model and imported JSON to sqlite3 Database
then further created views funcitons, filters queries and other logics
there are 2 apss:
dashboard
and 
API

in api app REST api is created (BASIC)
in dashboard there are frontend , templates and sqlite3 model (Data)

