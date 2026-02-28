from sympy import to_dnf, simplify_logic, to_cnf
from sys import exit
from re import search 
from string import ascii_lowercase


def remove_spaces(expr):
  expr = expr.split(' ')
  return ''.join(expr)


def remove_dublicate_negs(expr):
  return expr.replace('~~', '')


def clarify_conjunction(expr):
  seq_found = search(r"(?:(?:~{0,}[A-z])|~{0,}\(.*\)){2}", expr)
  while seq_found:
    pat = seq_found.group(0)
    bracketCnt = 0
    first_operand = True
    a = ""
    b = ""
    for l in pat:
      if l == '(':
        bracketCnt += 1
        if len(a) > 0 and a != '~' and bracketCnt == 1:
          first_operand = False # a(...)
      elif l == ')':
        bracketCnt -= 1
        if bracketCnt == 0 and first_operand:
          first_operand = False # (...)b, (...)(...)
          a += l
          continue
      elif l == '~' and len(a) > 0 and bracketCnt == 0:
        first_operand = False # a~b, a~(...)
      elif l in ascii_lowercase and len(a) > 0 and bracketCnt == 0 and a != '~':
        first_operand = False # ab
      
      if (first_operand):
        a += l
      else:
        b += l
    expr = expr.replace(pat, f"{a} & {b}", 1)
    seq_found = search(r"(?:(?:~{0,}[A-z])|~{0,}\([^\(\)]*\)){2}", expr)
  return expr    


def replace_operator(operator, rep, expr):
  op_found = search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  while op_found:
    pat = op_found.group(0)
    operands = pat.split(operator)
    expr = expr.replace(pat, f"{rep}({operands[0]}, {operands[1]})", 1)
    op_found = search(r"[^&|+>=!/]+\{}[^&|+>=!/]+".format(operator), expr)
  return expr


def format(expr):
  expr = remove_spaces(expr)
  expr = remove_dublicate_negs(expr)
  expr = clarify_conjunction(expr)
  # Important to save the operators order to keep it correct
  expr = replace_operator('=', "Equivalent", expr)
  expr = replace_operator('>', "Implies", expr)
  expr = replace_operator('!', "Nor", expr)
  expr = replace_operator('/', "Nand", expr)
  expr = replace_operator('+', "Xor", expr)
  return expr


def show_menu():
  print("""
    [menu] Choose the option:
      "1" to simplify your expression 
      "2" to convert show your expression to dnf form
      "3" to convert it to cnf form
      "exit" to exit the program
      "back" to return to main menu
      "help" to get hints
  """)
  choice = input(">>> ")
  if (choice == "exit"): 
    exit()
  if (choice == "help"):
    start()
  if (choice == "1"):
    entry("[simplify]", simplify_logic)
  if (choice == "2"):
    entry("[dnf]", to_dnf)
  if (choice == "3"):
    entry("[cnf]", to_cnf)
  else:
    show_menu()


def entry(program, callback):
  print(f"{program} Type your expression:")
  expr = ""
  while (expr != "back"):
    expr = input(">>> ")
    if (expr == "exit"):
      exit()
    if (expr == "back"):
      show_menu()
    print(callback(format(expr)))
    

def start():
  print(f"""
    +--------+------------+--------+------------+
    | Symbol | Operation  | Symbol | Operation  |   Note that:
    +--------+------------+--------+------------+   1) ab = a & b
    |   &    |    AND     |   !    |    NOR     |   2) (...)(...) = (...) & (...)
    +--------+------------+--------+------------+  
    |   |    |    OR      |   /    |    NAND    |    
    +--------+------------+--------+------------+  
    |   +    |    XOR     |   >    |  IMPLIES   |
    +--------+------------+--------+------------+   
    |   =    | EQUIVALENT |   ~    |    NOT     |   
    +--------+------------+--------+------------+                      
  """)
  show_menu()  


if __name__ == "__main__":
  start()