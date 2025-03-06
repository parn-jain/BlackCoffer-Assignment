# Project Overview  

## Tools and Technologies  
- **Backend & API:** Django and DRF  
- **Database:** SQLite3  
- **Frontend:** Bootstrap  
- **Charts:** Plotly  

## Data Preprocessing  
The dataset contained a significant amount of missing data, making it difficult to draw meaningful conclusions and insights.  

### Handling Missing Data  

#### Start Year:  
- **690 out of 1000** entries were missing in the `start_year` column.  
- To address this, I used the `published_year` as the `start_year` whenever it was missing.  
- After this step, only **60 out of 1000** entries remained empty, which allowed logical patterns to emerge in the graphs.  

#### End Year:  
- **742 out of 1000** entries were missing in the `end_year` column.  
- I left `end_year` untouched and based all analyses on `start_year`.  
- Filling `end_year` with the current year would have introduced incorrect predictions, which could negatively impact insights. Therefore, it was better to leave it empty rather than insert potentially misleading values.  

#### Other Missing Values:  
- Missing values in `relevance` and `likelihood` were minimal and were replaced with the mode value.  
- Missing values in `topics` and `sectors` were not large enough to cause major data loss. These could either be distributed equally or classified as "Unknown."  
- I opted to classify them as **"Unknown"** for consistency.  

**You can find all preprocessing and data analysis steps in the** `Preprocessing-and-analysis.ipynb` **file.**  

## Main Project  

- Created a **data model** and imported JSON data into an **SQLite3 database**.  
- Developed **views, functions, filters, queries, and other logic** for data processing.  
- The project consists of two apps:  

### 1. **Dashboard App**  
   - Contains the **frontend, templates, and SQLite3 models (data storage).**  
   - Visualizations and insights are presented using Bootstrap and Plotly.  

### 2. **API App**  
   - Implements a **basic REST API** using Django REST Framework (DRF).  
