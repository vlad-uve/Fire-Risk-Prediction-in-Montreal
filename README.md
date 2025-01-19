# Prediction of High Fire Risk Areas in Montréal

This repository contains the work for the **YCBS 299 - Data Science Capstone Project** course at McGill University conducted in 2024 by Team #6: Felix MARTINEZ MEJIAS, Sienko IKHABI, Vladislav YUSHKEVICH, Vadim STRELNIKOV. ~~The project focuses on using machine learning to predict high fire-risk areas in Montréal, enabling the fire department to optimize resource allocation, enhance response precision, and improve cost efficiency.~~

## Project Overview

The Montreal Fire Department faces rising fire incidents despite limited staffing and resources. This project aims to **predict monthly high fire-risk areas** using advanced analytics and machine learning, enabling improved resource allocation and preemptive strategies that enhance public safety and reduce operational costs.

Primary objective:
- **Enhance Response Precision**: Develop a machine learning model capable of accurately predict areas with high fire risk to enable swift strategic response.

~~Secondary objectives:~~
- **Optimize Resource Allocation**: Allocate personnel and equipment to high-risk areas effectively.
- **Improve Cost-Efficiency**: Prioritize inspections and reduce preventive measure costs.
- **Support Budget Planning**: Provide foresight into expenditures for fire incident management.

The data science project directly addresses the critical needs of the Montreal Fire Department, aligning with goals of efficiency, effectiveness, and fiscal responsibility. By enhancing the accuracy of fire incident predictions, the model optimizes resource deployment and bolsters the city's firefighting capabilities, ultimately contributing to the safety and well-being of its residents.
  
## Data Overview

The analysis leveraged diverse datasets spanning January 2005 to January 2024, including:
- **Fire Incidents** (Open Data - City of Montreal)  
   - Records of fire-related calls, incident types, timestamps, and event locations.
   - Avaialble online: https://donnees.montreal.ca/dataset/interventions-service-securite-incendie-montreal
- **Fire Station Locations** (Open Data - City of Montreal)  
   - Addresses and coverage details of fire stations.
   - Available online: https://donnees.montreal.ca/dataset/casernes-pompiers
- **Property Assessments** (Open Data - City of Montreal)  
   - Building attributes (floors, year of construction, surface area).
   - Avaialble online: https://donnees.montreal.ca/dataset/unites-evaluation-fonciere  
- **Crime Statistics** (Open Data - City of Montreal)  
   - Anonymized crime reports with timestamps, locations, and categories.
   - Avaialble online: https://donnees.montreal.ca/dataset/actes-criminels
- **Census Data** (Open Data - Statistics Canada, 2021)  
   - Demographic and socioeconomic variables (population density, income, dwelling types, etc.).
   - Available online: https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E

~~Datasets were preprocessed, aggregated, and aligned using an artificial 1km x 1km grid over Montréal Island, with unique identifiers for each grid cell.~~

## Data Exploration


## Data Aggregation

- Montréal was divided into 685 grid cells (each 1 km²)

![image](https://github.com/user-attachments/assets/6ad63505-fb1c-45c5-876b-ccd0799aaae8)

- Monthly aggregation of features for each grid cell included fire incidents, crime counts, building attributes, and census metrics.
  
- Fire Risk Definition: A grid cell was classified as high-risk if it had 2 or more fire incidents in a given month.


## Model and Results

Our predictive model classified grid areas into high-risk and low-risk categories. Key highlights:
- **Base Model**: XGBoost outperformed other algorithms with a weighted F1 score of 78.0%.
- **Class Imbalance**: Techniques like SMOTE and Oversampling significantly improved recall for high-risk areas.
- **Key Insights**:
  - Correctly predicted 81% of high-risk areas in the test set.
  - Potential cost savings of approximately $1.8M/month through proactive measures.

## Recommendations

The project underscores the need for continued exploration, including:
- Incorporating time-aligned demographic data for improved model accuracy.
- Leveraging additional internal datasets from the fire department for enriched features.
- Enhancing collaboration between data scientists and fire management experts.

## Conclusion

This project demonstrates how data-driven insights can strengthen Montréal's firefighting capabilities, safeguard communities, and reduce the financial burden of fire incidents.


## ~~Project Organization~~
```
├── project-name/
│   ├── notebooks/
│   │   ├── data_exploration.ipynb
│   │   ├── model_training.ipynb
│   ├── scripts/
│   │   ├── data_preprocessing.py
│   │   ├── model.py
│   │   ├── train.py
│   ├── results/
│   │   ├── figures/
│   │   │   ├── confusion_matrix.png
│   │   │   ├── accuracy_plot.png
│   │   ├── metrics.txt
│   ├── environment.yml (or requirements.txt)
│   ├── LICENSE
│   ├── README.md
│   └── .gitignore
```
## ~~Tools and Techniques~~

- **Data Cleaning and Processing**: Alteryx, Google Cloud BigQuery.
- **Model Development**: Python, Jupyter Notebooks, libraries such as XGBoost.
- **Visualization**: Tableau, Excel for impactful storytelling.
- **Advanced Methods**: SMOTE and Oversampling techniques to address class imbalance.
