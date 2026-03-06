from re import findall, search


def remove_spaces(expr):
  expr = expr.split(' ')
  return ''.join(expr)


def remove_dublicate_negs(expr):
  return expr.replace('~~', '')


def clarify_conjunction(expr):
  # regex matches: )( )a )~ a( a~ aa, where a - any letter from eng alphabet   
  seq_found = search(r"[A-z\)][A-z\(~]", expr)
  while seq_found:
    pat = seq_found.group(0)
    expr = expr.replace(pat, f"{pat[0]}&{pat[1]}", 1)
    seq_found = search(r"[A-z\)][A-z\(~]", expr)

  return expr

def replace_operator(operator, rep, expr):
  while operator in expr:
    start_i = expr.index(operator)
    a = expr[start_i - 1]
    b = expr[start_i + 1]
    if a == ')':
      bracketCnt = -1
      i = start_i - 2
      while (bracketCnt != 0):
        if expr[i] == ')': bracketCnt -= 1
        elif expr[i] == '(': bracketCnt += 1
        a = expr[i] + a
        i -= 1
      if i >= 0 and expr[i] == '~':
        a = expr[i] + a
    else:
      if start_i - 2 >= 0 and expr[start_i - 2] == '~':
        a = '~' + a
    
    i = start_i + 2
    if b == '~':
      b += expr[start_i + 2]
      i += 1
    
    if b[-1] == '(':
      bracketCnt = 1
      while bracketCnt != 0:
        if expr[i] == ')': bracketCnt -= 1
        elif expr[i] == '(': bracketCnt += 1
        b = b + expr[i]
        i += 1

    expr = expr.replace(a+operator+b, f"({rep}({a},{b}))", 1)

  return expr


def format_logic(expr):
  expr = remove_spaces(expr)
  expr = remove_dublicate_negs(expr)
  expr = clarify_conjunction(expr)
  # Important to save the operators order to keep it correct
  expr = replace_operator('&', "And", expr)
  expr = replace_operator('/', "Nand", expr)
  expr = replace_operator('|', "Or", expr)
  expr = replace_operator('!', "Nor", expr)
  expr = replace_operator('+', "Xor", expr)
  expr = replace_operator('>', "Implies", expr)
  expr = replace_operator('=', "Equivalent", expr)
  return expr