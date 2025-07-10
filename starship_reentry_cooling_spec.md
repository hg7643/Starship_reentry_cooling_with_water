# Starship Reentry Cooling with Water Vaporization: Analysis and Code Specification

## Introduction

This document summarizes the analysis of using liquid water as a cooling fluid for Starship's reentry surface via vaporization to enable rapid reusability. The concept involves loading water from an orbital depot before reentry or on the vehicle proior to launch if onboard capacity is available. Initial calculations focused on converting a portion of the vehicle's kinetic energy into steam, with refinements to assumptions over iterations (e.g., focusing on maximum heating phase, temperature reduction targets, realistic heat transfer fractions, and operational logistics like flights and costs).

The goal is to reduce water quantity and costs while ensuring feasibility. Water is selected as the optimal fluid due to its high latent heat of vaporization (2,260 kJ/kg), surpassing alternatives like ammonia or ethanol.

This analysis can be provided to a future Grok version for refinement. Key questions addressed include:
- Water mass required per reentry.
- Cost to deliver water to orbit (based on propellant costs only).
- Number of reentries supplied per water transport launch, accounting for the freighter's own reentry consumption.

Refinements included:
- Initial overestimation: Assumed 80% of total kinetic energy converted to steam → 1200 tonnes.
- Focused on max heating (30% of KE) → 360 tonnes.
- Temperature reduction to 80% of max tolerable (using radiative equilibrium: heat flux reduction to ~41%) → 270 tonnes.
- Realistic heat transfer fraction (1-3% of dissipated KE becomes vehicle heat load, based on Space Shuttle and hypersonic data) → ~3-5 tonnes per reentry.
- Logistics: One 150-tonne payload launch supplies ~50 reentries.

## Key Assumptions

Assumptions are parameterized in the code for easy modification. Defaults based on Starship specs and reentry physics:

- **Vehicle Mass (`m_vehicle`)**: 120,000 kg (dry mass of Starship upper stage ~120 tonnes).
- **Orbital Velocity (`v_orbital`)**: 7,800 m/s (LEO).
- **Fraction of KE Dissipated in Max Heating (`fraction_max_heating`)**: 0.3 (30%, based on reentry profiles).
- **Heat Transfer Fraction (`heat_fraction`)**: 0.01 (1%, refined from Shuttle data; typical range 0.01-0.03 for blunt-body reentry where most energy heats the atmosphere).
- **Desired Tile Temperature Fraction (`temp_fraction`)**: 0.8 (80% of max tolerable).
- **Latent Heat of Vaporization for Water (`Lv`)**: 2,260,000 J/kg.
- **Payload per Flight (`payload_per_flight`)**: 150 tonnes (Starship to LEO).
- **Propellant Cost per Flight (`propellant_cost_per_flight`)**: $500,000 USD.

Radiative equilibrium assumption: Tile temperature \( T \propto q^{1/4} \), where \( q \) is net heat flux. Reducing \( T \) to 80% requires reducing \( q \) to \( (0.8)^4 \approx 0.41 \), so water absorbs ~59% of heat load.

## Calculation Methodology

1. **Total Kinetic Energy (KE_total)**: \( \frac{1}{2} m v^2 \).
2. **KE in Max Heating (KE_max)**: `fraction_max_heating` × KE_total.
3. **Heat Load to Vehicle (heat_max)**: `heat_fraction` × KE_max.
4. **Fraction Absorbed by Water (`fraction_absorbed`)**: 1 - (`temp_fraction`)^4.
5. **Energy to Steam**: `fraction_absorbed` × heat_max.
6. **Water Mass (`m_water_tonnes`)**: (Energy to Steam / Lv) / 1000 (in tonnes).
7. **Flights Needed**: Ceiling of (`m_water_tonnes` / `payload_per_flight`).
8. **Total Cost**: Flights × `propellant_cost_per_flight`.
9. **Reentries per Launch**: Floor of (`payload_per_flight` / `m_water_tonnes`), including freighter's consumption (assumes freighter uses one reentry's worth from payload).

With defaults: ~3 tonnes water per reentry, 1 flight for delivery (~$500k), supplies ~52 reentries per launch (satisfies fewer transport flights than reentries).

## Limitations and Potential Refinements

