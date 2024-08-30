#!/bin/bash

# Define an array of topics
topics=(
    "The Impact of Quantum Computing on Cryptography"
    "Ethical Implications of AI in Healthcare"
    "The Role of Renewable Energy in Mitigating Climate Change"
    "Pros and Cons of Remote Work in the Tech Industry"
    "The Future of Autonomous Vehicles in Urban Environments"
    "Challenges and Opportunities of Colonizing Mars"
    "The Influence of Social Media on Public Opinion and Political Movements"
    "Should We Fear AI Becoming Superintelligent?"
    "The Economic Impact of Universal Basic Income (UBI)"
    "Genetic Editing: The Promise and Perils of CRISPR Technology"
)

# Python script to generate article
python_script="discuss_and_generate_article.py"

# Loop through each topic and run the Python script, saving output to a file
for topic in "${topics[@]}"; do
    # Replace spaces with underscores for the filename
    filename=$(echo "$topic" | tr ' ' '_').md

    echo "Generating article for topic: $topic"
    echo "Saving to file: $filename"

    # Run the Python script and save the output to a file
    ./$python_script "$topic" "$filename"

    echo "------------------------------------------"
done

echo "All topics processed."
