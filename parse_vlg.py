import re
import sys
import vlg

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

prefix = sys.argv[1]

def get_average_attrs(vlgs):
    num = 0
    attrs = []
    for vlg in vlgs:
        if attrs == []:
            attrs = vlg.get_base_attributes()
        else:
            attrs = map(lambda x, y: (x[0], x[1] + y[1]), attrs, vlg.get_base_attributes())
        num += 1
    attrs = map(lambda(x): (x[0], x[1] / num), attrs)

    return attrs

all_vlgs = []
young_num = 0
grown_up_num = 0

eye_color = {}
hair_color = {}
complexion = {}
age = {}
corruptions = {}

history_1 = []
history_2 = []

full_corruptions = {}

for index in range(1, int(sys.argv[2])):
    try:
        vlg_file = open(prefix + str(index) + ".vlg")
    except IOError:
        continue
    cur_vlg = vlg.Vlg(vlg_file.read())
    all_vlgs.append(cur_vlg)

    if 6 in cur_vlg.history:
        history_1.append(cur_vlg)
    if 5 in cur_vlg.history:
        history_2.append(cur_vlg)
    if cur_vlg.age_group == "young":
        young_num += 1
    else:
        grown_up_num += 1
    if cur_vlg.age in age:
        age[cur_vlg.age] += 1
    else:
        age[cur_vlg.age] = 1
    if cur_vlg.eye_color in eye_color:
        eye_color[cur_vlg.eye_color] += 1
    else:
        eye_color[cur_vlg.eye_color] = 1
    if cur_vlg.hair_color in hair_color:
        hair_color[cur_vlg.hair_color] += 1
    else:
        hair_color[cur_vlg.hair_color] = 1
    if cur_vlg.complexion in complexion:
        complexion[cur_vlg.complexion] += 1
    else:
        complexion[cur_vlg.complexion] = 1
    for corruption in cur_vlg.corruptions:
        if corruption in corruptions:
            corruptions[corruption] += 1
        else:
            corruptions[corruption] = 1
        if corruption in full_corruptions:
            intern_corr_map = full_corruptions[corruption]
        else:
            intern_corr_map = {}
        for o_corruption in cur_vlg.corruptions:
            if o_corruption == corruption:
                continue
            if o_corruption in intern_corr_map:
                intern_corr_map[o_corruption] += 1
            else:
                intern_corr_map[o_corruption] = 1
        full_corruptions[corruption] = intern_corr_map
print get_average_attrs(all_vlgs)
print str(grown_up_num) + "/" + str(young_num)

#print eye_color
#print hair_color
#print complexion
#print age
#print corruptions
print vlg.int_to_hist(6) + str(get_average_attrs(history_1))
print vlg.int_to_hist(5) + str(get_average_attrs(history_2))
print len(history_1)
print len(history_2)
