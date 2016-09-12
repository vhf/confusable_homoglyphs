import pickle
import re
import urllib2


def generate():
    # inspired by https://gist.github.com/anonymous/2204527
    code_points_ranges = []
    iso_15924_aliases = []
    categories = []

    match = re.compile(r'([0-9A-F]+)(?:\.\.([0-9A-F]+))?\W+(\w+)\s*#\s*(\w+)',
                       re.UNICODE)

    url = 'http://www.unicode.org/Public/UNIDATA/Scripts.txt'
    file = urllib2.urlopen(url)
    for line in file:
        p = re.findall(match, line)
        if p:
            code_point_range_from, code_point_range_to, alias, category = p[0]
            alias = alias.upper()
            if alias not in iso_15924_aliases:
                iso_15924_aliases.append(alias)
            if category not in categories:
                categories.append(category)
            code_points_ranges.append((
                int(code_point_range_from, 16),
                int(code_point_range_to or code_point_range_from, 16),
                iso_15924_aliases.index(alias), categories.index(category))
            )
    code_points_ranges.sort()

    categories_data = {
        'iso_15924_aliases': iso_15924_aliases,
        'categories': categories,
        'code_points_ranges': code_points_ranges,
    }

    with open('categories.pkl', 'wb') as datafile:
        pickle.dump(categories_data, datafile, 2)
