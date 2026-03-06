from re import findall, search


def prioritize(expr):
  seqs = findall(r"~{0,}[A-z](?:&~{0,}[A-z])+", expr)
  for seq in seqs:
    expr = expr.replace(seq, f"({seq})", 1)
  return expr


def clarify_neg(expr):
  seq = search(r"~[A-z]", expr)
  while (seq):
    seq = search()
  return expr


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
  op_found = search(r"(?:(?:~{{0,}}[A-z])|~{{0,}}\([^\{0}]*\))\{0}(?:(?:~{{0,}}[A-z])|~{{0,}}\([^\{0}]*\))".format(operator), expr)
  while op_found:
    pat = op_found.group(0)
    operands = pat.split(operator)
    expr = expr.replace(pat, f"({rep}({operands[0]}, {operands[1]}))", 1)
    op_found = search(r"(?:(?:~{{0,}}[A-z])|~{{0,}}\([^\{0}]*\))\{0}(?:(?:~{{0,}}[A-z])|~{{0,}}\([^\{0}]*\))".format(operator), expr)
  return expr


def format_logic(expr):
  expr = remove_spaces(expr)
  expr = remove_dublicate_negs(expr)
  expr = clarify_conjunction(expr)
  expr = prioritize(expr)
  # Important to save the operators order to keep it correct
  expr = replace_operator('/', "Nand", expr)
  expr = replace_operator('!', "Nor", expr)
  expr = replace_operator('+', "Xor", expr)
  expr = replace_operator('>', "Implies", expr)
  expr = replace_operator('=', "Equivalent", expr)
  return expr
