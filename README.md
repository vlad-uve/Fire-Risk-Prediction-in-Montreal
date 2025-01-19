# Prediction of High Fire Risk Areas in Montréal

This repository contains the work for the **YCBS 299 Data Science Capstone Project** conducted by Team #6. The project focuses on using machine learning to predict high fire-risk areas in Montréal, enabling the fire department to optimize resource allocation, enhance response precision, and improve cost efficiency.

## Project Overview

The Montréal Fire Department faces increasing fire incidents despite stagnant staffing levels. Our goal was to develop a predictive model to identify areas at high risk for fire incidents, aiding in proactive resource deployment and enhanced operational efficiency.

Key objectives:
- **Enhance Response Precision**: Predict areas with high fire risk to enable strategic response.
- **Optimize Resource Allocation**: Allocate personnel and equipment to high-risk areas effectively.
- **Improve Cost-Efficiency**: Prioritize inspections and reduce preventive measure costs.
- **Support Budget Planning**: Provide foresight into expenditures for fire incident management.

## Data Sources

The analysis leveraged diverse datasets spanning January 2005 to January 2024, including:
- **Fire Incidents**: Historical data on fire incidents.
- **Fire Station Locations**: Details about fire station coverage.
- **Property Assessments**: Attributes of buildings and properties.
- **Crime Statistics**: Events categorized by type and geographic location.
- **Census Data**: Demographic and socioeconomic insights.

Datasets were preprocessed, aggregated, and aligned using an artificial 1km x 1km grid over Montréal Island, with unique identifiers for each grid cell.

## Tools and Techniques

- **Data Cleaning and Processing**: Alteryx, Google Cloud BigQuery.
- **Model Development**: Python, Jupyter Notebooks, libraries such as XGBoost.
- **Visualization**: Tableau, Excel for impactful storytelling.
- **Advanced Methods**: SMOTE and Oversampling techniques to address class imbalance.

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
