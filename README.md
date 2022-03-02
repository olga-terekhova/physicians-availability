# physicians-availability
## the goal of the project
I want to visualize data about the number of physicians in Ontario per area. The source data is provided by Ontario Physician Human Resources Data Centre. The result should clearly show which geographical area has more or less physicians per 100 000 population. The result is hosted at https://olga-terekhova.github.io/html/physicians.html .
## flow chart of the project
![flow chart of the project](https://github.com/olga-terekhova/physicians-availability/blob/main/docs/diagram.png)
## description of the flows
### 1 - Grabbing the data and saving it into CSV
Source: 
1. https://www.ophrdc.org/wp-content/uploads/2021/11/2020-PIO-Annual-Report.pdf copied to https://github.com/olga-terekhova/physicians-availability/blob/main/data/2020-PIO-Annual-Report.pdf

Python code: 
The function extract_table:
1. Takes the source pdf
2. Parses two pages with the needed table
3. Splits it by dividers
4. Loads it into pandas dataframe
5. Assigns labels
6. loads the data into a csv file. 
Dependencies: 
1. tabula-py and java runtime used by tabula-py under the hood to parse a PDF into a table. 
2. pandas.

Outcome:
1. CSV file with values (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_values_2020.csv)


### 2 - Calculating ranking of LHINs for every specialty of practice
Source:
1. CSV file with the source data (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_values_2020.csv)

Python code: 
The function assign_rank:
1. Calculates a mininum and a maximum value for the "Physicians per 100 000 population" measure within each row.
2. Assigns a rank for each LHIN within this row calculated according to the formula: (current LHIN value - min value) / (max value - min value), so that the rank ranges from 0 to 1.
3. Saves the result for the current row into cells labeled as "Name of the LHIN" + " - Rank". 
4. Writes the resulting dataset into a CSV.
Dependencies: 
1. pandas.

Outcome:
1. CSV file with ranking (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_rank_2020.csv)

### 3 - Generating an HTML file with the table containing the data and colored according to the ranking
Source:
1. The initial HTML file (https://github.com/olga-terekhova/physicians-availability/blob/main/html/physicians_src.html) contains the whole content of the target HTML file except for the table with data. Instead of this a placeholder "&lt;table&gt;&lt;/table&gt;" is used.
2. CSV file with values (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_values_2020.csv)
3. CSV file with ranking (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_rank_2020.csv)

Python code: 
The function generate_html_table:
1. Generates the whole TABLE element containing values from the CSV file with values. 
2. Adds a JavaScript function call to the headings with the names of LHINs and passes the code of the LHIN as a parameter. It will allow the user to select a current LHIN by clicking on the headings. 
3. Adds element names "LHINleft" and "LHINright" to the cells. It will allow to highlight properly the left and and the right column for a LHIN when the user selects a LHIN.
4. Calculates an HSL background color for each cell according to the rank of the LHIN within each row. H component is 120 (green), S component is 50%, L component is calculated according to the formula: (1-(Rank/2)) * 100, so that the highest ranked LHIN has 50% lightness (green) and the lowest ranked LHIN has 100% lightness (white).
5. Replaces the "&lt;table&gt;&lt;/table&gt;" in the source file with the generated TABLE element.

Outcome:
1. Resulting HTML file (https://github.com/olga-terekhova/physicians-availability/blob/main/html/physicians.html)

### 4 - Creating an SVG map of LHINs
Source:
1. PNG file with a map of LHINs (https://github.com/olga-terekhova/physicians-availability/blob/main/pic/ontario-lhins-map.png).

Inkscape transformations:
I used vectorisation functionality to convert the map into SVG and cleaned it up so that each shape was assigned an ID with a LHIN code. 

Outcome:
1. SVG map (https://github.com/olga-terekhova/physicians-availability/blob/main/pic/ontario-lhins-map-final.svg)

### 5 - Generating several SVG maps: colored according to the ranking and highlighting current LHIN
Source: 
1. SVG map (https://github.com/olga-terekhova/physicians-availability/blob/main/pic/ontario-lhins-map-final.svg)
2. CSV file with ranking (https://github.com/olga-terekhova/physicians-availability/blob/main/data/df_rank_2020.csv)

Pythone code:
The function generate_png_for_all_current:
1. Iterates through 0 to 14 LHIN codes.
2. For each LHIN code parses the SVG file into a tree using ElementTree library.
3. Collects and iterates through LHIN shapes within the tree.
4. If the code of the LHIN is equal to the code of the current code, then the shape's outline is highlighted with black.
5. The fill color for the shape is generated according to the rank of the corresponding LHIN. 
6. The SVG code from the tree is written into a PNG file. 

Outcome:
1. 15 png files: one for a map with no LHIN selected (https://github.com/olga-terekhova/physicians-availability/blob/main/pic/ontario-lhins-map-gtranked0.png) and 14 files for each LHIN selected as a current one.

### 6 - Showing the end result as a dynamic HTML page
Source:
1. HTML file (https://github.com/olga-terekhova/physicians-availability/blob/main/html/physicians.html)
2. JS files:
2.1. jquery (https://github.com/olga-terekhova/physicians-availability/blob/main/js/jquery-1.10.1.min.js)
2.2. JS file performing an API call to find a LHIN by a postal code (https://github.com/olga-terekhova/physicians-availability/blob/main/js/LHINLookup.js)
2.3. JS file processing a selection of an LHIN on the page (https://github.com/olga-terekhova/physicians-availability/blob/main/js/LHINLookup.js)
3. 15 png files with LHIN maps
4. An existing API at http://healthcareathome.ca that takes a postal code and returns an LHIN code.

