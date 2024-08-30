#!/usr/bin/env python3
# coding: utf-8

import os
import markdown
from urllib.parse import quote

# Directory containing the .md files
directory = '.'

# List to store the HTML filenames for the index
html_files = []

# Bootstrap CSS link for styling
bootstrap_css = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">'

# Loop through all files in the current directory
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        # Read the Markdown file
        with open(filename, 'r') as f:
            md_content = f.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # Create corresponding .html filename
        html_filename = filename.replace('.md', '.html')
        html_files.append(html_filename)

        # Create a styled HTML template
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
                    <p>&copy; 2024 Zero One</p>
                </footer>
            </div>
        </body>
        </html>
        """

        # Write the styled HTML content to the .html file
        with open(html_filename, 'w') as f:
            f.write(complete_html)

# Create a styled index.html file that links to each generated HTML file
index_html_content = f"""
<html>
<head>
    <title>Blog by Zero One - AI author</title>
    {bootstrap_css}
</head>
<body>
    <div class="container">
        <header class="my-4">
            <h1>Index of Articles</h1>
        </header>
        <ul class="list-group">
"""

# Use quote() to encode the filenames
for html_file in html_files:
    encoded_file = quote(html_file)
    index_html_content += f'<li class="list-group-item"><a href="{encoded_file}">{html_file.replace(".html", "").replace("_", " ")}</a></li>\n'

index_html_content += """
        </ul>
        <footer class="my-4">
            <p>&copy; 2024 Zero One</p>
        </footer>
    </div>
</body>
</html>
"""

# Write the index HTML content to index.html
with open('index.html', 'w') as index_file:
    index_file.write(index_html_content)

print("Conversion complete. 'index.html' has been created.")
