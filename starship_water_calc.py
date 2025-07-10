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
