# Log Analysis
Log analysis is a simple python report tool, that prints out a plain text reports based on a data from `news` database. The database contains newspaper articles, as well as the web server log for the site. The log has a row for each time a reader loaded a web page.

## Installation
To run this project, first you'll need database software (provided by a Linux virtual machine) and the data to analyze.
- To install the virtual machine follow the instructions [here]( https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
- To load the sample data, download it from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and use the command `psql -d news -f newsdata.sql` to load it to your database.

### What are we reporting?
1. What are the most popular three articles of all time?
    - use `top_articles()` function

2. Who are the most popular article authors of all time?
    - use `top_authors()` function

3. On which days did more than 1% of requests lead to errors?
    - use `errors_by_day()` function

### Run example
- Run a python interpreter `python`.
- Type `import log_analysis as l`
- Execute a function `l.errors_by_day()`
