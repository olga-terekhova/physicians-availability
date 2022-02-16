
import tabula
import pandas
import xml.etree.ElementTree as ET
import re



def extract_table(filepath, df_values_name):
    tables = tabula.read_pdf(filepath,pages = "45-46", multiple_tables = True)

    #keeping only relevant records
    tables[0] = tables[0].iloc[8:92, :]
    tables[0] = tables[0].reset_index(drop = True)
    tables[1] = tables[1].iloc[7:91, :]
    tables[1] = tables[1].reset_index(drop = True)

    #merging tables from the two pages together but dropping row labels from the second one
    merged_table = pandas.concat([tables[0],tables[1].iloc[:,1:]], axis = 1)

    #starting to create the final table with the row labels
    newdf = merged_table.iloc[:,0]

    #for each column in the merged table split it by space as delimiter and append to the final table
    for x in range(len(merged_table.iloc[:,1:].columns)):
        splitdf = merged_table.iloc[:, x+1].str.split(' ', 0, expand=True)
        newdf = pandas.concat([newdf,splitdf], axis = 1)

    #assign labels to columns
    labels_list = ['Specialty of Practice',
                   'Erie St. Clair - Physician Count',
                   'Erie St. Clair - Phys per 100,000 Population',
                   'South West - Physician Count',
                   'South West - Phys per 100,000 Population',
                   'Waterloo Wellington - Physician Count',
                   'Waterloo Wellington - Phys per 100,000 Population',
                   'Hamilton Niagara Haldimand Brant - Physician Count',
                   'Hamilton Niagara Haldimand Brant - Phys per 100,000 Population',
                   'Central West - Physician Count',
                   'Central West - Phys per 100,000 Population',
                   'Mississauga Halton - Physician Count',
                   'Mississauga Halton - Phys per 100,000 Population',
                   'Toronto Central - Physician Count',
                   'Toronto Central - Phys per 100,000 Population',
                   'Central - Physician Count',
                   'Central - Phys per 100,000 Population',
                   'Central East - Physician Count',
                   'Central East - Phys per 100,000 Population',
                   'South East - Physician Count',
                   'South East - Phys per 100,000 Population',
                   'Champlain - Physician Count',
                   'Champlain - Phys per 100,000 Population',
                   'North Simcoe Muskoka - Physician Count',
                   'North Simcoe Muskoka - Phys per 100,000 Population',
                   'North East - Physician Count',
                   'North East - Phys per 100,000 Population',
                   'North West - Physician Count',
                   'North West - Phys per 100,000 Population',
                   'Grand Total - Physician Count',
                   'Grand Total - Phys per 100,000 Population'
]
    newdf = newdf.set_axis(labels_list, axis = 1, inplace = False)
    newdf.to_csv('../data/'+ df_values_name+'.csv', index=False)

def assign_color_LHIN(LHIN_series, min_series, max_series):
    s_color =  (LHIN_series - min_series) / (max_series - min_series)
    s_color.name = LHIN_series.name[0:LHIN_series.name.find(' - '):] + ' - Rank'
    return s_color

def assign_rank(df, df_rank_name):
    pop_list = [i for i in df.columns if "Phys per 100,000 Population" in i]
    df_pop_list = df[pop_list]
    df_min = df_pop_list.min(axis = 1)
    df_max = df_pop_list.max(axis = 1)
    df_pop_list = pandas.concat([df_pop_list,df_min.rename('Min')], axis = 1)
    df_pop_list = pandas.concat([df_pop_list,df_max.rename('Max')], axis = 1)

    for x in df_pop_list:
        if "Phys per 100,000 Population" in x:
            new_rank = assign_color_LHIN(df_pop_list[x], df_pop_list['Min'], df_pop_list['Max'])
            df_pop_list = pandas.concat([df_pop_list, new_rank], axis=1)

    rank_list = [i for i in df_pop_list.columns if " - Rank" in i]
    df = pandas.concat([df.iloc[:,0],df_pop_list[rank_list]], axis=1)
    df.to_csv('../data/'+ df_rank_name + '.csv', index=False)

def generate_hex_from_rank(h,s,rank):
    import colorsys
    l = int((1 - rank/2) * 100)
    rgb = colorsys.hls_to_rgb(h/360, l/100, s/100)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    rgb_str = str(r)+' '+ str(g) + ' ' + str(b)
    hex_str = '#%02x%02x%02x' % (r, g, b)
    return hex_str

def generate_hsl_from_rank(rank):
    l = int((1 - rank/2) * 100)
    return l

