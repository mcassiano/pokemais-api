from pulp import LpVariable, LpMinimize, LpMaximize, LpProblem, LpStatus, value, lpSum

def parseRequestBody(bodyString):

	parsedJson = bodyString

	function = parsedJson['function']
	constraints = parsedJson['restrictions']

	objective = LpMaximize
	op = LpMaximize if function['operation'].upper() == 'MAX' else LpMinimize
	problem = LpProblem("Problem", objective)
	function_coefficients = function['coefficients']

	problem_vars = [LpVariable("x" + str(x+1), 0, cat = "Integer") for x in range(0, len(function_coefficients))]

	problem += lpSum([function_coefficients[i] * problem_vars[i] for i in range(0, len(function_coefficients))])

	for restriction in constraints:

		coefficients = restriction['coefficients']
		sense = restriction['type']
		bound = restriction['value']

		if sense.upper() == 'LT':
			problem += lpSum([problem_vars[i] * coefficients[i] for i in range(0, len(coefficients))]) <= bound
		elif sense.upper() == 'EQ':
			problem += lpSum([problem_vars[i] * coefficients[i] for i in range(0, len(coefficients))]) == bound
		elif sense.upper() == 'GT':
			problem += lpSum([problem_vars[i] * coefficients[i] for i in range(0, len(coefficients))]) >= bound


	status = problem.solve()

	response = {
		'status': LpStatus[status].upper(),
		'values': [value(problem.objective)] + [value(var) for var in problem_vars]
	}

	return response