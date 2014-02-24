import re

virtual = {}
def declaration(scanner, token):
	varname = scanner.match.group(2)
	value = scanner.match.group(3)
	return "DECLARE", varname, value

def equality(scanner, token):
	return "EQUALITY", scanner.match.group(1), scanner.match.group(2), scanner.match.group(3)

def addition(scanner, token):
	result_varname = scanner.match.group(1)
	operand_1 = scanner.match.group(2)
	operand_2 = scanner.match.group(3)
	return "EQADD", result_varname, operand_1, operand_2

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
    (r"so\s+((\w+))\s+much\s(\d+)", declaration),
    (r"very\s+(\w+)", increment),
    (r"(\w+)\s+nice\s+(\w+)\s+very\s+(\w+)",equality),
    (r"nice\s+(\w+)\s+very\s+(\w+)\s+very\s+(\w)", addition),
    (r"[0-9]+(\.[0-9]+)?", digit),
    (r"amaze\s+(\w+)", printer),
    (r"wow", end_stmnt),
    (r"many codes", start_stmnt),
    (r"\s+", None),
    ])

sample_program = """
many codes
so x much 50
so y much 6
very x
nice z very x very y
nice p very 60 very 9
amaze z
amaze y
amaze x
wow
"""

tokens, remainder = scanner.scan(sample_program)
for token in tokens:
    print token