def generate_html_table(df_values, df_rank):
    head = ('<table style="width:100%;text-align:left;border-collapse: collapse;">\n')
    tr1 = '<tr>\n'
    for x in df_values.columns:
        if 'Specialty of Practice' in x:
            border_style ='border-top:solid;border-bottom:solid;border-right:solid;'
            tr1 = tr1 + '<th style = "' + border_style + '" rowspan = "2">' + x + '</th>\n'
        elif 'Physician Count' in x:
            border_style = 'border-top:solid;border-bottom:solid;border-right:solid'
            tr1 = tr1 + '<th style = "' + border_style + '" colspan = "2">' + x[0:x.find(' - '):] + '</th>\n'
    tr1 = tr1 + '</tr>\n'
    tr = '<tr>\n'
    for x in df_values.columns:
        if 'Physician Count' in x:
            border_style = 'border-top:solid;border-bottom:solid;border-left: solid;border-right:1px solid #777777;'
            tr = tr + '<th style = "' + border_style + '">' + x[x.find(' - ')+3:] + '</th>\n'
        elif 'Phys per 100,000 Population' in x:
            border_style = 'border-top:solid;border-bottom:solid;border-right: solid;'
            tr = tr + '<th style = "' + border_style + '">' + x[x.find(' - ')+3:] + '</th>\n'
        else:
            border_style = 'border-top:solid;border-bottom:solid;'

    tr = tr + '</tr>\n'
    tr_v = ''
    for rowIndex, row in df_values.iterrows():
        total = False
        tr_v = tr_v + '<tr style="border-bottom: 1px solid #777777 ">\n'
        for columnIndex, value in row.items():
            curr_row = rowIndex
            if ' - ' in columnIndex:
                rank_col_name = columnIndex[0:columnIndex.find(' - '):]+ ' - Rank'
                rank = df_rank[rank_col_name][curr_row]
                color = generate_hsl_from_rank(rank)
            else:
                color = generate_hsl_from_rank(0)
            if 'Physician Count' in columnIndex:
                border_style = 'border-left: solid;border-right:1px solid #777777;'
            elif 'Phys per 100,000 Population' in columnIndex:
                border_style = 'border-right: solid;border-left:1px solid #777777;'
            else:
                border_style = ''
            if 'Specialty of Practice' in columnIndex:
                if 'Total' in value:
                    total = True
                    font = ''
                else:
                    font = 'padding-left:5px;'
            else:
                font = ''
            if total is True:
                total_style = 'font-weight:bold;border-bottom: 2px solid;'
            else:
                total_style = ''
            tr_v = tr_v + '<td style="background-color:hsl(120, 50%, ' + str(color) + '%);'+ border_style+font+total_style+'">' \
                   + str(value) + '</td>\n'
        tr_v = tr_v + '</tr>\n'
    trail = ('</table>\n')

    html_table = head + tr1 + tr + tr_v + trail
    file_src = open('../html/physicians_src.html','r')
    html_src = file_src.read()
    html_trg = html_src.replace('<table></table>',html_table)

    file_src.close()
    file = open('../html/physicians.html','w')
    file.write(html_trg)
    file.close()

def getLHIN_number(svg_name):
    if 'LHIN' in svg_name:
        if svg_name.find('_') < 0:
            LHIN_number = int(svg_name[4:])
        else:
            LHIN_number = int(svg_name[4:svg_name.find('_'):])
    else:
        LHIN_number = 0
    return LHIN_number

def get_label_of_element(element):
    if "{http://www.inkscape.org/namespaces/inkscape}label" in element.attrib:
        return element.attrib["{http://www.inkscape.org/namespaces/inkscape}label"]
    else:
        return ''

def path_is_LHIN(element):
    if 'LHIN' in get_label_of_element(element):
        return True
    else:
        return False

def get_grand_total_rank_series(df_rank):
    df_grand_total_rank = df_rank.loc[df_rank['Specialty of Practice'] == 'Grand Total']
    df_grand_total_rank = df_grand_total_rank.iloc[:,1:15]
    #print(df_grand_total_rank)
    return df_grand_total_rank

def get_rank_of_lhin_element(element, df_series_rank):
    return df_series_rank.iloc[0, getLHIN_number(get_label_of_element(element)) - 1]

def get_rank_by_lhin_number(number,df_series_rank):
    return df_series_rank.iloc[0,number - 1]


def replace_fill_color(line, hex):
    #line = 'style="fill:#40bf40;fill-opacity:1;stroke:#000000;stroke-opacity:1"'
    line_pos = line.find('fill:#')+6
    #print(line)
    #print(line[line_pos:line_pos+6])
    new_line = line[0:line_pos-1] + hex + line[line_pos+6:]
    return new_line

def replace_stroke_color(line, hex):
    #line = 'style="fill:#40bf40;fill-opacity:1;stroke:#000000;stroke-opacity:1"'
    line_pos = line.find('stroke:#')+8
    #print(line)
    #print(line[line_pos:line_pos+6])
    new_line = line[0:line_pos-1] + hex + line[line_pos+6:]
    return new_line

def process_svg(current,df_rank):
    from cairosvg import svg2png

    tree = ET.parse('../pic/ontario-lhins-map-final.svg')
    root = tree.getroot()
    all_elements = list(tree.iter('{http://www.w3.org/2000/svg}path'))

    df_grant_total_rank = get_grand_total_rank_series(df_rank)
    for element in all_elements:
        if path_is_LHIN(element):
            #check whether is current -> update border
            if getLHIN_number(get_label_of_element(element)) == current:
                element.attrib["style"] = replace_stroke_color(element.attrib["style"],'#000000')
            else:
                element.attrib["style"] = replace_stroke_color(element.attrib["style"], '#999999')
            #assign rank -> fill color:
            l = get_rank_of_lhin_element(element,df_grant_total_rank)
            hex = generate_hex_from_rank(120,50,l)
            element.attrib["style"] = replace_fill_color(element.attrib["style"],hex)
    tree_bytes = ET.tostring(root, encoding='utf8', method='xml')
    svg2png(bytestring=tree_bytes, write_to='../pic/ontario-lhins-map-gtranked'+str(current)+'.png')
    #tree.write('../pic/ontario-lhins-map-gtranked.svg')


def generate_png_for_all_current(df_rank):
    for i in range(15):
        process_svg(i, df_rank)

# Main

filepath = '../data/2020-PIO-Annual-Report.pdf'
df_values_name = 'df_values_2020'
df_rank_name = 'df_rank_2020'



#extract_table(filepath,df_values_name)
#df = pandas.read_csv('../data/' + df_values_name + '.csv')
#assign_rank (df, df_rank_name)
df_rank = pandas.read_csv('../data/' + df_rank_name + '.csv')
#generate_html_table(df,df_rank)


generate_png_for_all_current(df_rank)


