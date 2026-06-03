import math

# ============================================================
# ============================================================

class MaterialError(ValueError):
    """Raised for invalid material property values."""
    pass

class GeometryError(ValueError):
    """Raised for invalid geometric dimensions."""
    pass

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Error: Enter a numeric value.")
            continue
        if value <= 0:
            print("  Error: Value must be greater than zero.")
            continue
        return value

def get_poisson_ratio(prompt):
    """Poisson ratio must be strictly between 0 and 0.5."""
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Error: Enter a numeric value.")
            continue
        if not (0 < value < 0.5):
            print("  Error: Poisson ratio must be between 0 and 0.5 (exclusive).")
            continue
        return value

class MechanicalComponent:
    def __init__(self, density, youngs_modulus, poisson_ratio, yield_strength):
        if density <= 0:
            raise MaterialError(f"Density must be positive, got {density}.")
        if youngs_modulus <= 0:
            raise MaterialError(f"Young's modulus must be positive, got {youngs_modulus}.")
        if not (0 < poisson_ratio < 0.5):
            raise MaterialError(f"Poisson ratio must be in (0, 0.5), got {poisson_ratio}.")
        if yield_strength <= 0:
            raise MaterialError(f"Yield strength must be positive, got {yield_strength}.")

        self.density        = density
        self.youngs_modulus = youngs_modulus
        self.poisson_ratio  = poisson_ratio
        self.__yield_strength = yield_strength   # Private — encapsulation

    def get_yield_strength(self):
        return self.__yield_strength

    def display_material(self):
        print(f"  Density         : {self.density} kg/m³")
        print(f"  Young's Modulus : {self.youngs_modulus / 1e9:.1f} GPa")
        print(f"  Poisson Ratio   : {self.poisson_ratio}")
        print(f"  Yield Strength  : {self.__yield_strength / 1e6:.1f} MPa")

class Shaft(MechanicalComponent):
    def __init__(self, density, youngs_modulus, poisson_ratio,
                 yield_strength, radius, length):
        super().__init__(density, youngs_modulus, poisson_ratio, yield_strength)
        if radius <= 0:
            raise GeometryError(f"Radius must be positive, got {radius}.")
        if length <= 0:
            raise GeometryError(f"Length must be positive, got {length}.")
        self.radius = radius
        self.length = length

    def calculate_volume(self):
        try:
            return math.pi * self.radius ** 2 * self.length
        except OverflowError:
            raise GeometryError("Dimensions too large — overflow error.")

    def calculate_mass(self):
        try:
            return self.density * self.calculate_volume()
        except OverflowError:
            raise GeometryError("Mass calculation overflow — check dimensions.")

    def display_results(self, name="Shaft"):
        print(f"\n{'='*50}")
        print(f"  Component       : {name}")
        self.display_material()
        print(f"  Radius          : {self.radius * 1000:.2f} mm")
        print(f"  Length          : {self.length:.3f} m")
        print(f"  Volume          : {self.calculate_volume():.6f} m³")
        print(f"  Mass            : {self.calculate_mass():.4f} kg")
        print(f"{'='*50}")

def build_shaft_from_input(name):
    """Collect and validate shaft parameters, returning a Shaft object."""
    print(f"\n  --- Enter Properties for {name} ---")
    while True:
        try:
            density    = get_positive_float("  Density (kg/m³)        : ")
            youngs_GPa = get_positive_float("  Young's Modulus (GPa)  : ")
            poisson    = get_poisson_ratio( "  Poisson Ratio (0–0.5)  : ")
            yield_MPa  = get_positive_float("  Yield Strength (MPa)   : ")
            radius_mm  = get_positive_float("  Radius (mm)            : ")
            length_m   = get_positive_float("  Length (m)             : ")

            shaft = Shaft(
                density       = density,
                youngs_modulus= youngs_GPa * 1e9,
                poisson_ratio = poisson,
                yield_strength= yield_MPa * 1e6,
                radius        = radius_mm / 1000,
                length        = length_m
            )
            return shaft

        except (MaterialError, GeometryError) as e:
            print(f"  Engineering Error: {e} — please re-enter values.")
        except OverflowError:
            print("  Error: Values too extreme — causes numerical overflow.")

def main():
    print("=" * 55)
    print("   EXPERIMENT 02: OOP Mechanical Component Modelling")
    print("   AI in Mechanical Engineering — ONT406")
    print("   Sharda University")
    print("=" * 55)

    while True:
        print("\n--- MENU ---")
        print("1. Analyse a Single Custom Shaft")
        print("2. Compare Two Custom Shafts")
        print("3. Use Preset (Steel vs Aluminum)")
        print("4. Exit")

        choice = input("\nEnter your choice (1/2/3/4): ").strip()

        if choice == '1':
            shaft = build_shaft_from_input("Custom Shaft")
            shaft.display_results("Custom Shaft")

        elif choice == '2':
            shaft1 = build_shaft_from_input("Shaft 1")
            shaft2 = build_shaft_from_input("Shaft 2")
            shaft1.display_results("Shaft 1")
            shaft2.display_results("Shaft 2")
            try:
                diff = abs(shaft1.calculate_mass() - shaft2.calculate_mass())
                lighter = "Shaft 1" if shaft1.calculate_mass() < shaft2.calculate_mass() else "Shaft 2"
                print(f"\n  {lighter} is lighter by {diff:.4f} kg")
            except (GeometryError, OverflowError) as e:
                print(f"  Comparison Error: {e}")

        elif choice == '3':
            try:
                steel = Shaft(7850, 200e9, 0.30, 250e6, 0.02, 1.0)
                alum  = Shaft(2700,  70e9, 0.33, 150e6, 0.02, 1.0)
                steel.display_results("Steel Shaft (Preset)")
                alum.display_results ("Aluminum Shaft (Preset)")
            except (MaterialError, GeometryError) as e:
                print(f"  Preset Error: {e}")

        elif choice == '4':
            print("\nExiting. Goodbye!")
            break

        else:
            print("  Error: Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Program interrupted by user. Goodbye!")
