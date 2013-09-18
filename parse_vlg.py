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

for index in range(1, int(sys.argv[2])):
	try:
		vlg_file = open(prefix + str(index) + ".vlg")
	except IOError:
		continue
	cur_vlg = vlg.Vlg(vlg_file.read())
	all_vlgs.append(cur_vlg)
	if cur_vlg.age == "young":
		young_num += 1
	else:
		grown_up_num += 1

print get_average_attrs(all_vlgs)
print str(grown_up_num) + "/" + str(young_num)
