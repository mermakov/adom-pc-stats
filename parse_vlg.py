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
    print attrs
    attrs = map(lambda(x): (x[0], x[1] / num), attrs)

    return attrs

all_vlgs = []

merchant_specs = {}
items = {}
skill_values = [{},{},{},{}]
skill_modifiers = [{},{},{},{}]
average_gold = 0
gold_by_charisma = {}
gold_by_appearance = {}
stats = {}

for index in range(1, int(sys.argv[2]) + 1):
    try:
        vlg_file = open(prefix + str(index) + ".vlg")
    except IOError:
        continue
    cur_vlg = vlg.Vlg(vlg_file.read())
    all_vlgs.append(cur_vlg)
    for attr in cur_vlg.attributes:
        if attr in stats:
            stats[attr] += 1
        else:
            stats[attr] = 1
#    spec = vlg.merchant_spec_dict[cur_vlg.specialization] - 1
    spec = 0
    for skill in cur_vlg.skills:
        if skill[0] in skill_values[spec]:
            skill_values[spec][skill[0]] = (skill_values[spec][skill[0]][0] + skill[1], skill_values[spec][skill[0]][1] + 1)
        else:
            skill_values[spec][skill[0]] = (skill[1], 1)
        if skill[0] in skill_modifiers[spec]:
            if spec == 0 and skill[0] == 'Literacy':
                print str(skill[1]) + " " + str(index)
            if skill[2] in skill_modifiers[spec][skill[0]]:
                skill_modifiers[spec][skill[0]][skill[2]] += 1
            else:
                skill_modifiers[spec][skill[0]][skill[2]] = 1
        else:
            skill_modifiers[spec][skill[0]] = {}
            skill_modifiers[spec][skill[0]][skill[2]] = 1
    for item in cur_vlg.items:
        if item[0][0] == 'gold piece':
            average_gold += item[1]
            gold = item[1]
    for attribute in cur_vlg.attributes:
        if attribute[0] == 'Ch':
            if attribute[1] in gold_by_charisma:
                gold_by_charisma[attribute[1]] = (gold_by_charisma[attribute[1]][0] + gold, gold_by_charisma[attribute[1]][1] + 1)
            else:
                gold_by_charisma[attribute[1]] = (gold, 1)
        if attribute[0] == 'Ap':
            if attribute[1] in gold_by_appearance:
                gold_by_appearance[attribute[1]] = (gold_by_appearance[attribute[1]][0] + gold, gold_by_appearance[attribute[1]][1] + 1)
            else:
                gold_by_appearance[attribute[1]] = (gold, 1)
        

print get_average_attrs(all_vlgs)
for key in sorted(stats.keys()):
    print str(key) + " "  + str(stats[key])

for x in range(0, 4):
    print vlg.merchant_spec_rdict[x + 1]
    for skill_value in skill_values[x]:
        print skill_value + " " + str(skill_values[x][skill_value][0] / skill_values[x][skill_value][1])
    for skill_modifier in skill_modifiers[x]:
        out = skill_modifier + ": "
    for skill_mod in skill_modifiers[x][skill_modifier]:
        out += skill_mod + " - " + str(skill_modifiers[x][skill_modifier][skill_mod]) + " "
    print out
print average_gold / (int(sys.argv[2]) + 1)
for g in gold_by_charisma:
    print 'Ch:' + str(g) + " - " + str(gold_by_charisma[g][0] / gold_by_charisma[g][1])
for g in gold_by_appearance:
    print 'Ap:' + str(g) + " - " + str(gold_by_appearance[g][0] / gold_by_appearance[g][1])
