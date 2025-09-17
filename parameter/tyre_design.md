# Bike Tyre Design
keep styling same as other thing design 

# Input parameters
Bike type
Vehicle mass (kg)
Rim diameter (inches)
Desired aspect ratio (%)
Section width (mm)

# Output parameters
Section height (mm)
Overall diameter (mm)
Tread thickness (mm)
Sidewall thickness (mm)
Bead size (mm)
Crown radius (mm)
Contact patch area (m²)

# Formulas / Standard values
Section height (mm)     = (Aspect ratio / 100) × Section width

Overall diameter (mm)   = (2 × Section height) + (Rim diameter × 25.4)

Tread thickness (mm)    = Standard by bike type:
                          commuter: 6–8
                          sports: 7–9
                          superbike: 8–9
                          cruiser/touring: 8–10
                          offroad: 10–12

Sidewall thickness (mm) = 6–10% of Section height

Bead size (mm)          = 15–20 (standard range)

Crown radius (mm)       = ~1.7 × Section width

Contact patch area (m²) = Load per tyre / Inflation pressure
                          Load per tyre ≈ (Vehicle mass × 9.81) / 2
                          Typical inflation pressure = 200–250 kPa


## Integration & UI Behaviour (home page)

- Add one card/link called **Tyre Design**
- Clicking it navigates to route `/tyredesign`
- On that page, present form asking for **Input parameters** as above
- After user submits, display **Output parameters** on right side (as results), similar to existing “other design” tools (disc design etc.)
- search the calculation formula from internet. find how to find the output parameter from the intput parameter .implement in code 