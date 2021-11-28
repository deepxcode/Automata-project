import itertools

lhs, rhs = 0, 1

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def loadModel(modelPath):
	file = open(modelPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Productions:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Productions:\n")[1])

	return cleanAlphabet(K), cleanAlphabet(V), cleanProduction(P)
#Make production easy to work with
def cleanProduction(expression):
	result = []
	#remove spaces and explode on ";"
	rawRulse = expression.replace('\n','').split(';')
	
	for rule in rawRulse:
		#Explode evry rule on "->" and make a couple
		leftSide = rule.split(' -> ')[0].replace(' ','')
		rightTerms = rule.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

def cleanAlphabet(expression):
	return expression.replace('  ',' ').split(' ')

def seekAndDestroy(target, productions):
	trash, ereased = [],[]
	for production in productions:
		if target in production[rhs] and len(production[rhs]) == 1:
			trash.append(production[lhs])
		else:
			ereased.append(production)
			
	return trash, ereased
 
def setupDict(productions, variables, terms):
	result = {}
	for production in productions:
		#
		if production[lhs] in variables and production[rhs][0] in terms and len(production[rhs]) == 1:
			result[production[rhs][0]] = production[lhs]
	return result


def rewrite(target, production):
	result = []
	#get positions corresponding to the occurrences of target in production rhs side
	#positions = [m.start() for m in re.finditer(target, production[rhs])]
	positions = [i for i,x in enumerate(production[rhs]) if x == target]
	#for all found targets in production
	for i in range(len(positions)+1):
 		#for all combinations of all possible lenght phrases of targets
 		for element in list(itertools.combinations(positions, i)):
 			#Example: if positions is [1 4 6]
 			#now i've got: [] [1] [4] [6] [1 4] [1 6] [4 6] [1 4 6]
 			#erease position corresponding to the target in production rhs side
 			tadan = [production[rhs][i] for i in range(len(production[rhs])) if i not in element]
 			if tadan != []:
 				result.append((production[lhs], tadan))
	return result

def dict2Set(dictionary):
	result = []
	for key in dictionary:
		result.append( (dictionary[key], key) )
	return result

# def print_rules(rules):
# 	for rule in rules:
# 		tot = ""
# 		for term in rule[rhs]:
# 			tot = tot +" "+ term
# 		print(rule[lhs]+" -> "+tot)

def print_rules(rules):
	dictionary = {}
	for rule in rules:
		if rule[lhs] in dictionary:
			dictionary[rule[lhs]] += ' | '+' '.join(rule[rhs])
		else:
			dictionary[rule[lhs]] = ' '.join(rule[rhs])
	result = ""
	for key in dictionary:
		result += key+" -> "+dictionary[key]+"\n"
	return result