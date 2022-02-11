def pretty(d, indent=0):
    s = ""
    for key, value in d.items():
        s += "\n" + ('\t' * indent + str(key))
        if isinstance(value, dict):
            s += pretty(value, indent+1)
        else:
            if value == "-":
                s += ": -"
            else:
                s += (': \t' + str(value))
    return s

d = {
    "kolokwium zal": {
        "Calculated weight": "-",
        "Grade": "15.00",
        "Range": "0\u201320",
        "Percentage": "75.00 %",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "kolokwium zal popr": {
        "Calculated weight": "-",
        "Grade": "-",
        "Range": "0\u201320",
        "Percentage": "-",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "aktywno\u015b\u0107 1": {
        "Calculated weight": "-",
        "Grade": "4.00",
        "Range": "0\u20134",
        "Percentage": "100.00 %",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "aktywno\u015b\u0107 2 ": {
        "Calculated weight": "-",
        "Grade": "-",
        "Range": "0\u20134",
        "Percentage": "-",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "aktywno\u015b\u0107 3": {
        "Calculated weight": "-",
        "Grade": "-",
        "Range": "0\u20134",
        "Percentage": "-",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "aktywno\u015b\u0107 5": {
        "Calculated weight": "-",
        "Grade": "-",
        "Range": "0\u20134",
        "Percentage": "-",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "aktywno\u015bc 6": {
        "Calculated weight": "-",
        "Grade": "4.00",
        "Range": "0\u20134",
        "Percentage": "100.00 %",
        "Feedback": "\u00a0",
        "Contribution to course total": "-"
    },
    "": {
        "Course totalSimple weighted mean of grades.": {
            "Calculated weight": "-",
            "Grade": "-",
            "Range": "0\u2013100",
            "Percentage": "-",
            "Feedback": "\u00a0",
            "Contribution to course total": "-"
        }
    }
}

print(pretty(d))