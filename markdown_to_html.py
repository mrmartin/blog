#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import os
import markdown

# Directory containing the .md files
directory = '.'

# List to store the HTML filenames for the index
html_files = []

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

        # Write the HTML content to the .html file
        with open(html_filename, 'w') as f:
            f.write(html_content)

# Create an index.html file that links to each generated HTML file
with open('index.html', 'w') as index_file:
    index_file.write('<html><head><title>Index of Markdown Files</title></head><body>\n')
    index_file.write('<h1>Index of Converted Markdown Files</h1>\n')
    index_file.write('<ul>\n')

    for html_file in html_files:
        index_file.write(f'<li><a href="{html_file}">{html_file}</a></li>\n')

    index_file.write('</ul>\n')
    index_file.write('</body></html>\n')

print("Conversion complete. 'index.html' has been created.")

