from copy import copy
import json

def less_than_5min(string):
    """return time since last access < 5 minutes"""

    if not "secs" in string:
        # So much time has passed that secs are irrelevant
        return False
    
    if not "mins" in string:
        # secs are relevant, but mins are not counted, so I gues it has been less than minute
        return True
    
    # Mins and secs are present. I guess that if hours were present secs would not be shown.
    return 5*60 > string2secs(string)

def string2secs(string):
    """count how many secs is the time in UPEL format
    example string: 12 mins 22 secs
                    1 day 2 hours"""
    #return int(mins)*60 + int(secs)
    secs = 0
    try:
        string = list(map(lambda s: s.strip(), string.split(" ")))
        if "years" in string:
            secs += int(string[0]) * 365 * 24 * 60 * 60
            string = string[2:]
        
        if "days" in string:
            secs += int(string[0]) * 24 * 60 * 60
            string = string[2:]
        
        if "hours" in string:
            secs += int(string[0]) * 60 * 60
            string = string[2:]

        if "mins" in string:
            secs += int(string[0]) * 60
            string = string[2:]
        
        if "secs" in string:
            secs += int(string[0])

        return secs
    except:
        print("string")
        raise ValueError("Couldnt parse string to secs.")


def parse_grades(grades):
    """pass argument 'grades' as soup from BeautifulSoup \n
    return dict"""
    columns = [th.text for th in grades.find("thead").find("tr").find_all("th")]
    parsed_grades = {}
    section = {}
    section_name = ""
    level = 2
    rows = grades.find("tbody").find_all("tr")[1:] # skip the title row (it displays the name of the course above the table)
    while len(rows)>0:
        row = rows.pop(0)
        # check if this is a normal row, or a section title row or a separator row
        if not row.find("td"):
            # it is a <tr></tr>, so skip this element
            continue
        
        level2_count = len(row.find_all(class_="level2"))
        new_level = 2 if level2_count > 0 else 3

        if level2_count == 2 or new_level < level:
            # this is a level2 section title, so a new section is starting from this row forward
            # or we have just left section and are in level2 data rows
            if section_name:
                parsed_grades[section_name] = section.copy()
            
            section = {}
            if not new_level < level:
                section_name = row.find("th").text
                level = new_level
                continue
            
            # this is a level2 data row, we will parse it and not skip it. 

        row_name = row.find("th").text

        tds = row.find_all("td")
        if len(tds)!=len(columns)-1:
            print("DIFFERENT LENGTH! SOMETHING WRONG")
            print(tds)

        row_dict = {}
        for col, val in zip(columns[1:], tds):
            row_dict[col] = val.text

        if level2_count == len(columns):
            # this is a lavel2 row but with normal columns (it is not a section title row)
            parsed_grades[row_name] = row_dict.copy()
        else:
            section[row_name] = row_dict.copy()

        level = new_level

    if section:
        parsed_grades[section_name] = section.copy()
    return parsed_grades
