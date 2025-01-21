# Prediction of High Fire Risk Areas in Montréal

This repository contains the work for the **YCBS 299 - Data Science Capstone Project** course at McGill University conducted in 2024 by Team #6: Felix MARTINEZ MEJIAS, Sienko IKHABI, Vladislav YUSHKEVICH, Vadim STRELNIKOV. ~~The project focuses on using machine learning to predict high fire-risk areas in Montréal, enabling the fire department to optimize resource allocation, enhance response precision, and improve cost efficiency.~~

## Project Overview

The Montreal Fire Department faces rising fire incidents despite limited staffing and resources. This project aims to **predict monthly high fire-risk areas** using advanced analytics and machine learning, enabling improved resource allocation and preemptive strategies that enhance public safety and reduce operational costs.

Key objectives:
- **Enhance Response Precision**: Develop a machine learning model capable of accurately predict areas with high fire risk to enable swift strategic response.
- **Optimize Resource Allocation**: Allocate personnel and equipment to high-risk areas effectively.
- **Improve Cost-Efficiency**: Prioritize inspections and reduce preventive measure costs.
- **Support Budget Planning**: Provide foresight into expenditures for fire incident management.

The data science project directly addresses the critical needs of the Montreal Fire Department, aligning with goals of efficiency, effectiveness, and fiscal responsibility. By enhancing the accuracy of fire incident predictions, the model optimizes resource deployment and bolsters the city's firefighting capabilities, ultimately contributing to the safety and well-being of its residents.
  
## Data Overview and Exploration

The analysis leveraged diverse datasets spanning January 2005 to January 2024, including:
- **Fire Incidents** (Open Data - City of Montreal)  
   - Records of fire-related calls, incident types, timestamps, and event locations.
   - ~~Avaialble online: https://donnees.montreal.ca/dataset/interventions-service-securite-incendie-montreal~~
- **Fire Station Locations** (Open Data - City of Montreal)  
   - Addresses and coverage details of fire stations.
   - ~~Available online: https://donnees.montreal.ca/dataset/casernes-pompiers~~
- **Property Assessments** (Open Data - City of Montreal)  
   - Building attributes (floors, year of construction, surface area).
   - ~~Avaialble online: https://donnees.montreal.ca/dataset/unites-evaluation-fonciere~~ 
- **Crime Statistics** (Open Data - City of Montreal)  
   - Anonymized crime reports with timestamps, locations, and categories.
   - ~~Avaialble online: https://donnees.montreal.ca/dataset/actes-criminels~~
- **Census Data** (Open Data - Statistics Canada, 2021)  
   - Demographic and socioeconomic variables (population density, income, dwelling types, etc.).
   - ~~Available online: https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm?Lang=E~~

~~Datasets were preprocessed, aggregated, and aligned using an artificial 1km x 1km grid over Montréal Island, with unique identifiers for each grid cell.~~

## Data Aggregation

- Montréal was divided into 685 grid cells (each 1 km²)

- Monthly aggregation of features for each grid cell included fire incidents, crime counts, building attributes, and census metrics.
  
- Fire Risk Definition: A grid cell was classified as high-risk if it had 2 or more fire incidents in a given month.

## Feature Engineering



## Modelling Approach


