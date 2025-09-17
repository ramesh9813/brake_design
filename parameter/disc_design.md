input parameter
    Vehicle mass (kg)
    Rider + load mass (kg)
    Desired deceleration (m/s²) or Stopping distance + initial speed
    Wheel radius (m)
    Friction coefficient (μ)
    Caliper piston area (cm²)
    Hydraulic pressure (MPa)
    Number of discs per wheel
    Wheel hub/bolt circle dimensions (for inner diameter)
    Material density (kg/m³)
    Material specific heat (J/kg·K)
    Material yield strength (MPa)
    Max outer diameter allowed (packaging constraint)
    Initial disc thickness (mm, design choice)
    Wear allowance (% of thickness)
    Brake energy distribution (front/rear %)
    Fraction of energy absorbed by rotor (vs pads)

output parameter
    Required braking force
    Required braking torque at wheel
    Effective radius of disc
    Outer diameter of disc (approx.)
    Inner diameter of disc (based on hub geometry)
    Disc thickness (first-pass estimate from energy/stress balance)
    Minimum service thickness (rule-based)
    Mass of disc (geometry × density)
    Heat energy absorbed per stop
    Approximate temperature rise (energy / heat capacity)
    Factor of safety (simplified, using σ = F/A)