

# from server.pydantic_schemas.kundali_schema import KundaliResponse

# def transform_kundali_response(kundali: KundaliResponse) -> dict:
#     transformed_data = {}

#     # Ascendant
#     transformed_data["Ascendant"] = {
#         "sign": kundali.ascendant.sign,
#         "degree": kundali.ascendant.longitude,
#         "house": kundali.ascendant.index
#     }

#     # Planets
#     for planet_name, planet in kundali.planets.items():
#         transformed_data[planet_name] = {
#             "sign": planet.sign.strip(),
#             "degree": planet.longitude,
#             "house": planet.house
#         }

#     return transformed_data
