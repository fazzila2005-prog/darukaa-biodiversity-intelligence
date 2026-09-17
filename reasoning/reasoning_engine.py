def analyze_environment(data):

    findings = []

    soc = data.get("soil_organic_carbon")
    rainfall = data.get("rainfall")
    biodiversity = data.get("species_richness")
    land_use = data.get("land_use")
    soil_ph = data.get("soil_ph")
    temperature = data.get("temperature")
    pollution = data.get("pollution")
    deforestation = data.get("deforestation")
    habitat_diversity = data.get("habitat_diversity")


    # ======================================================
    # SOIL CARBON + RAINFALL
    # ======================================================

    if soc is not None and rainfall is not None:

        if soc < 1.0 and rainfall < 600:

            findings.append(
                "Low soil organic carbon combined with relatively "
                "low rainfall indicates potential soil-water stress. "
                "Soil carbon and water availability should therefore "
                "be considered together."
            )


    # ======================================================
    # BIODIVERSITY + LAND USE
    # ======================================================

    if biodiversity is not None and land_use is not None:

        if biodiversity < 10 and land_use.lower() == "monoculture":

            findings.append(
                "Low species richness combined with monoculture "
                "indicates limited habitat and resource diversity. "
                "Land-use diversification and habitat creation "
                "should be considered."
            )


    # ======================================================
    # THREE-VARIABLE INTERACTION
    # ======================================================

    if (
        soc is not None
        and rainfall is not None
        and land_use is not None
    ):

        if (
            soc < 1.0
            and rainfall < 600
            and land_use.lower() == "monoculture"
        ):

            findings.append(
                "Soil organic carbon, rainfall and land use are "
                "interacting environmental factors. Low carbon, "
                "limited rainfall and simplified land use indicate "
                "that soil, water and biodiversity should be "
                "considered together rather than independently."
            )


    # ======================================================
    # FOUR-VARIABLE INTERACTION
    # ======================================================

    if (
        soc is not None
        and rainfall is not None
        and biodiversity is not None
        and land_use is not None
    ):

        if (
            soc < 1.0
            and rainfall < 600
            and biodiversity < 10
            and land_use.lower() == "monoculture"
        ):

            findings.append(
                "Four environmental indicators show potential "
                "combined pressure: low soil organic carbon, "
                "low rainfall, low species richness and monoculture. "
                "Recommendations should therefore consider soil "
                "health, water availability, habitat diversity and "
                "biodiversity together."
            )


    # ======================================================
    # SOIL pH
    # ======================================================

    if soil_ph is not None:

        if soil_ph < 5.5:

            findings.append(
                "The measured soil pH is acidic. Soil pH can influence "
                "nutrient availability and soil biological activity, "
                "so soil chemistry should be considered when evaluating "
                "soil health and biodiversity."
            )

        elif soil_ph > 8.5:

            findings.append(
                "The measured soil pH is alkaline. Soil pH can influence "
                "nutrient availability and soil biological activity, "
                "so soil chemistry should be considered when evaluating "
                "soil health and biodiversity."
            )


    # ======================================================
    # TEMPERATURE
    # ======================================================

    if temperature is not None:

        if temperature > 35:

            findings.append(
                "High temperature can increase environmental stress "
                "for organisms and can interact with water availability. "
                "Temperature and moisture should therefore be considered "
                "together."
            )


    # ======================================================
    # POLLUTION
    # ======================================================

    if pollution is not None:

        if str(pollution).lower() in [
            "high",
            "severe",
            "heavy"
        ]:

            findings.append(
                "High pollution represents a potential pressure on "
                "biodiversity and ecosystem functioning. Pollution "
                "reduction should be considered alongside habitat "
                "and land-management measures."
            )


    # ======================================================
    # DEFORESTATION
    # ======================================================

    if deforestation is not None:

        if str(deforestation).lower() in [
            "high",
            "severe",
            "heavy"
        ]:

            findings.append(
                "High deforestation pressure can contribute to habitat "
                "loss and fragmentation. Habitat connectivity and "
                "remaining vegetation should therefore be considered."
            )


    # ======================================================
    # HABITAT DIVERSITY
    # ======================================================

    if habitat_diversity is not None:

        if str(habitat_diversity).lower() in [
            "low",
            "poor"
        ]:

            findings.append(
                "Low habitat diversity indicates a potentially "
                "simplified habitat structure. Increasing habitat "
                "variety may be relevant when supported by local "
                "conditions and scientific evidence."
            )


    return findings


# ==========================================================
# MISSING DATA
# ==========================================================

def check_missing_data(data):

    missing = []

    if data.get("soil_organic_carbon") is None:

        missing.append(
            "soil organic carbon"
        )

    if data.get("rainfall") is None:

        missing.append(
            "annual rainfall"
        )

    if data.get("species_richness") is None:

        missing.append(
            "species richness"
        )

    if data.get("land_use") is None:

        missing.append(
            "land use"
        )

    return missing