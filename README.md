# SpaceX Data Science Capstone

Brian Reid — IBM Applied Data Science Capstone

## Objective
Explore historical Falcon 9 launches and predict the first-stage landing label used by the course.

## Completed work
1. `01_data_collection_api.ipynb`: launch snapshot retrieval and filtering, with documented IBM data fallback after HTTP 522 from the detail API.
2. `02_web_scraping.ipynb`: BeautifulSoup extraction of 121 records from the June 9, 2021 Wikipedia revision.
3. `03_data_wrangling.ipynb`: launch/orbit/outcome counts and binary training labels.
4. `04_eda_visualization.ipynb`: six required EDA charts and one-hot encoding.
5. `05_eda_sql.ipynb`: ten SQLite queries with outputs.
6. `06_folium_launch_sites.ipynb`: site circles/labels, outcome clusters, and selected-point distances.
7. `07_machine_learning.ipynb`: logistic regression, SVM, decision tree, and KNN tuning and evaluation.
8. `spacex-dash-app.py`: interactive launch-site dropdown, outcome pie chart, payload slider, and scatter chart.

## Results and limits
- Wrangling: 90 launches, 60 Class 1 and 30 Class 0 records.
- All four models: 83.33% accuracy on the same 18-record test set.
- Decision tree: highest mean 10-fold cross-validation accuracy, 87.68%.
- Every test confusion matrix: [[3, 3], [0, 12]], with rows as actual Class 0/1 and columns as predicted Class 0/1.
- The course counts successful ocean landings as Class 1. This label does not establish booster recovery or reuse.
- The prediction lab loads the course's 83-feature file independently. The EDA notebook produces 80 encoded features. These are separate supplied lab inputs.
- The course workflow scales features before the train/test split. A production analysis should fit preprocessing inside training folds using a pipeline to avoid leakage.
- Final Folium map: selected shoreline point 0.838 km, selected road point 0.644 km from CCAFS SLC-40. Manual points are not certified nearest features. Earlier maps use a misleading example coastline point and are superseded by the final corrected map.
- API snapshot, SQL (101 records), maps/dashboard (56 records), and scraped table (121 records) use different historical coverage. Do not pool their success rates.

## Run the dashboard
```bash
pip install -r requirements.txt
python spacex-dash-app.py
```
Open port 8050. Keep `spacex_launch_dash.csv` beside the script.

## Data and attribution
IBM Skills Network provides lab templates and course datasets. Source notebook author credits are retained. Wikipedia revision 1027686922 provides the scraped launch tables. `dataset_part_1.csv` is reconstructed from the supplied part-2 file by removing Class. `dataset_part_3_eda.csv` is regenerated from the same 90-record course dataset and is not the prediction lab's independent 83-feature input.

## Notebook environments
The saved visualization, Folium, and prediction notebooks were executed in JupyterLite and retain browser-specific piplite/js imports. Run these in the course browser environment or adapt those setup/data-loading cells for desktop Jupyter. SQL, wrangling, API fallback, and scraping notebooks use standard Python.
