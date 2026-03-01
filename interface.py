from sympy import to_dnf, simplify_logic, to_cnf
from sys import exit
from formatter import format_logic


def show_menu():
  print("""
    [menu] Choose the option:
    >> "1" to simplify your expression 
    >> "2" to convert show your expression to dnf form
    >> "3" to convert it to cnf form
    >> "exit" to exit the program
    >> "help" to get hints
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
  print(f"""
    {program} Type your expression or "back" to return:
  """)
  expr = ""
  while (expr != "back"):
    expr = input(">>> ")
    if (expr == "exit"):
      exit()
    if (expr == "back"):
      show_menu()
    print(f"""
      {callback(format_logic(expr))}
    """)
    

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