![image](https://github.com/user-attachments/assets/bac8123c-3f13-4c01-be08-bd0aa997c1c2)



## Base Model Results
The evaluation of baseline models highlighted the performance gap between simple and advanced methods, as shown in the accompanying confusion matrices and performance metrics:

- **Dummy Classifier**: Set the baseline with an F1-score of **0.47**, reflecting its limited predictive capability.  
- **Decision Tree Classifier**: Marginally improved performance with an F1-score of **0.55**.  
- **XGBoost**: Achieved a notable F1-score of **0.63** using a basic configuration, demonstrating its potential for handling the classification task.  
- **LightGBM**: Delivered comparable performance to XGBoost, with an F1-score of **0.62**.  

The visualized metrics underscore XGBoost’s ability to outperform simpler models, justifying its selection for further optimization in handling the fire-risk prediction challenge.

![image](https://github.com/user-attachments/assets/a90c8cdd-a91a-472a-aa16-19b5117b4498)


## Improvement of XGBoost

The main issue affecting the model's predictive accuracy was the class imbalance. The dataset contained significantly more low-risk examples (~100,517) than high-risk examples (~13,878). To mitigate this imbalance, techniques such as **SMOTE** and **Oversampling** were applied to increase the representation of the high-risk class.

- **SMOTE** improved high-risk recall to **51%**, while **Oversampling** further enhanced it to **81%**.  
![image](https://github.com/user-attachments/assets/0dc0dd53-0826-4ad7-a52b-06bbf1d23d0d) 

- These methods also contributed to better overall weighted F1-scores for the model, balancing precision and recall effectively.
![image](https://github.com/user-attachments/assets/2f4b8ae4-ef6f-4da9-97ca-aaa567bab858) 

-
![image](https://github.com/user-attachments/assets/2e3d14fe-5b8a-4f4f-883f-2585fbd94d40)

- **Impact of Balancing**:  
  - **SMOTE** improved high-risk recall to **51%**, while Oversampling further enhanced it to **81%**.  


The improved XGBoost model demonstrated a marked increase in its ability to correctly predict high-risk areas, making it more suitable for practical implementation in fire-risk management.

## Modelling Results

The images below highlight the efficacy of the **XGBoost model** in predicting high fire-risk areas across Montréal for January 2024. ~~Compare both saying that hgh risk zonez are successfully aught even thouagh a mistake type 1 presents~~
![image](https://github.com/user-attachments/assets/b45d9a77-2223-4e98-a5fd-53808f8b3e29)
![image](https://github.com/user-attachments/assets/22eef90b-f2d0-418f-af90-f5b26cff49c0)

Model testing on the test set (~~2024?~~)
![image](https://github.com/user-attachments/assets/c13985db-8380-45ed-803c-e8cdba3c4264)



Key metrics include:
- **High-Risk Prediction Accuracy**: The model correctly predicted 72 out of 98 high-risk grid areas for January 2024, achieving a recall rate of 81%.  
- **Low-Risk Prediction Accuracy**: Correctly identified 73% of low-risk areas, providing actionable insights for targeted inspections.  
- **Cost Impact**: Predictions could save the Montréal Fire Department approximately **$1.8 million per month**, based on average insurance coverage of $25,000 per fire incident.  
- **Proactive Inspections**: Identifying 583 low-risk events offers an opportunity to focus preventive efforts, reducing overall fire incidents.  

These findings emphasize the model’s ability to enhance **operational efficiency**, **cost savings**, and **public safety** through data-driven insights.

## Business Impact and Recommendations

Using January 2024 as an example, the fire-risk prediction model demonstrates significant potential for enhancing fire prevention strategies in Montréal, enabling impactful operational and cost-saving benefits:  

- **High-Risk Prediction Accuracy**: The model predicted **98 high-risk events** for January 2024, of which **72 were correctly identified**, showcasing its ability to highlight critical areas for intervention.  
- **Cost Savings**: The correct predictions of the high fire risk incidents could save approximately **$1.8 million per month**, based on an average insurance coverage of **$25,000 per fire incident**.
- **Low-Risk Predictions**: Identified **583 low-risk events**, creating an opportunity for focused preventive inspections to proactively reduce fire incidents.  
- **Efficient Resource Allocation**: Proactive inspections and targeted interventions decrease staff workload, allowing for better resource reallocation and enhanced service delivery.  
- **Potential Trends and Focus Zones**: The model offers insights into recurring high-risk areas, enabling data-driven refinement of preventive strategies and resource optimization.  

These results underscore the model’s ability to improve public safety while offering actionable recommendations to guide future fire prevention initiatives in Montréal.

## ~~Conclusion~~

Our predictive model classified grid areas into high-risk and low-risk categories. Key highlights:
- **Base Model**: XGBoost outperformed other algorithms with a weighted F1 score of 78.0%.
- **Class Imbalance**: Techniques like SMOTE and Oversampling significantly improved recall for high-risk areas.
- **Key Insights**:
  - Correctly predicted 81% of high-risk areas in the test set.
  - Potential cost savings of approximately $1.8M/month through proactive measures.

## ~~Recommendations~~

The project underscores the need for continued exploration, including:
- Incorporating time-aligned demographic data for improved model accuracy.
- Leveraging additional internal datasets from the fire department for enriched features.
- Enhancing collaboration between data scientists and fire management experts.

## ~~Conclusion~~

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
