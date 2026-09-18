def create_environment_profile(
    soil_ph,
    organic_carbon,
    rainfall,
    temperature,
    land_use
):

    profile = {
        "soil_ph": soil_ph,
        "organic_carbon": organic_carbon,
        "rainfall": rainfall,
        "temperature": temperature,
        "land_use": land_use
    }

    return profile


# Test
profile = create_environment_profile(
    soil_ph=5.2,
    organic_carbon=0.8,
    rainfall=600,
    temperature=29,
    land_use="Agriculture"
)

print("Environmental Profile:")
print(profile)