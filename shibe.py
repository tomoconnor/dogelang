import re

virtual = {}

def declaration(scanner, token):
	varname = scanner.match.group(2)
	value = scanner.match.group(3)
	virtual[varname] = value
	return "DECLARE", varname, value

def equality(scanner, token):
	return "EQUALITY", scanner.match.group(1), scanner.match.group(2), scanner.match.group(3)

def simpleMath(op, val1, val2):
	real1 = 0
	real2 = 0
	type1 = type(val1)
	type2 = type(val2)
	if type1 in [int,float]:
		real1 = val1
	if type2 in [int,float]:
		real2 = val2
	if type1 == str:
		if val1 in virtual: # it's a variable
			real1 = virtual[val1]
		elif '.' in val1: #its' a decimal
			real1 = float(val1)
		elif '.' not in val1: #its an int.
			real1 = int(val1)

	if type2 == str:
		if val2 in virtual:
			real2 = virtual[val2]
		elif '.' in val1:
			real2 = float(val2)
		elif '.' not in val1:
			real2 = int(val2)

	if op == '+':
		return float(real1) + float(real2)
	elif op == '-':
		print type(real1), type(real2)
		print real1,real2
		return float(real1) - float(real2)
	elif op == '/':
		if float(real2) == 0:
			return 0.0
		else:
			return float(real1) / float(real2)
	elif op == "*":
		return float(real1) * float(real2)

def addition(scanner, token):
	result_varname = scanner.match.group(1)
	operand_1 = scanner.match.group(2)
	operand_2 = scanner.match.group(3)
	virtual[result_varname] = simpleMath('+', operand_1, operand_2)
	return "EQADD", result_varname, operand_1, operand_2

def subtraction(scanner,token):
	result_varname = scanner.match.group(1)
	operand_1 = scanner.match.group(2)
	operand_2 = scanner.match.group(3)
	virtual[result_varname] = simpleMath('-', operand_1, operand_2)
	return "EQSUB", result_varname, operand_1, operand_2

def multiplication(scanner,token):
	result_varname = scanner.match.group(1)
	operand_1 = scanner.match.group(2)
	operand_2 = scanner.match.group(3)
	virtual[result_varname] = simpleMath('*', operand_1, operand_2)
	return "EQMUL", result_varname, operand_1, operand_2

def division(scanner,token):
	result_varname = scanner.match.group(1)
	operand_1 = scanner.match.group(2)
	operand_2 = scanner.match.group(3)
	virtual[result_varname] = simpleMath('/', operand_1, operand_2)
	return "EQDIV", result_varname, operand_1, operand_2

def increment(scanner, token):
	return "INCREMENT", scanner.match.group(1)
def digit(scanner, token):
	return "DIGIT", token
def end_stmnt(scanner, token):
	return "END"
def start_stmnt(scanner, token):
	return "BEGIN"
def printer(scanner,token):
	variable_name = scanner.match.group(1)
	return "PRINT", variable_name

scanner = re.Scanner([
    (r"so\s+((\w+))\s+much\s(.+)", declaration),
    (r"very\s+(\w+)", increment),
    (r"nice\s+(\w+)\s+very\s+(.+)\s+very\s+(.+)", addition),
    (r"bad\s+(\w+)\s+very\s+(.+)\s+very\s+(.+)", subtraction),
    (r"much\s+(\w+)\s+very\s+(.+)\s+very\s+(.+)", multiplication),
    (r"few\s+(\w+)\s+very\s+(.+)\s+very\s+(.+)", division),
    (r"amaze\s+(.+)", printer),
    (r"wow", end_stmnt),
    (r"many codes", start_stmnt),
    (r"\s+", None),
    ])

sample_program = """
many codes
so x much 50
so y much 6
so a much 3.14
so b much -42
very x
nice z very x very y
nice p very 60 very 9
bad f very x very y
bad g very 60 very 9
much f very x very y
much g very 60 very 9
much t very a very b
few f very x very y
few g very 60 very 9
amaze z
amaze y
amaze x
wow
"""

tokens, remainder = scanner.scan(sample_program)
for token in tokens:
    print token

print virtual