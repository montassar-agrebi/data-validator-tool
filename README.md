<h1>Data Validation & Reconciliation Tool</h1>

<p>
A Python-based application designed to automate data validation between 
<strong>source</strong> and <strong>target datasets</strong> during 
data migration or ETL testing.
</p>

<p>
The tool helps analysts and engineers quickly detect inconsistencies,
missing records, and column mismatches between datasets while providing
clear migration health insights.
</p>

<hr>

<h2>Overview</h2>

<p>
Data migrations and ETL transformations often require validating that
the target dataset accurately reflects the source system.
Manual spreadsheet comparisons become inefficient and error-prone
when dealing with large datasets.
</p>

<p>
This tool automates the validation process and produces structured
reports that highlight discrepancies and data quality issues.
</p>

<hr>

<h2>Key Features</h2>

<h3>Flexible Key Selection</h3>
<p>
Users can manually select the <strong>primary comparison key</strong>
used to match records between the source and target datasets.
</p>

<p>
This allows validation across different table structures and
migration scenarios.
</p>

<h3>Duplicate Key Detection</h3>

<p>
The tool automatically checks the selected comparison key for
duplicate values.
</p>

<p>
If duplicates are detected, the validation process stops and
an error message is displayed to prevent incorrect comparisons.
Users can then select a different column as the comparison key.
</p>

<h3>Dataset Validation</h3>

<p>The validator compares:</p>

<ul>
<li>dataset schema</li>
<li>row counts</li>
<li>record presence between source and target</li>
</ul>

<p>
This helps detect missing or extra records during migrations.
</p>

<h3>Column-Level Validation</h3>

<p>The tool detects column inconsistencies including:</p>

<ul>
<li>value mismatches</li>
<li>null inconsistencies</li>
<li>missing data</li>
</ul>

<h3>Migration Health Insights</h3>

<p>
A validation summary provides an overview of the migration status,
including:
</p>

<ul>
<li>overall validation health</li>
<li>number of mismatched rows</li>
<li>affected columns</li>
<li>data quality indicators</li>
</ul>

<h3>Issue Sampling for Tracking</h3>

<p>
For each column containing discrepancies, the tool generates
<strong>up to five sample records</strong> showing the detected issue.
</p>

<p>
These samples are formatted as text so they can be easily copied
into validation trackers, issue logs, hierarchy reports,
or migration documentation.
</p>

<hr>

<h2>Quick Launch (Recommended)</h2>

<p>
For convenience, the repository includes a <strong>Windows launcher</strong>
that starts the application without requiring a Python installation.
</p>

<p>
The launcher uses a bundled <strong>portable Python environment</strong>
and installs required dependencies automatically if needed.
</p>

<p>To run the application:</p>

<ol>
<li>Download or clone the repository</li>
<li>Open the project folder</li>
<li>Double-click <strong>launch_validator.bat</strong></li>
</ol>

<p>
The Streamlit application will automatically open in your browser.
</p>

<hr>

<h2>Developer Setup</h2>

<p>If you prefer running the tool manually:</p>

<p>Install dependencies:</p>

<pre><code>
pip install -r requirements.txt
</code></pre>

<p>Run the application:</p>

<pre><code>
streamlit run app/app.py
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
├── app/
│   └── app.py
│
├── src/
│   └── validator_engine.py
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
<li>Run the validation</li>
<li>Review mismatch reports and migration insights</li>
</ol>

<hr>

<h2>Example Output</h2>

<ul>
<li>dataset comparison metrics</li>
<li>column mismatch reports</li>
<li>migration health summary</li>
<li>sample issue records for tracking</li>
</ul>

<p><em>Screenshots of the interface can be added in this section.</em></p>

<hr>

<h2>Future Improvements</h2>

<ul>
<li>database connection support</li>
<li>automated validation report export</li>
<li>large dataset optimization</li>
<li>scheduled validation jobs</li>
</ul>
