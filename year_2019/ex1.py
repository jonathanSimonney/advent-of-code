import math


def compute_fuel_requirement(module_mass):
    print(module_mass)
    fuel_mass_required = math.trunc(module_mass/3) - 2
    if fuel_mass_required <= 0:
        return 0
    return fuel_mass_required + compute_fuel_requirement(fuel_mass_required)


with open("data.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [compute_fuel_requirement(int(x.strip())) for x in content]


print(sum(content))
