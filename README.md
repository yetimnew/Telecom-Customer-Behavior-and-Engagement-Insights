# Telecom Customer Insights and Analytics

## Project Overview
This repository focuses on a comprehensive analysis of telecom customer data for a fictional company, **TellCo**, operating in the Republic of Pefkakia. The goal of the project is to extract actionable insights into customer behavior, engagement, experience, and satisfaction using advanced analytics techniques. Additionally, the project includes building an interactive dashboard for data visualization and decision-making.

## Objectives
- Perform exploratory data analysis (EDA) to understand customer behavior and identify patterns.
- Analyze user engagement metrics, network performance, and device usage.
- Segment users into meaningful clusters for engagement and experience.
- Predict customer satisfaction scores using machine learning models.
- Build an interactive dashboard to visualize the findings and provide actionable insights.

## Key Features
- **Data Preprocessing**: Cleaning and transforming raw telecom data from a PostgreSQL database.
- **Customer Overview Analysis**: Identifying popular handsets, manufacturers, and user patterns.
- **User Engagement Analysis**: Clustering customers based on engagement metrics using K-Means.
- **Experience Analytics**: Analyzing network parameters (TCP retransmission, RTT, throughput) and device characteristics.
- **Satisfaction Analysis**: Combining engagement and experience scores to predict customer satisfaction.
- **Interactive Dashboard**: A Streamlit-powered dashboard with intuitive navigation and clear visualizations.

## Repository Structure
```
├── .vscode/
│   └── settings.json          # Editor settings
├── .github/
│   └── workflows/
│       └── unittests.yml      # CI/CD workflow for unit testing
├── .gitignore                 # Files to ignore in version control
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation (this file)
├── src/
│   └── __init__.py            # Source code directory
├── notebooks/
│   ├── __init__.py            # Notebook initialization
│   └── README.md              # Documentation for Jupyter notebooks
├── tests/
│   └── __init__.py            # Unit test initialization
└── scripts/
    ├── __init__.py            # Script initialization
    └── README.md              # Documentation for scripts
```

## Technical Stack
- **Languages**: Python
- **Data Handling**: Pandas, NumPy, SQLAlchemy
- **Machine Learning**: Scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit
- **Database**: PostgreSQL
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd <repository-name>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the PostgreSQL database and update connection details in the configuration file.

## How to Run
1. Run the preprocessing and analysis scripts:
   ```bash
   python src/preprocessing.py
   python src/analysis.py
   ```
2. Launch the Streamlit dashboard:
   ```bash
   streamlit run scripts/dashboard.py
   ```
3. Access the dashboard through the provided local URL.

## Deliverables
- A comprehensive report summarizing insights from customer analysis.
- An interactive dashboard showcasing key metrics and visualizations.
- A deployed version of the dashboard accessible online.

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with detailed comments.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or feedback, please reach out to [Your Name or Email Address].

