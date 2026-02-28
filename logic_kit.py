from sympy import logic
import re

def simplify(expr):
  expr = format(expr)
  return logic.simplify_logic(expr)


def remove_spaces(expr):
  expr = expr.split(' ')
  return ''.join(expr)


def remove_dublicate_negs(expr):
  return expr.replace('~~', '')


def separate_operands(expr):
  seq_found = re.search(r"~{0,}[A-z]~{0,}[A-z]", expr)
  while seq_found:
    pat = seq_found.group(0)
    splitted = [x for x in pat]
    a = splitted[0] 
    b = ""
    for i in range(1, len(splitted)):
      if (a[-1] != '~'):
        b += splitted[i]
      else: 
        a += splitted[i]
    expr = expr.replace(pat, f"{a}&{b}", 1)
    seq_found = re.search(r"~{0,}[A-z]~{0,}[A-z]", expr)
  return expr


def replace_operator(operator, rep, expr):
  op_found = re.search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  while op_found:
    pat = op_found.group(0)
    operands = pat.split(operator)
    expr = expr.replace(pat, f"{rep}({operands[0]}, {operands[1]})", 1)
    op_found = re.search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  return expr


def format(expr):
  expr = remove_spaces(expr)
  expr = remove_dublicate_negs(expr)
  expr = separate_operands(expr)

  # Important to save the operators order to keep it correct
  expr = replace_operator('=', "Equivalent", expr)
  expr = replace_operator('>', "Implies", expr)
  expr = replace_operator('!', "Nor", expr)
  expr = replace_operator('/', "Nand", expr)
  expr = replace_operator('+', "Xor", expr)

  return expr

if __name__ == "__main__":
  print(f"""
    +--------+------------+--------+------------+
    | Symbol | Operation  | Symbol | Operation  |   Note that:
    +--------+------------+--------+------------+   ab = a & b
    |   &    |    AND     |   !    |    NOR     |   
    +--------+------------+--------+------------+  
    |   |    |    OR      |   /    |    NAND    |
    +--------+------------+--------+------------+  
    |   +    |    XOR     |   >    |  IMPLIES   |
    +--------+------------+--------+------------+  
    |   =    | EQUIVALENT |   ~    |    NOT     |
    +--------+------------+--------+------------+                      
  """)

  expr = ""
  while (expr != "exit"):
    print("Input your logic expression:")
    expr = input(">>> ")
    if (expr == "exit"): break
    print(f"""
      {simplify(expr)}
    """)


