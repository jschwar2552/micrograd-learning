# Python Fundamentals Cheat Sheet

## TLDR Syntax

### Classes & Instances
```python
class Box:                    # Define a blueprint
    pass

my_box = Box()                # Build an instance from the blueprint
```

### Attributes (stuff inside)
```python
my_box.color = "red"          # Add attribute after creation
print(my_box.color)           # Read it back: "red"
```

### `__init__` (automatic setup)
```python
class Box:
    def __init__(self, color, size):   # Runs automatically when you do Box(...)
        self.color = color             # Store inputs as attributes
        self.size = size

red_box = Box("red", 5)       # Creates box with color="red", size=5
```

### `self` = "this particular instance"
```python
class Box:
    def __init__(self, data):
        self.data = data      # self.data means "this box's data compartment"
```

### Operator overloading (`__add__`)
```python
class Box:
    def __init__(self, data):
        self.data = data

    def __add__(self, other):           # Runs when you write a + b
        return Box(self.data + other.data)

a = Box(2)
b = Box(3)
c = a + b    # c.data = 5 (calls a.__add__(b))
```

### Lambda (tiny inline function)
```python
double = lambda x: x * 2      # Same as def double(x): return x * 2
double(5)                     # Returns 10
```

### Sets (no duplicates)
```python
visited = set()
visited.add("a")
visited.add("a")              # Ignored - already there!
"a" in visited                # True - fast lookup
```

---

## Key Terms

| Term | Meaning |
|------|---------|
| **Class** | Blueprint/instructions for making things |
| **Instance** | A thing built from a class |
| **Attribute** | Data stored inside an instance (`box.color`) |
| **`__init__`** | Code that runs automatically when creating an instance |
| **`self`** | "This particular instance I'm working with" |
| **`__add__`** | Defines what `+` does for your class |
| **`__repr__`** | Defines what `print()` shows |
| **Lambda** | One-line function you can store and call later |
| **Set** | Collection with no duplicates, fast lookup |

---

## Why Boxes Instead of Plain Numbers?

Plain `2 + 3 = 5` forgets everything. Just the answer.

`Value(2) + Value(3) = Value(5)` can **remember its history**:
- `c._prev = {a, b}` — "c came from a and b"
- This is how backpropagation traces backwards!

---

## Custom Reminders (From Your Questions)

### Double underscores matter!
```python
def __init__(self):    # CORRECT - two underscores each side
def _init_(self):      # WRONG - won't work!
```

### Don't forget parameters
```python
# WRONG - can't customize
def __init__(self):
    self.name = "Jason"

# RIGHT - accepts inputs
def __init__(self, name, age):
    self.name = name
    self.age = age
```

### `_children` is not magic
The underscore just means "internal." We manually pass parents in `__add__`:
```python
def __add__(self, other):
    out = Value(self.data + other.data, (self, other))  # We pass (a, b) here!
    return out
```

---

## Common Mistakes to Avoid

1. **Single vs double underscores**: `__init__` not `_init_`

2. **Forgetting to add parameters**: If you want `Person("Jason", 27)` to work, you need `def __init__(self, name, age):`

3. **String vs number**: `"27"` is text, `27` is a number you can do math with

4. **Thinking `self` is automatic content**: `self` is just a reference to "this instance" - YOU fill it with `self.whatever = value`

---

## Micrograd Connection

The `Value` class is just a fancy Box:
```python
class Value:
    def __init__(self, data, _children=()):
        self.data = data           # The number
        self.grad = 0              # Gradient (calculus)
        self._prev = set(_children) # Who made me
        self._backward = lambda: None
```

When you do `c = a + b`:
- `c.data` = the sum
- `c._prev` = `{a, b}` (remembers parents for backprop)
