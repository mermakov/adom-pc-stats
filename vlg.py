import re

starsign_dict = {
	'Raven':		1,
	'Book':			2,
	'Wand':			3,
	'Unicorn':		4,
	'Salamander':	5,
	'Dragon':		6,
	'Sword':		7,
	'Falcon':		8,
	'Cup':			9,
	'Candle':		10,
	'Wolf':			11,
	'Tree':			12
}

starsign_attr_modifier_rules = {
	'Raven':		{ 'Pe':2 },
	'Book':			{},
	'Wand':			{ 'Ch':2 },
	'Unicorn':		{ 'Ap':2 },
	'Salamander':	{ 'Ch':1, 'Ma':3 },
	'Dragon':		{ 'To':1, 'St':2, 'Wi':-3 },
	'Sword':		{ 'Le':1 },
	'Falcon':		{ 'Wi':2, 'Ch':1 },
	'Cup':			{ 'Le':2 },
	'Candle':		{},
	'Wolf':			{ 'Wi':3 },
	'Tree':			{ 'Wi':5 }
}

gender_attr_modifier_rules = {
	'male':			{ 'St':1 },
	'female':		{ 'Dx':1 }
}

age_attr_modifier_rules = {
	'grown-up':		{ 'St':1, 'Wi':2, 'Le':2 },
	'young':		{}
}

def apply_attr_modifier_rule(attribute, rule):
	return (attribute[0], - rule.get(attribute[0], 0) + attribute[1])
	

starsign_pattern_s = ""
for starsign in starsign_dict.keys():
	starsign_pattern_s += "|" + starsign

starsign_pattern = re.compile(starsign_pattern_s[1:])
skill_pattern = re.compile(r"[a-zA-Z ]* \.* [ \d]\d\s*\([a-z]*\)\s*\[\+[0-9d]*\]")
skill_parse_pattern = re.compile(r"([A-Z][a-zA-Z ]*[a-z])[ \.]*([0-9]+).*\[(.*)\]")
attribute_pattern = re.compile(r"[A-Z][a-z]:[ 0-9][0-9](?= )")
attribute_parse_pattern = re.compile(r"(Le|St|Wi|Dx|To|Ap|Ch|Ma|Pe)\:([ 0-9]*)")

alignment_pattern = re.compile(r"(?<=Pe:[ 0-9]{4})[LCN]")
gender_pattern = re.compile(r"(?<=Race: )[a-z]*")

age_pattern = re.compile(r"(?<=Age:).*")
age_parse_pattern = re.compile(r"(?<=\().*(?=\))")

starsign_rdict = {
	1:	'Raven',
	2:	'Book',
	3:	'Wand',
	4:	'Unicorn',
	5:	'Salamander',
	6:	'Dragon',
	7:	'Sword',
	8:	'Falcon',
	9:	'Cup',
	10:	'Candle',
	11:	'Wolf',
	12:	'Tree'
}

history_dict = {
	'lower class':		1,
	'moderately well':	2,
	'is a guildmaster':	3,
	'humble shepherd':	4,
	'to the nobility':	5,
	'the middle class':	6,
	'Both are compet':	7,
	'were poor people':	8,
	'were often alone':	11,
	'ever-declining':	12,
	'cared a lot for':	13,
	'through happy':	14,
	'enjoyed your pre':	15,
	'everchanging':		16,
	'of your uncles':	17,
	'cruel parents':	18,
	'seriously ill':	21,
	'were very lazy':	22,
	'watched the adul':	23,
	'very active kid':	24,
	'center of inter':	25,
	'exploring woods':	26,
	'embarked on many':	27,
	'become rich and':	28,
	'left your home':	31,
	'renowned master':	32,
	'deeper meaning':	33,
	'with all means':	34,
	'clearly lying':	35,
	'steady determ':	36,
	'many occupations':	37,
	'a lot to finance':	38
}
	

history_rdict = {
	1:	'lower class',
	2:	'are travelling',
	3:	'is a guildmaster',
	4:	'humble shepherd',
	5:	'to the nobility',
	6:	'the middle class',
	7:	'Both are compet',
	8:	'were poor people',
	11:	'were often alone',
	12:	'ever-declining',
	13:	'cared a lot for',
	14:	'through happy',
	15:	'enjoyed your pre',
	16:	'everchanging',
	17:	'of your uncles',
	18:	'cruel parents',
	21:	'seriously ill',
	22:	'were very lazy',
	23:	'watched the adul',
	24:	'very active kid',
	25:	'center of inter',
	26:	'exploring woods',
	27:	'embarked on many',
	28:	'become rich and',
	31:	'left your home',
	32:	'renowned master',
	33:	'deeper meaning',
	34:	'with all means',
	35:	'clearly lying',
	36:	'steady determ',
	37:	'many occupations',
	38:	'a lot of finance'
}

history_pattern_s = ""
for history in history_dict.keys():
	history_pattern_s += "|" + history.replace(" ", "\s*")

history_pattern = re.compile(history_pattern_s[1:], )

def ss_to_int(starsign):
	return starsign_dict[starsign]

def int_to_ss(starsign):
	return starsign_rdict[starsign]

def hist_to_int(history):
	return history_dict[re.sub("\s+", " ", history)]

def int_to_hist(history):
	return history_rdict[history]

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
		if not attr in result:
			result.append(attr)
	return result




class Vlg:

	def __init__(self,contents):
		self.starsign = re.search(starsign_pattern, contents).group(0)
		self.skills = parse_skills(contents)
		self.attributes = parse_attributes(contents)
		self.alignment = re.search(alignment_pattern, contents).group(0)
		age = re.search(age_pattern, contents).group(0)
		self.age = re.search(age_parse_pattern, age).group(0)
		self.gender = re.search(gender_pattern, contents).group(0)
		self.history = []
		for history in re.findall(history_pattern, contents):
			self.history.append(hist_to_int(history))

	def get_base_attributes(self):
		result = []
		for attribute in self.attributes:
			attr = apply_attr_modifier_rule(attribute,
											starsign_attr_modifier_rules[self.starsign])
			attr = apply_attr_modifier_rule(attr, age_attr_modifier_rules[self.age])
			attr = apply_attr_modifier_rule(attr, gender_attr_modifier_rules[self.gender])
			result.append(attr)

		return result	
