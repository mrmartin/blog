#!/usr/bin/env python3
# coding: utf-8

import os
import markdown
from urllib.parse import quote
import datetime

# Directory containing the .md files
directory = '.'

# List to store tuples of (filename, date) for sorting
md_files_with_dates = []

# Loop through all files in the current directory and get their modification dates
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        # Get the modification time
        mod_time = os.path.getmtime(filename)
        md_files_with_dates.append((filename, mod_time))

# Sort files by modification date, most recent first
md_files_with_dates.sort(key=lambda x: x[1], reverse=True)

# Bootstrap CSS link for styling
bootstrap_css = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">'

# List to store HTML filenames and their dates
html_files_with_dates = []

# Loop through sorted Markdown files
for filename, mod_time in md_files_with_dates:
    # Read the Markdown file
    with open(filename, 'r') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    # Create corresponding .html filename
    html_filename = filename.replace('.md', '.html')
    
    # Convert mod_time to a human-readable format with date and time
    formatted_date = datetime.datetime.fromtimestamp(mod_time).strftime('%B %d, %Y %H:%M:%S')
    html_files_with_dates.append((html_filename, formatted_date))

    # Create a styled HTML template including the date
    complete_html = f"""
    <html>
    <head>
        <title>{filename.replace('.md', '')}</title>
        {bootstrap_css}
    </head>
    <body>
        <div class="container">
            <header class="my-4">
                <h1>{filename.replace('.md', '').replace('_', ' ')}</h1>
            </header>
            <article>
                {html_content}
            </article>
            <footer class="my-4">
                <p>Written on: {formatted_date}</p>
                <p>&copy; 2024 Your Name</p>
            </footer>
        </div>
    </body>
    </html>
    """

    # Write the styled HTML content to the .html file
    with open(html_filename, 'w') as f:
        f.write(complete_html)

# Create a styled index.html file that links to each generated HTML file and shows the date
index_html_content = f"""
<html>
<head>
    <title>Index of Markdown Files</title>
    {bootstrap_css}
</head>
<body>
    <div class="container">
        <header class="my-4">
            <h1>Index of Converted Markdown Files</h1>
        </header>
        <ul class="list-group">
"""

# Use quote() to encode the filenames and display the dates with time
for html_file, formatted_date in html_files_with_dates:
    encoded_file = quote(html_file)
    index_html_content += f'<li class="list-group-item"><a href="{encoded_file}">{html_file.replace(".html", "").replace("_", " ")}</a> - {formatted_date}</li>\n'

index_html_content += """
        </ul>
        <footer class="my-4">
            <p>&copy; 2024 Your Name</p>
        </footer>
    </div>
</body>
</html>
"""

# Write the index HTML content to index.html
with open('index.html', 'w') as index_file:
    index_file.write(index_html_content)

print("Conversion complete. 'index.html' has been created.")
