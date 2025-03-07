#!/usr/bin/env python3
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Define module structure based on navigation
system_structure = {
    "name": "专家知识库系统",
    "modules": [
        {
            "name": "知识录入",
            "icon": "fa-edit",
            "pages": [
                {"name": "对话标注", "path": "ExpertKnowledge/Knowledge_Entry/对话标注.html"}
            ]
        },
        {
            "name": "知识管理",
            "icon": "fa-database",
            "pages": [
                {"name": "专家策略库", "path": "ExpertKnowledge/Knowledge_Management/专家策略.html"}
            ]
        },
        {
            "name": "模型评测",
            "icon": "fa-flask",
            "pages": [
                {"name": "对战界面", "path": "ExpertKnowledge/Model_Evaluation/对战界面.html"},
                {"name": "对战结果界面", "path": "ExpertKnowledge/Model_Evaluation/对战结果界面.html"}
            ]
        }
    ]
}

# Flatten page list for screenshots
html_files = []  # Remove index page from screenshots
for module in system_structure["modules"]:
    for page in module["pages"]:
        if "对战数据创建" not in page["name"]:  # Skip 对战数据创建 page
            html_files.append(page["path"])

# Set up Chrome options for headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Get the current working directory
current_dir = os.getcwd()

# Create screenshots directory if it doesn't exist
screenshots_dir = os.path.join(current_dir, "ExpertKnowledge/screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

# Dictionary to store screenshot paths for each page
screenshot_paths = {}

# Capture screenshots of all HTML files
print("Capturing screenshots of all pages...")
for html_file in html_files:
    # Create absolute file path from relative path
    file_path = f"file://{os.path.join(current_dir, html_file)}"
    
    # Get page name for the screenshot file
    page_name = os.path.basename(html_file).replace(".html", "")
    screenshot_file = f"{page_name}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_file)
    
    # Save the path for later use in the architecture diagram
    screenshot_paths[html_file] = screenshot_path
    
    # Load the page and take a screenshot
    print(f"Loading {file_path}...")
    driver.get(file_path)
    
    # Wait for any JS to load
    time.sleep(2)
    
    # Capture screenshot
    print(f"Capturing screenshot to {screenshot_path}...")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")

# Generate HTML architecture diagram and page
print("\nGenerating architecture page...")

# Generate HTML page to view the architecture with screenshots
html_output = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专家知识库系统架构</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
            padding: 20px;
            background-color: #f5f7fa;
        }
        .card {
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .module-title {
            background-color: #2c6ecb;
            color: white;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .page-title {
            font-weight: bold;
            margin: 10px 0;
        }
        .screenshot {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease-in-out;
        }
        .screenshot:hover {
            transform: scale(1.02);
        }
        
        /* Architecture diagram styling */
        .architecture-container {
            margin: 30px 0;
            overflow-x: auto;
        }
        .architecture-diagram {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .system-node {
            background-color: #2c6ecb;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            font-size: 1.5rem;
            font-weight: 600;
            width: 300px;
        }
        .modules-container {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }
        .module-node {
            background-color: #eef4fd;
            border: 2px solid #2c6ecb;
            color: #2c6ecb;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 220px;
            position: relative;
        }
        .module-node::before {
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            width: 2px;
            height: 20px;
            background-color: #2c6ecb;
        }
        .pages-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            margin-top: 20px;
        }
        .page-node {
            background-color: white;
            border: 1px solid #2c6ecb;
            color: #333;
            padding: 8px 15px;
            border-radius: 4px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            width: 180px;
            position: relative;
        }
        .page-node::before {
            content: '';
            position: absolute;
            top: -10px;
            left: 50%;
            width: 1px;
            height: 10px;
            background-color: #2c6ecb;
        }
        .vertical-line {
            width: 2px;
            height: 20px;
            background-color: #2c6ecb;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <h1 class="my-4 text-center">专家知识库系统架构图</h1>
        
        <!-- Architecture Diagram -->
        <div class="architecture-container">
            <div class="architecture-diagram">
                <div class="system-node">专家知识库系统</div>
                <div class="vertical-line"></div>
                <div class="modules-container">
"""

# Add module nodes to the diagram
for module in system_structure["modules"]:
    html_output += f"""
                    <div class="module-column">
                        <div class="module-node">
                            <i class="fas {module['icon']} mb-2"></i><br>
                            {module['name']}
                        </div>
                        <div class="pages-container">
    """
    
    # Add page nodes for this module
    for page in module["pages"]:
        html_output += f"""
                            <div class="page-node">{page['name']}</div>
        """
    
    html_output += """
                        </div>
                    </div>
    """

# Close the architecture diagram container
html_output += """
                </div>
            </div>
        </div>
        
        <h2 class="my-4 text-center">模块截图</h2>
"""

# Add each module section with its pages and screenshots
for module in system_structure["modules"]:
    html_output += f"""
        <div class="row">
            <div class="col-12">
                <h3 class="module-title"><i class="fas {module['icon']} mr-2"></i>{module['name']}</h3>
            </div>
    """
    
    # Add each page in the module
    for page in module["pages"]:
        page_name = os.path.basename(page["path"]).replace(".html", "")
        html_output += f"""
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header">
                        <h4 class="m-0">{page["name"]}</h4>
                    </div>
                    <div class="card-body">
                        <div class="text-center">
                            <img src="{page_name}.png" alt="{page["name"]}" class="screenshot">
                        </div>
                    </div>
                </div>
            </div>
        """
    
    html_output += "        </div>\n"

# Close the HTML document
html_output += """
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Write the HTML file
architecture_html_path = os.path.join(screenshots_dir, "architecture.html")
with open(architecture_html_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"Architecture HTML page saved as {architecture_html_path}")

# Close the browser
driver.quit()

print("\nProcess completed successfully!")
print(f"Screenshots saved to: {screenshots_dir}")
print(f"Architecture HTML page saved to: {architecture_html_path}")
print("\nYou can view the complete system architecture by opening the architecture.html file in your browser.") 