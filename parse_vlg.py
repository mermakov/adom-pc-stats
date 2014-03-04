import re
import sys
import vlg
import argparse

def parse_skills(contents):
    result = []
    skills = re.findall(skill_pattern, contents)
    for skill in skills:
        skill_mo = re.search(skill_parse_pattern, skill)
        result.append((skill_mo.group(1), int(skill_mo.group(2))))
    return result


def parse_attributes(contents):
    result = []
    for attribute in re.findall(attribute_pattern, contents):
        attribute_mo = re.search(attribute_parse_pattern, attribute)
        attr = (attribute_mo.group(1), int(attribute_mo.group(2)))
        result.append(attr)

    return result

def merge_skill_lists(skills1, skills2):
    result = []
    for skill1 in skills1:
        found = False
        for skill2 in skills2:
            if skill1[0] == skill2[0]:
                result.append((skill1[0], skill1[1] + skill2[1]))
                found = True
                break
        if found == False:
            result.append(skill1)

    for skill2 in skills2:
        found = False
        for skill1 in skills2:
            if skill1[0] == skill2[0]:
                found = True
                break
        if found == False:
            result.append(skill2)

    return result

def get_average_attrs(vlgs):
    num = 0
    attrs = []
    for vlg in vlgs:
        if attrs == []:
            attrs = vlg.get_base_attributes()
        else:
            attrs = map(lambda x, y: (x[0], x[1] + y[1]), attrs, vlg.get_base_attributes())
        num += 1
    print attrs
    attrs = map(lambda(x): (x[0], int(round(float(x[1]) / float(num)))), attrs)

    return attrs

all_vlgs = []

items = {}
items_extended = {}
skill_values = [{},{},{},{}]
skill_modifiers = [{},{},{},{}]
stats = {}
young = 0
grown_up = 0
num = 0
parser = argparse.ArgumentParser()
parser.add_argument("-dir", nargs="+", dest="dirs")
parser.add_argument("-n", type=int, dest="num")
opts = parser.parse_args(sys.argv[1:])

for vlg_dir in opts.dirs:
    for index in range(1, opts.num + 1):
        try:
            vlg_file = open(vlg_dir + "/" + str(index) + ".vlg")
        except IOError:
            continue
        cur_vlg = vlg.Vlg(vlg_file.read())
        if cur_vlg.age_group == 'young':
            young += 1
        else:
            grown_up += 1 
        all_vlgs.append(cur_vlg)
        for attr in cur_vlg.attributes:
            if attr in stats:
                stats[attr] += 1
            else:
                stats[attr] = 1
        local_items = {}
        for item in cur_vlg.items:
            base_name = item[0]
            item_n = cur_vlg.items[item]
            if base_name in items:
                items[base_name] += item_n
            else:
                items[base_name] = item_n
            if base_name in local_items:
                local_items[base_name] += item_n
            else:
                local_items[base_name] = item_n
        for local_item in local_items:
            if (local_item, local_items[local_item]) in items_extended:
                items_extended[(local_item, local_items[local_item])] += 1
            else:
                items_extended[(local_item, local_items[local_item])] = 1
        num += 1

print get_average_attrs(all_vlgs)
for key in items:
    print key + ': ' + str(int(round(float(items[key]) / float(num))))
for key in items_extended:
    if key[0] == 'gold piece':
        continue
    print str(key) + ': ' + str(items_extended[key])
print 'young: ' + str(young)
print 'grown-up: ' + str(grown_up)