- **Heat Transfer Accuracy**: Current `heat_fraction=0.01` is conservative; actual may vary with trajectory, angle, etc. Refine with Starship-specific simulations.
- **Efficiency Losses**: Assumes 100% efficient vaporization; add factors for incomplete absorption or system losses.
- **Alternative Fluids**: Water is optimal, but consider mixtures or superheated steam for edge cases.
- **Operational**: Doesn't account for depot losses, water sourcing (e.g., lunar/asteroid mining to reduce Earth launches), or full vehicle mass effects on KE.
- **Future Questions**: 
  - Integrate variable trajectories or Mars reentry.
  - Optimize for cost per reentry over N missions.
  - Compare to ablative shields or no cooling.

Provide this to future LLM with new assumptions or questions, e.g., "Refine with heat_fraction=0.02 and add lunar water sourcing."

## Code Specification

The Python code is a self-contained script for calculations. It uses `math` for ceiling/floor. Run via `python starship_water_calc.py`. Modify variables at top and rerun.

### Code

```python
# Python program to calculate water mass for Starship reentry cooling
# and the cost to deliver that water to orbit
# Assumptions can be changed in the variables below

import math

# Vehicle mass in kg (e.g., dry mass of Starship upper stage ~120 tonnes)
m_vehicle = 120000  # kg

# Orbital velocity in m/s (LEO ~7800 m/s)
v_orbital = 7800  # m/s

# Fraction of total kinetic energy dissipated during maximum heating phase (0.0 to 1.0)
# Based on analysis, ~0.3 for Starship
fraction_max_heating = 0.3

# Fraction of kinetic energy that becomes heat flux to the vehicle (0.01 to 0.03 typical for blunt body reentry)
# Based on Shuttle data and Starship estimates ~0.01
heat_fraction = 0.01

# Desired tile temperature as fraction of maximum tolerable (0.0 to 1.0)
temp_fraction = 0.8

# Latent heat of vaporization for water in J/kg (at boiling point)
Lv = 2260000  # J/kg

# Payload capacity per Starship flight to LEO in tonnes
payload_per_flight = 150  # tonnes

# Propellant cost per Starship flight in USD
propellant_cost_per_flight = 500000  # USD

# Calculate total kinetic energy in J
KE_total = 0.5 * m_vehicle * v_orbital ** 2

# Kinetic energy during max heating phase
KE_max = fraction_max_heating * KE_total

# Heat load during max heating phase
heat_max = heat_fraction * KE_max

# Fraction of heat to tiles (radiative equilibrium assumption)
heat_to_tiles_fraction = temp_fraction ** 4

# Fraction of heat absorbed by water vaporization
fraction_absorbed = 1 - heat_to_tiles_fraction

# Energy to be converted to steam
energy_to_steam = fraction_absorbed * heat_max

# Required water mass in kg
m_water_kg = energy_to_steam / Lv

# Convert to metric tonnes
m_water_tonnes = m_water_kg / 1000

# Number of flights needed (ceiling to whole flights)
num_flights = math.ceil(m_water_tonnes / payload_per_flight)

# Total cost in USD
total_cost = num_flights * propellant_cost_per_flight

# Reentries supplied per single water transport launch (including freighter's reentry)
reentries_per_launch = math.floor(payload_per_flight / m_water_tonnes)

# Output results
print(f"Total kinetic energy: {KE_total:.2e} J")
print(f"KE during max heating ({fraction_max_heating*100}%): {KE_max:.2e} J")
print(f"Heat during max heating (heat_fraction {heat_fraction}): {heat_max:.2e} J")
print(f"Fraction absorbed by water: {fraction_absorbed:.2f}")
print(f"Energy to steam: {energy_to_steam:.2e} J")
print(f"Required water mass: {m_water_tonnes:.0f} metric tonnes")
print(f"Number of flights needed: {num_flights}")
print(f"Total cost to deliver water to orbit: ${total_cost:,} USD")
print(f"Reentries supplied per launch (including freighter): {reentries_per_launch}")
```

### Example Output (with Defaults)

```
Total kinetic energy: 3.65e+12 J
KE during max heating (30.0%): 1.10e+12 J
Heat during max heating (heat_fraction 0.01): 1.10e+10 J
Fraction absorbed by water: 0.59
Energy to steam: 6.47e+09 J
Required water mass: 3 metric tonnes
Number of flights needed: 1
Total cost to deliver water to orbit: $500,000 USD
Reentries supplied per launch (including freighter): 52
```
### Reference link to orginal Grok 4 analysis iterations

https://grok.com/share/bGVnYWN5_c43db318-3399-43ea-987c-6afb37e00af4
