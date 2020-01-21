
import operator as OP
import dill as pickle

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
        else:
          r_str.append('')

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
      
  def update(self, rc1, cell):
   row = rc1[0]
   col = rc1[1]
   if self.cells.get(row) == None:
     self.cells[row] = {}
   self.cells[row][col] = cell

def select(spread, rc1):
  row = rc1[0]
  col = rc1[1]
  return spread.cells[row][col]

# CELL COMPOSITON MONADS
def op(op1, rcs):
  # Sanity Check Array...
  # But... Programming with monads is pure insanity

  def g(spread):
    f = _bind_spread(rcs[0])
    for rc in rcs[1:]:
      f = _bind_op(op1, f, rc)
    return f(spread)
  return g

def _bind_op(op1, f, rc1):
  def g(spread):
    return op1(f(spread), select(spread, rc1).eval())
  return g

def _bind_spread(rc1):
  def g(spread):
    return select(spread, rc1).eval()
  return g

# RECURSIVE FUNCTION COMPOSITION
# PHAT calculations could blow that stack
def opf(op1, fs):
  # Sanity Check...
  # Is this insaine? Absolutely...

  def g(spread):
    if len(fs) == 1:
      f1 = fs[0]
      return f1(spread)
    f1 = fs[0]
    f2 = opf(op1,fs[1:])
    return op1(f1(spread), f2(spread))
  return g


class FCell:
  def __init__(self, spread, f):
    def g():
      return f(spread)
    self.eval = g

class Cell:
  def __init__(self, f):
    self.eval = f

def Zero():
  def g():
    return 0
  return g

def Return(val):
  def g():
    return val
  return g

print("-------------------------------------------")
print("==== Functions As Data, Spreadsheet Ex ====")
print("-------------------------------------------\n")
print("UNBOUNDED TWO CELL CALCULATION (Add)")
spr = Spread((1,4), False)
spr.update((0,0), Cell(Return(5)))
spr.update((0,1), Cell(Return(5)))
add_cells_op = op(OP.add, [(0,0), (0,1)])
spr.update((0,3), FCell(spr, add_cells_op))
spr.pr()
print()

print("UNBOUNDED CALCULATION (Add), (Sub)")
spr = Spread((3,6), False)
spr.update((0,0), Cell(Return(5)))
spr.update((0,1), Cell(Return(5)))
spr.update((0,2), Cell(Return(5)))
spr.update((0,3), Cell(Return(5)))
spr.update((1,0), Cell(Return(60)))
spr.update((1,1), Cell(Return(10)))
spr.update((1,2), Cell(Return(10)))
spr.update((1,3), Cell(Return(10)))
add_cells_op = op(OP.add, [(0,0), (0,1), (0,2), (0,3)])
sub_cells_op = op(OP.sub, [(1,0), (1,1), (1,2), (1,3)])
spr.update((0,5), FCell(spr, add_cells_op))
spr.update((1,5), FCell(spr, sub_cells_op))
spr.pp()
print()

print("FUNCTION COMPOSITION")
#spr = Spread((3,4), False)
spr.update((0,5), Cell(Return(0)))
spr.update((1,5), Cell(Return(0)))
add_cells_op = op(OP.add, [(0,0), (0,1), (0,2), (0,3)])
sub_cells_op = op(OP.sub, [(1,0), (1,1), (1,2), (1,3)])
jeeze = opf(OP.add, [add_cells_op, sub_cells_op])
spr.update((2, 5), FCell(spr, opf(OP.add, [add_cells_op, sub_cells_op])))
spr.pp()
print()

print("Higher Order Function COMPOSITION")
spr = Spread((5,8), False)
spr.update((0,5), Cell(Return(0)))
spr.update((1,5), Cell(Return(0)))

spr.update((0,0), Cell(Return(5)))
spr.update((0,1), Cell(Return(5)))
spr.update((0,2), Cell(Return(5)))
spr.update((0,3), Cell(Return(5)))
spr.update((1,0), Cell(Return(60)))
spr.update((1,1), Cell(Return(10)))
spr.update((1,2), Cell(Return(10)))
spr.update((1,3), Cell(Return(10)))
spr.update((2,0), Cell(Return(5)))
spr.update((2,1), Cell(Return(5)))
spr.update((2,2), Cell(Return(5)))
spr.update((2,3), Cell(Return(5)))
spr.update((3,0), Cell(Return(5)))
spr.update((3,1), Cell(Return(5)))
spr.update((3,2), Cell(Return(5)))
spr.update((3,3), Cell(Return(5)))

add_cells_op0 = op(OP.add, [(0,0), (0,1), (0,2), (0,3)])
sub_cells_op1 = op(OP.sub, [(1,0), (1,1), (1,2), (1,3)])
add_cells_op2 = op(OP.add, [(2,0), (2,1), (2,2), (2,3)])
add_cells_op3 = op(OP.add, [(3,0), (3,1), (3,2), (3,3)])

calc01 = opf(OP.add, [add_cells_op0, sub_cells_op1])
calc02 = opf(OP.add, [add_cells_op2, add_cells_op3])

totalCalc = opf(OP.add, [calc01, calc02])

spr.update((0, 5), FCell(spr, add_cells_op0))
spr.update((1, 5), FCell(spr, sub_cells_op1))
spr.update((2, 5), FCell(spr, add_cells_op2))
spr.update((3, 5), FCell(spr, add_cells_op3))

spr.update((1, 6), FCell(spr, calc01))
spr.update((3, 6), FCell(spr, calc02))
spr.update((4, 7), FCell(spr, totalCalc))
spr.pp()
print()

fname = 'Spread.pkl'
print("Serializing File as: " + fname)
with open(fname, 'wb') as file:
    pickle.dump(spr, file)
print()


ser = None
print("Deserializing File as: " + fname)
with open(fname, 'rb') as file:
    ser = pickle.load(file)
print()

print("Pretty Printing Saved Spreadsheet")
ser.pp()