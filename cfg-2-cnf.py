import sys, organizer

lhs, rhs = 0, 1

K, V, Productions = [],[],[]
variablesJar = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]


def isUnitary(rule, variables):
	if rule[lhs] in variables and rule[rhs][0] in variables and len(rule[rhs]) == 1:
		return True
	return False

def isSimple(rule):
	if rule[lhs] in V and rule[rhs][0] in K and len(rule[rhs]) == 1:
		return True
	return False


for nonTerminal in V:
	if nonTerminal in variablesJar:
		variablesJar.remove(nonTerminal)

#Add S0->S rule
def begin(productions, variables):
	variables.append('S0')
	return [('S0', [variables[0]])] + productions

#Removing rules that contain both terminal and non terminal together
def replace_terminals(productions, variables):
	newProductions = []
	#create a dictionary for all base production
	dictionary = organizer.setupDict(productions, variables, terms=K)
	for production in productions:
		#check if the production is simple
		if isSimple(production):
			#in that case there is nothing to change
			newProductions.append(production)
		else:
			for term in K:
				for index, value in enumerate(production[rhs]):
					if term == value and not term in dictionary:
						#it's created a new production vaiable->term and added to it 
						dictionary[term] = variablesJar.pop()
						#Variables set it's updated adding new variable
						V.append(dictionary[term])
						newProductions.append( (dictionary[term], [term]) )
						
						production[rhs][index] = dictionary[term]
					elif term == value:
						production[rhs][index] = dictionary[term]
			newProductions.append( (production[lhs], production[rhs]) )
			
	#merge created set and the introduced rules
	return newProductions

#Eliminate non unitry rules
def remove_nonterminals(productions, variables):
	result = []
	for production in productions:
		k = len(production[rhs])
		if k <= 2:
			result.append( production )
		else:
			newVar = variablesJar.pop(0)
			variables.append(newVar+'1')
			result.append( (production[lhs], [production[rhs][0]]+[newVar+'1']) )
			i = 1
#TODO
			for i in range(1, k-2 ):
				var, var2 = newVar+str(i), newVar+str(i+1)
				variables.append(var2)
				result.append( (var, [production[rhs][i], var2]) )
			result.append( (newVar+str(k-2), production[rhs][k-2:k]) ) 
	return result
	

#Delete non terminal rules
def remove_nullprod(productions):
	newSet = []
	outlaws, productions = organizer.seekAndDestroy(target='e', productions=productions)
	for outlaw in outlaws:
		#consider every production: old + new resulting important when more than one outlaws are in the same prod.
		for production in productions + [e for e in newSet if e not in productions]:
			if outlaw in production[rhs]:
				#the rule is rewrited in all combination of it, rewriting "e" rather than outlaw
				newSet = newSet + [e for e in  organizer.rewrite(outlaw, production) if e not in newSet]
				for i in newSet:
					if len(i[rhs]) == 1:
						if (i[rhs][0] == outlaw):
							i[rhs][0] = 'e'						

	#add unchanged rules and return
	newSet= newSet + ([productions[i] for i in range(len(productions)) 
							if productions[i] not in newSet])
	return newSet

def unit_routine(rules, variables):
	unitaries, result = [], []

	for aRule in rules:
		if isUnitary(aRule, variables):
			unitaries.append( (aRule[lhs], aRule[rhs][0]) )
		else:
			result.append(aRule)

	for uni in unitaries:
		for rule in rules:
			if uni[rhs]==rule[lhs] and uni[lhs]!=rule[lhs]:
				result.append( (uni[lhs],rule[rhs]) )
	
	return result

def remove_unitprod(productions, variables):
	i = 0
	result = unit_routine(productions, variables)
	tmp = unit_routine(result, variables)
	while result != tmp and i < 1000:
		result = unit_routine(tmp, variables)
		tmp = unit_routine(result, variables)
		i+=1
	return result


if __name__ == '__main__':
	if len(sys.argv) > 1:	
		modelPath = str(sys.argv[1])
	else:
		modelPath = 'model.txt'
	
	K, V, Productions = organizer.loadModel( modelPath )

	for i in Productions:
		if "" in i[1]:
			i[1].remove("")
	
	print("add start function")
	Productions = begin(Productions, variables=V)
	print( organizer.print_rules(Productions) )
	
	print("remove terminals from rightside")
	Productions = replace_terminals(Productions, variables=V)
	print( organizer.print_rules(Productions) )
	
	print("remove more than 2")
	Productions = remove_nonterminals(Productions, variables=V)
	print( organizer.print_rules(Productions) )
	
	c=[]	
	
	for i in Productions:
		c+=i[1]		
	while 'e' in c:
		print("remove NULL productions")	
		Productions = remove_nullprod(Productions)
		print( organizer.print_rules(Productions) )
		c=[]
		for i in Productions:
			c+=i[1]		

	
	print("remove UNIT production")
	Productions = remove_unitprod(Productions, variables=V)
	new_productions=[]
	for i in Productions:
		if i not in new_productions:
			new_productions.append(i)
	print( organizer.print_rules(new_productions) )
	# print( len(new_productions) )
	# open('out.txt', 'w').write(	organizer.print_rules(Productions) )