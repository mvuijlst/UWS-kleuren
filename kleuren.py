import pandas as pd
import yaml

# Load the Excel file
file_path = "colours.xlsx"  # Make sure the Excel file is named "colours.xlsx" and is in the same folder as this script
xls = pd.ExcelFile(file_path)

# Load the sheet into a DataFrame
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Create YAML structure for all palettes
palettes = {
    "palette": {
        col: [
            {"name": row["Name"], "slug": row["Slug"], "color": row[col]}
            for _, row in df.iterrows()
        ]
        for col in df.columns[2:]
    }
}

# Save YAML output to a file
yaml_file_path = "palettes.yaml"
with open(yaml_file_path, "w") as file:
    yaml.dump(palettes, file, sort_keys=False)

print(f"YAML file saved to: {yaml_file_path}")

# Define HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Color Palettes</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; color: white; background-color: #444444}}
        .palette-container {{ margin-bottom: 10px; }}
        .palette-name {{ font-weight: bold; margin-right: 10px; font-size: 1.2em; text-align: right; display: inline-block; width: 100px; }}
        .palette {{ display: flex; align-items: center; margin-bottom: 5px; }}
        .color-circle {{
            width: 40px; height: 40px; display: inline-block;
        }}
    </style>
</head>
<body>
    <h1>All Color Palettes</h1>
    {palettes}
</body>
</html>
"""

# Define a function to create HTML for all palettes with names
def generate_full_palette_html(df):
    html = ""
    # Loop through columns that represent palettes (after "Name" and "Slug")
    for col in df.columns[2:]:
        html += f"<div class='palette-container'>"
        html += "<div class='palette'>"
        html += f"<span class='palette-name'>{col}</span>"
        for _, row in df.iterrows():
            html += f"<div class='color-circle' style='background-color: {row[col]}'></div>"
        html += "</div></div><br/>"
    return html

# Generate the full HTML content for all palettes
full_palette_html = generate_full_palette_html(df)

# Combine HTML content with labels in front of circles
html_content_full = html_template.format(palettes=full_palette_html)

# Save the HTML output with labels
html_file_path = "color_palettes_with_labels.html"
with open(html_file_path, "w") as html_file:
    html_file.write(html_content_full)

print(f"HTML file saved to: {html_file_path}")
