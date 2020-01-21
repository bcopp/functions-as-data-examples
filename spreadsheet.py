import operator as OP

class Spread:
  def __init__(self, rc, isZeroed=False):
    self.row = rc[0]
    self.col = rc[1]
    self.cells = {}

    if isZeroed:
      for r in range(0, self.row):
        self.cells[r] = {}
        for c in range(0, self.col):
          self.cells[r][c] = Cell(Zero())
  
  def update(self, rc, cell):
    row = rc[0]
    col = rc[1]
    if self.cells.get(row) == None:
      self.cells[row] = {}
    self.cells[row][col] = cell

  def pr(self):
    for r in range(0, self.row):
      r_str = []
      for c in range(0, self.col):
        if self.cells.get(r) != None and self.cells.get(r).get(c) != None:
          r_str.append(str(self.cells[r][c].eval()))
        r_str.append("|")
      print(''.join(r_str[:-1]))

  def pp(self):
    # Create array to track max cols
    max_col_len = []
    for c in range(0, self.col):
      max_col_len.append(0)

    # Get max length for each col
    for c in range(0, self.col):
      for r in range(0, self.row):
        if self.cells.get(r) != None and self.cells.get(r).get(c) != None:
          cur_len = len(str(self.cells[r][c].eval()))
          if max_col_len[c] < cur_len:
            max_col_len[c] = cur_len
    
    # Pretty Print Method
    c = 0
    for r in range(0, self.row):
      r_str = []
      for c in range(0, self.col):
        if self.cells.get(r) != None and self.cells.get(r).get(c) != None:
          r_str.append(str(self.cells[r][c].eval()))

      # Adjust Spacing
      adjusted_strs = []
      for c, s in enumerate(r_str):
        dif = abs(len(s) - max_col_len[c])
        new_s = [s]
        for _ in range(0, dif):
          new_s.append(" ")
        new_s.append("|")
        adjusted_strs.append(''.join(new_s))
      print(''.join(adjusted_strs))
      
  # Returns a Cell at this spot
  def select(self, rc):
    row = rc[0]
    col = rc[1]
    if self.cells.get(row) == None:
      return None
    return self.cells[row].get(col)

# Non Generic
  def sum_two(self, rc1, rc2):
    def g():
      return self.select(rc1).eval() + self.select(rc2).eval()
    return g

  # Takes at least two arguments and returns a function that when called calculates the values.
  def sum_many_fn(self, rc1, rc2, *rcs):
    def g():
      return self.select(rc1).eval() + self.select(rc2).eval()
    f = g
    for rc in rcs:
      f = self.bind_sum_select(f, rc) 
    return f 

  def bind_sum_select(self, f, rc):
    def g():
      return f() + self.select(rc).eval()
    return g

# Bounded Generalized Monad
  # Made more general by passing in OP
  def bind_op_two(self, op1, rc1, rc2):
    def g():
      return op1(self.select(rc1).eval(), self.select(rc2).eval())
    return g
  

# Unbounded Monads
  def op(self, op1, rc1, rc2, *rcs):
    def g():
      return op1(self.select(rc1).eval(), self.select(rc2).eval())
    f = g
    for rc in rcs:
      f = self._bind_op_select(op1, f, rc)
    return f

  def _bind_op_select(self, op1, f, rc):
    def g():
      return op1(f(), self.select(rc).eval())
    return g

  # op is the operation between two functions
  # fopf is zero or many tuples containing (operator, function)
  def bind_f(self, f1, op1, f2, *opfs):
    def g():
      return op1(f1(), f2())
    f = g
    for (op_, f_) in opfs:
      f = self.bind_f_helper(f, op_, f_)
    return f

  def bind_f_helper(self, f1, op1, f2):
    def g():
      return op1(f1(), f2())
    return g
  
class Cell:
  def __init__(self, fn):
    self.eval = fn

def Return(val):
  def g():
    return val
  return g

def Zero():
  def g():
    return 0
  return g

print("-------------------------------------------")
print("==== Functions As Data, Spreadsheet Ex ====")
print("-------------------------------------------\n")
print("BOUNDED TWO CELL CALCULATION (Add)")
spr = Spread((1,6), True)
spr.update((0,0), Cell(Return(5)))
spr.update((0,1), Cell(Return(10)))
sum_fn = spr.bind_op_two(OP.add, (0,0), (0,1))
spr.update((0,5), Cell(sum_fn))
spr.pp()
print("")

print("UNBOUNDED CALCULATION (Add)")
spr2 = Spread((1,6), True)
spr2.update((0,0), Cell(Return(5)))
spr2.update((0,1), Cell(Return(5)))
spr2.update((0,2), Cell(Return(5)))
spr2.update((0,3), Cell(Return(5)))
spr2.update((0,5), Cell(spr2.op(OP.add, (0,0), (0,1), (0,2), (0,3))))
spr2.pp()
print("")

print("UNBOUNDED GENERIC CALCULATIONS (Mul), (Sub), (Pow)")
spr3 = Spread((4,5), True)
spr3.update((0,0), Cell(Return(5)))
spr3.update((0,1), Cell(Return(5)))
spr3.update((0,2), Cell(Return(5)))
spr3.update((1,0), Cell(Return(15)))
spr3.update((1,1), Cell(Return(5)))
spr3.update((1,2), Cell(Return(5)))
spr3.update((2,0), Cell(Return(2)))
spr3.update((2,1), Cell(Return(2)))
spr3.update((2,2), Cell(Return(2)))

spr3.update((0,4), Cell(spr3.op(OP.mul, (0,0), (0,1), (0,2))))
spr3.update((1,4), Cell(spr3.op(OP.sub, (1,0), (1,1), (1,2))))
spr3.update((2,4), Cell(spr3.op(OP.pow, (2,0), (2,1), (2,2))))
spr3.pp()
print("")

print("UNBOUNDED FUNCTIONS BINDED TOGETHER WITH GENERIC OPERATORS")
print("( f0(Mul) (Add) f1(Sub) ) (Mul) f2(Pow)")
print("ie. 125     +      5        *     16")
spr4 = Spread((4,5), True)
spr4.update((0,0), Cell(Return(5)))
spr4.update((0,1), Cell(Return(5)))
spr4.update((0,2), Cell(Return(5)))
spr4.update((1,0), Cell(Return(15)))
spr4.update((1,1), Cell(Return(5)))
spr4.update((1,2), Cell(Return(5)))
spr4.update((2,0), Cell(Return(2)))
spr4.update((2,1), Cell(Return(2)))
spr4.update((2,2), Cell(Return(2)))
spr4.update((3,4), Cell(
  spr4.bind_f(
    spr4.op(OP.mul, (0,0), (0,1), (0,2)),
    OP.add,
    spr4.op(OP.sub, (1,0), (1,1), (1,2)),
    (OP.mul, spr4.op(OP.pow, (2,0), (2,1), (2,2)))
    )
  ))

spr4.pp()
#spr2.update((2,1), Cell(spr2.op(OP.add, (0,0), (0,1), (0,2))))
#spr2.pp()
