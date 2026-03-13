<h1>📊 Data Validation & Reconciliation Tool</h1>

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/framework-streamlit-red)
![License](https://img.shields.io/badge/license-MIT-green)

<p>
A Python-based application designed to automate data validation between 
<strong>source</strong> and <strong>target datasets</strong> during 
data migration, ETL validation, or system reconciliation processes.
</p>

<p>
The tool allows analysts and data engineers to quickly detect 
data inconsistencies, missing records, and column mismatches while
providing clear insights about overall data migration health.
</p>

<hr>

<h2>Overview</h2>

<p>
Data migrations and ETL pipelines require validating that the
target system accurately reflects the source dataset.
</p>

<p>
Manual spreadsheet comparisons become inefficient and unreliable
when working with large datasets or complex schemas.
</p>

<p>
This application automates the validation workflow and produces
clear validation summaries that highlight discrepancies
between datasets.
</p>

<hr>

<h2>Key Features</h2>

<h3>Flexible Primary Key Selection</h3>

<p>
Users can manually select the <strong>primary key</strong>
used to align records between the source and target datasets.
</p>

<p>
This flexibility allows validation across different table
structures and migration scenarios.
</p>

<h3>Duplicate Key Detection</h3>

<p>
The tool automatically checks the selected comparison key
for duplicate values in both datasets.
</p>

<p>
If duplicates are detected, validation stops and an error message
is displayed to prevent incorrect comparisons.
</p>

<p>
Users can then select another column as the comparison key.
</p>

<h3>Dataset Alignment</h3>

<p>
The validator aligns rows between datasets using the selected key
before performing comparisons.
</p>

<p>
It also detects records that exist only in one dataset,
helping identify potential data loss or unexpected records.
</p>

<h3>Column-Level Validation</h3>

<p>
Each column shared between the datasets is compared to detect
value differences including:
</p>

<ul>
<li>value mismatches</li>
<li>null inconsistencies</li>
<li>missing values</li>
<li>unexpected value changes</li>
</ul>

<h3>Comparison Modes</h3>

<p>The tool provides two comparison modes:</p>

<ul>
<li><strong>Normalized Mode</strong> – removes formatting differences such as case sensitivity, trailing spaces, and numeric formatting</li>
<li><strong>Strict Mode</strong> – compares values exactly as stored in the datasets</li>
</ul>

<h3>Migration Health Insights</h3>

<p>
After validation, the application produces a summary
showing the overall data migration health.
</p>

<p>The dashboard includes:</p>

<ul>
<li>rows compared</li>
<li>columns compared</li>
<li>mismatched values</li>
<li>rows containing discrepancies</li>
<li>attribute accuracy scores</li>
</ul>

<h3>Mismatch Classification</h3>

<p>
Detected issues are automatically categorized to help
understand the root cause of discrepancies.
</p>

<p>Examples include:</p>

<ul>
<li>perfect matches</li>
<li>missing values on source</li>
<li>missing values on target</li>
<li>mostly incorrect values</li>
<li>mixed mismatch patterns</li>
</ul>

<h3>Issue Sampling for Tracking</h3>

<p>
For each column containing mismatches, the tool generates
<strong>up to five example records</strong> showing the detected issue.
</p>

<p>
These samples are formatted as text so they can easily be copied
into issue trackers, validation logs, or data quality reports.
</p>

<hr>

<h2>Quick Launch (Recommended)</h2>

<p>
The repository includes a <strong>Windows launcher</strong>
allowing the application to run without installing Python manually.
</p>

<p>
The launcher uses a bundled <strong>portable Python environment</strong>
and installs required dependencies automatically when needed.
</p>

<p>To run the application:</p>

<ol>
<li>Download or clone the repository</li>
<li>Open the project folder</li>
<li>Double-click <strong>🚀 Start Data Validation Tool.bat</strong></li>
</ol>

<p>
The Streamlit dashboard will automatically open in your browser.
</p>

<hr>

<h2>Developer Setup</h2>

<p>If you prefer running the application manually:</p>

<p>Install dependencies:</p>

<pre><code>
pip install -r requirements.txt
</code></pre>

<p>Run the application:</p>

<pre><code>
streamlit run app.py
</code></pre>

<hr>

<h2>Tech Stack</h2>

<ul>
<li>Python</li>
<li>Pandas</li>
<li>Streamlit</li>
</ul>

<hr>

<h2>Project Structure</h2>

<pre><code>
data-validator-tool
│
├── launch_validator.bat
├── python_portable/
│
├── app.py
│
├── src/
│   ├── validator.py
│   ├── comparison.py
│   └── profiling.py
│
├── sample_data/
│
├── screenshots/
│
├── requirements.txt
└── README.md
</code></pre>

<hr>

<h2>Example Workflow</h2>

<ol>
<li>Upload the source dataset</li>
<li>Upload the target dataset</li>
<li>Select the comparison key</li>
<li>Choose the comparison mode</li>
<li>Run the validation</li>
<li>Review mismatch insights and migration metrics</li>
</ol>

<hr>

<h2>Example Output</h2>

<ul>
<li>dataset comparison metrics</li>
<li>column accuracy scores</li>
<li>migration health summary</li>
<li>mismatch samples for issue tracking</li>
<li>exportable mismatch reports</li>
</ul>

<p><em>Screenshots of the interface can be added in this section.</em></p>

<hr>

<h2>Application Preview</h2>

<p align="center">
<img src="screenshots/dashboard.png" width="900">
</p>

<hr>

<h2>Future Improvements</h2>

<ul>
<li>database connection support</li>
<li>automated validation report exports</li>
<li>large dataset optimization</li>
<li>scheduled validation workflows</li>
<li>support for additional file formats</li>
</ul>

<h2>Download Portable Version</h2>

<p>
A portable version of the application is available in the repository releases.
</p>

<p>
Download the ZIP package and run the launcher to start the tool without installing Python.
</p>
