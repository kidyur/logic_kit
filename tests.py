import formatter
import unittest


class LogicKitTests(unittest.TestCase):
  def test_remove_spaces(self):
    case = 'a b'
    res = formatter.remove_spaces(case)
    self.assertEqual(res, "ab")

    case = 'a    b'
    res = formatter.remove_spaces(case)
    self.assertEqual(res, "ab")
    
    case = ' a  b'
    res = formatter.remove_spaces(case)
    self.assertEqual(res, "ab")
    
    case = ' ( ) ( ) '
    res = formatter.remove_spaces(case)
    self.assertEqual(res, "()()")


  def test_clarify_conjunction(self):
    case = 'ab'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "a&b")

    case = '~ab'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "~a&b")

    case = 'a~b'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "a&~b")

    case = '~a~b'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "~a&~b")

    case = '(a)b'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "(a)&b")

    case = 'a(b)'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "a&(b)")

    case = '~(a)b'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "~(a)&b")

    case = 'a~(b)'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "a&~(b)")

    case = 'abc'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "a&b&c") 

    case = '(a)(b)(c)'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "(a)&(b)&(c)")

    case = '(a&b)(b&c)(c&d)'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "(a&b)&(b&c)&(c&d)")

    case = 'xyz | ~xyz'
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "x&y&z | ~x&y&z")


  def replace_operator_case(self, oper, rep):
    case = f'a{oper}b' 
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, b))")

    case = f'~a{oper}b'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~a, b))")
    
    case = f'a{oper}~b'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, ~b))")

    case = f'~a{oper}~b'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~a, ~b))")

    case = f'~(a){oper}~(b)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~(a), ~(b)))")
    
    case = f'(a){oper}~(b)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}((a), ~(b)))")

    case = f'~(a){oper}(b)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(~(a), (b)))")

    case = f'(a){oper}(b)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}((a), (b)))")

    case = f'a{oper}b{oper}c'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(a, b)), c))")

    case = f'~a{oper}~b{oper}~c'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(~a, ~b)), ~c))")

    case = f'(a){oper}(b){oper}(c)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}((a), (b))), (c)))")

    case = f'~(a){oper}~(b){oper}~(c)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(({rep}(~(a), ~(b))), ~(c)))")

    case = f'a{oper}(b{oper}c)'
    res = formatter.replace_operator(oper, rep, case)
    self.assertEqual(res, f"({rep}(a, (({rep}(b, c)))))")


  def test_replace_operators_all(self):
    self.replace_operator_case('>', "Implies")
    self.replace_operator_case('=', "Equivalent")
    self.replace_operator_case('!', "Nor")
    self.replace_operator_case('/', "Nand")
    self.replace_operator_case('+', "Xor")


  def test_remove_dublicate_negs(self):
    case = 'a' 
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "a")

    case = '~a'
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "~a")

    case = '~~a' 
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "a")

    case = '~~~a' 
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "~a")

    case = '~~a~~b' 
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "ab")

    case = '~a~b' 
    res = formatter.remove_dublicate_negs(case)
    self.assertEqual(res, "~a~b")


  def test_priority_of_operators(self):
    #         2   1
    case = 'a + b & c' 
    res = formatter.format_logic(case)
    self.assertEqual(res, "(Xor(a, (b&c)))")

    #         2   1
    case = 'a = b & c'
    res = formatter.format_logic(case)
    self.assertEqual(res, "(Equivalent(a, (b&c)))")

    #         5   1   3   2   4   6
    case = 'a + b & c | d / e ! f = g'
    res = formatter.format_logic(case)
    self.assertEqual(res, "(Equivalent((Xor(a, (Nor((b&c)|(Nand(d, e)), f)))), g))")

    #         3   1   2
    case = 'a | b & c / d'
    res = formatter.format_logic(case)
    self.assertEqual(res, "a|(Nand((b&c), d))")
  

  def test_prioritize(self):
    case = 'a&b&c' 
    res = formatter.prioritize(case)
    self.assertEqual(res, "(a&b&c)")

    case = '~a&~b&~c' 
    res = formatter.prioritize(case)
    self.assertEqual(res, "(~a&~b&~c)")

    case = 'a&b&c | c&d&b' 
    res = formatter.prioritize(case)
    self.assertEqual(res, "(a&b&c) | (c&d&b)")


  def test_format(self):
    case = "xyz | ~xyz"
    res = formatter.clarify_conjunction(case)
    self.assertEqual(res, "x&y&z | ~x&y&z")

    res = formatter.prioritize(res)
    self.assertEqual(res, "(x&y&z) | (~x&y&z)")

if __name__ == "__main__":
  unittest.main()