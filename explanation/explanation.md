# Experiment 02 — Code Explanation
# OOP for Mechanical Component Modelling

---

## What is this program doing?

This program models real mechanical components (shafts) as
**software objects** using Object-Oriented Programming (OOP).

Instead of writing separate variables for steel and aluminum,
we create a blueprint (class) once and use it for any material.

**Real life analogy:**
A class is like a **blueprint of a shaft**.
An object is the **actual shaft manufactured** from that blueprint.
You can make many different shafts from the same blueprint.

---

## OOP Core Concepts Used

| Concept | Meaning | Used Where |
|---|---|---|
| Class | Blueprint for creating objects | MechanicalComponent, Shaft |
| Object | Instance of a class | steel_shaft, aluminum_shaft |
| Inheritance | Child class gets parent's features | Shaft inherits from MechanicalComponent |
| Encapsulation | Hiding sensitive data | __yield_strength is private |
| Method | Function inside a class | calculate_volume(), calculate_mass() |

---

## Line by Line Explanation

---

### Line 1
```python
import math
```
We need `math.pi` for the volume formula V = π × r² × L.

---

### Lines 6-17 (Base Class — MechanicalComponent)
```python
class MechanicalComponent:
    def __init__(self, density, youngs_modulus, poisson_ratio, yield_strength):
        self.density = density
        self.youngs_modulus = youngs_modulus
        self.poisson_ratio = poisson_ratio
        self.__yield_strength = yield_strength
```
**What is a class?**
A class is a template/blueprint. `MechanicalComponent` defines
what every mechanical component has in common:
density, Young's modulus, Poisson's ratio, yield strength.

**What is `__init__`?**
This is the **constructor** — it runs automatically whenever
you create a new object. It sets up the initial values.

**What is `self`?**
`self` refers to the specific object being created.
It's how the object refers to its own data.
Think of it as "this particular shaft's density".

**What does `self.density = density` mean?**
- The `density` on the right = the value passed in when creating the object
- `self.density` on the left = stores it as the object's own property

**What is `__yield_strength` (double underscore)?**
This is **Encapsulation** — making data private.
The double underscore `__` means this variable CANNOT be accessed
directly from outside the class.

Why hide yield strength?
In real systems, critical material properties should not be
accidentally changed. Private variables prevent that.

---

### Lines 19-21 (Getter Method)
```python
def get_yield_strength(self):
    """Getter method to access private yield strength"""
    return self.__yield_strength
```
**What is a getter method?**
Since `__yield_strength` is private, we provide a
controlled way to READ it through this method.

You can read it but not change it directly — this is
the whole point of encapsulation.

**How to use it:**
```python
steel_shaft.get_yield_strength()  # Returns 250000000
```

---

### Lines 24-34 (Derived Class — Shaft)
```python
class Shaft(MechanicalComponent):
    def __init__(self, density, youngs_modulus, poisson_ratio,
                 yield_strength, radius, length):
        super().__init__(density, youngs_modulus, poisson_ratio, yield_strength)
        self.radius = radius
        self.length = length
```
**What is `class Shaft(MechanicalComponent)`?**
This is **Inheritance** — Shaft inherits everything from
MechanicalComponent AND adds its own specific properties.

`(MechanicalComponent)` in brackets means:
"Shaft is a child of MechanicalComponent"

**What is `super().__init__(...)`?**
`super()` refers to the parent class (MechanicalComponent).
This line calls the parent's constructor to set up the
inherited properties (density, modulus, etc.)

Then `self.radius` and `self.length` add the
shaft-specific dimensions.

**Why use inheritance?**
If tomorrow you add a Gear or Bearing class, they can also
inherit from MechanicalComponent and reuse the same material
properties code. No duplication.

---

### Lines 36-42 (Methods — Volume and Mass)
```python
def calculate_volume(self):
    """Volume = π × r² × L"""
    return math.pi * self.radius**2 * self.length

def calculate_mass(self):
    """Mass = density × volume"""
    return self.density * self.calculate_volume()
```
**What are these methods?**
Functions that belong to the class and operate on the
object's own data using `self`.

**calculate_volume():**
Uses `self.radius` and `self.length` — the object's own dimensions.
Formula: V = π × r² × L

**calculate_mass():**
Uses `self.density` AND calls `self.calculate_volume()` internally.
A method can call another method of the same class.
Formula: m = ρ × V

---

### Lines 45-70 (Creating Objects)
```python
steel_shaft = Shaft(
    density=7850,
    youngs_modulus=200e9,
    poisson_ratio=0.3,
    yield_strength=250e6,
    radius=0.02,
    length=1.0
)
```
**What is happening here?**
We are creating an actual Shaft object from the blueprint.
`steel_shaft` is a specific shaft made of steel.

**Using keyword arguments (name=value):**
Instead of just passing values in order, we name each argument.
This makes the code readable and prevents mistakes.

**Material values explained:**
- density=7850 → Steel density is 7850 kg/m³
- youngs_modulus=200e9 → Steel stiffness: 200 GPa
- poisson_ratio=0.3 → How much it expands sideways when compressed
- yield_strength=250e6 → Stress at which steel permanently deforms: 250 MPa
- radius=0.02 → 20mm radius
- length=1.0 → 1 meter long

---

### Lines 72-80 (Calling Methods and Printing)
```python
print(f"Volume: {steel_shaft.calculate_volume():.6f} m³")
print(f"Mass: {steel_shaft.calculate_mass():.2f} kg")
print(f"Yield Strength: {steel_shaft.get_yield_strength()/1e6} MPa")
```
**How to call a method:**
`object_name.method_name()` — use dot notation.

`steel_shaft.calculate_mass()` means:
"Calculate mass FOR THIS specific shaft."

**Why divide yield strength by 1e6?**
`get_yield_strength()` returns value in Pa (250,000,000).
Dividing by 1e6 converts to MPa (250) for readable output.

---

## Why This Approach is Powerful

**Without OOP:**
```python
steel_density = 7850
steel_radius = 0.02
steel_length = 1.0
steel_volume = math.pi * steel_radius**2 * steel_length
steel_mass = steel_density * steel_volume

aluminum_density = 2700
aluminum_radius = 0.02
aluminum_length = 1.0
aluminum_volume = math.pi * aluminum_radius**2 * aluminum_length
aluminum_mass = aluminum_density * aluminum_volume
# ... repeating code, messy, error-prone
```

**With OOP:**
```python
steel = Shaft(7850, 200e9, 0.3, 250e6, 0.02, 1.0)
alum  = Shaft(2700, 70e9, 0.33, 150e6, 0.02, 1.0)
print(steel.calculate_mass())
print(alum.calculate_mass())
# Clean, reusable, scalable
```

---

## Common Mistakes to Avoid

| Mistake | Wrong | Correct |
|---|---|---|
| Forgetting self | def calculate_volume(): | def calculate_volume(self): |
| Direct private access | shaft.__yield_strength | shaft.get_yield_strength() |
| Forgetting super() | Just self.radius = radius | super().__init__(...) first |
| Wrong indentation | Method outside class | Method indented inside class |
