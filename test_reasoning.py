from reasoning.reasoning_engine import analyze_environment, check_missing_data


# Test environmental data
data = {
    "soil_organic_carbon": 0.7,
    "rainfall": None,
    "species_richness": 6,
    "land_use": "Monoculture"
}


# Test missing data
missing = check_missing_data(data)

print("MISSING DATA:\n")

if missing:
    for item in missing:
        print("-", item)
else:
    print("No missing data.")


# Test reasoning
findings = analyze_environment(data)

print("\nENVIRONMENTAL FINDINGS:\n")

for finding in findings:
    print("-", finding)