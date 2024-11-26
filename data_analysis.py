import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os


def process_data(dataset_file, feature_desc_file):
    # Read the dataset
    data = pd.read_csv(dataset_file)
    # Read the feature description
    feature_desc = pd.read_csv(feature_desc_file)
    columns_of_dataset = data.columns.tolist()
    # Data cleaning: You can customize this part based on your requirements
    # Example: Drop rows with missing values
    data = data.dropna()

    # Descriptive statistics
    stats = data.describe(include='all').to_dict()

    # Create and save plots for each numeric feature
    plot_paths = []
    for col in data.select_dtypes(include='number').columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(data[col], kde=True)
        plt.title(f'Distribution of {col}')
        plot_path = f'public/{col}_plot.png'
        graph_path = f'{col}_plot.png'
        plt.savefig(plot_path)
        plt.close()
        plot_paths.append(graph_path)

    # Generate insights based on feature description
    insights = []
    for index, row in feature_desc.iterrows():
        feature_name = row['Feature']
        description = row['Description']
        insights.append(f"The feature '{feature_name}' is described as: {description}")

    # Prepare the output
    output = {
        'feature': columns_of_dataset,
        'statistics': stats,
        'plots': plot_paths,
        'insights': insights
    }

    # Print the output as JSON
    print(json.dumps(output))

if __name__ == '__main__':
    # Ensure two arguments are provided (dataset and feature description files)
    if len(sys.argv) != 3:
        print("Usage: python data_analysis.py <dataset_file> <feature_desc_file>")
        sys.exit(1)

    dataset_file = sys.argv[1]
    feature_desc_file = sys.argv[2]

    # Call the data processing function
    process_data(dataset_file, feature_desc_file)
