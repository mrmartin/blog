#!/bin/bash

# Define an array of topics
topics=(
    "The Role of Dark Matter in Galaxy Formation"
    "Quantum Entanglement and Its Implications for Communication"
    "Philosophical Implications of the Multiverse Theory"
    "The Economics of Climate Change and Carbon Pricing"
    "AI Ethics: The Challenges of Autonomous Decision-Making"
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

./markdown_to_html.py
git add *.html
git commit -m "new articles"
git push