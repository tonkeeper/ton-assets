import csv

from to_review.models import AssetData

ROW_TEMPLATE = """
      <tr class="row{i}">
        <td class="index">{i}</td>
        <td class="address"><a href="{link}" class="address{i}">{address}</a></td>
        <td class="category"><input type="text" class="category{i}" name="category{i}" placeholder="Enter category" value="{category}"></td>
        <td class="name"><input type="text" class="name{i}" name="name{i}" placeholder="Enter name" value="{name}"></td>
        <td class="website"><a href="website" class="website{i}">{website}</a></td>
        <td class="description"><input type="text" class="description{i}" name="description{i}" placeholder="Enter description" value="{description}"></td>
        <td class="accept"><input type="checkbox" class="accept{i}" name="{i}"></td>
      </tr>
"""
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>To review</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
    }}
    a {{
        text-decoration: none;
    }}
    table {{
      border-collapse: collapse;
    }}
    th, td {{
      padding: 9px;
      text-align: left;
      border: 1px solid #ddd;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .address {{
      min-width: 260px;
      max-width: 280px;
    }}
    .name {{
      min-width: 190px;
      max-width: 210px;
    }}
    .category {{
      min-width: 170px;
      max-width: 190px;
    }}
    .website {{
      min-width: 150px;
      max-width: 200px;
    }}
    .description {{
      width: 100%;
    }}
    th {{
      background-color: #f4f4f4;
    }}
    tr:nth-child(even) {{
      background-color: #f9f9f9;
    }}
    input[type="text"] {{
      width: 100%;
      padding: 6px;
      box-sizing: border-box;
      font-size: 16px;
    }}
    button {{
      padding: 10px 15px;
      width: 100%;
      font-size: 14px;
      cursor: pointer;
      background-color: lightsteelblue;
      border-radius: 4px;
      border: none;
    }}
    button:hover {{
      background-color: lightblue;
    }}
    .index {{
        text-align: center;
    }}
    #floating-button {{
      max-width: 120px;
      position: fixed;
      top: 3px;
      right: 10px;
      background-color: #007BFF;
      color: white;
      border: none;
      border-radius: 4px;
      padding: 12px 20px;
      font-size: 16px;
      cursor: pointer;
      z-index: 1000;
    }}
    
    #floating-button:hover {{
      background-color: #0056b3;
    }}
  </style>
</head>
<body>
  <h2>To review</h2>
  <table>
    <thead>
      <tr>
        <th class="index">#</th>
        <th>Address</th>
        <th>Category</th>
        <th>Name</th>
        <th>Website</th>
        <th>Description</th>
        <th>Accept</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <button id="floating-button" onclick="handleGenerateButtonClick()">Generate YAMLs</button>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
  <script>
      function handleGenerateButtonClick() {{
          const checkboxes = document.querySelectorAll('input[type="checkbox"]');
          const groupedData = {{}};
          groupedData["skiplist"] = [];
          checkboxes.forEach((checkbox) => {{
              const idx = checkbox.name;
              const address = document.querySelector(`.address${{idx}}`).textContent.trim();
              if (checkbox.checked) {{
                  const name = document.querySelector(`.name${{idx}}`).value.trim();
                  const website = document.querySelector(`.website${{idx}}`).textContent.trim()
                  const description = document.querySelector(`.description${{idx}}`).value.trim()
                  if (!groupedData[name]) {{
                      groupedData[name] = [];
                  }}

                  groupedData[name].push({{ address, name, website, description }});
                  document.querySelector(`.row${{idx}}`).style.backgroundColor = "lightgrey";
              }} else {{
                  groupedData["skiplist"].push(address);
                  document.querySelector(`.row${{idx}}`).style.backgroundColor = "white";
              }}
          }});

          if (Object.keys(groupedData).length === 0) {{
              alert("No rows selected.");
              return;
          }}

          const zip = new JSZip();
          for (const [name, entries] of Object.entries(groupedData)) {{
              let content = "";
              let filename = "";
              if (name === "skiplist") {{
                content = entries.join("\\n")
                filename = "skip_list.csv";
              }} else {{
                content = entries.map(item => {{
                  const lines = [];
                  lines.push(`- address: "${{item.address}}"\\n`);
                  lines.push(`  name: "${{item.name}}"\\n`);
                  if (item.description !== "") {{
                    lines.push(`  description: "${{item.description}}"\\n`);
                  }}
                  if (item.website !== "") {{
                    lines.push(`  websites:\\n    - "${{item.website}}"\\n`);
                  }}
                  return lines.join("")
                }}).join("");

                filename = `${{name.replace(/\\s+/g, '_').toLowerCase()}}.yaml`;
              }}

              zip.file(filename, content);
          }}

          zip.generateAsync({{ type: "blob" }}).then(function (blob) {{
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "generated_yamls.zip";
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
          }});
      }}
  </script>
</body>
</html>
"""

def generate_to_review_html(assets: list[AssetData]):
    with open("to_review.html", "w") as html:
        rows = ""
        for i in range(len(assets)):
            asset = assets[i]
            rows += ROW_TEMPLATE.format(
                i=i,
                link=asset.link,
                address=asset.address,
                category=asset.category,
                name=asset.name,
                website=asset.website,
                description=asset.description,
            )

        page = PAGE_TEMPLATE.format(rows=rows)

        html.write(page)

def add_blacklist(assets: list[AssetData]):
    with open("blacklist.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        for asset in assets:
            writer.writerow([asset.address])