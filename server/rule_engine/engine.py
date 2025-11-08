

from typing import Dict, List


# def run_rules(kundali_data: Dict) -> List[str]:
#     houses = kundali_data.get("houses", {})
#     results = []

#     # Rule 1: Jupiter in 1st House (Scorpio)
#     if "Jupiter" in houses.get("1", {}).get("planets", []):
#         results.append("You are likely to be wise, spiritual, and philosophical. Your personality radiates confidence and depth.")

#     # Rule 2: Saturn in 4th House (Aquarius)
#     if "Saturn" in houses.get("4", {}).get("planets", []):
#         results.append("Your emotional foundation might be strict or carry burdens from childhood. You take family responsibilities seriously.")

#     # Rule 3: Ketu in 6th House (Aries)
#     if "Ketu" in houses.get("6", {}).get("planets", []):
#         results.append("You have a mysterious strength to overcome enemies and hidden health issues. Spiritual detachment from material service.")

#     # Rule 4: Moon + Rahu in 12th House (Libra)
#     if "Moon" in houses.get("12", {}).get("planets", []) and "Rahu" in houses.get("12", {}).get("planets", []):
#         results.append("Your mind is deeply intuitive and mystical, but may suffer from emotional confusion or foreign entanglements.")

#     # Rule 5: Mars in 11th House (Virgo)
#     if "Mars" in houses.get("11", {}).get("planets", []):
#         results.append("You are energetic in networking and achieving goals. You assertively pursue income and influence.")

#     # Rule 6: Sun, Mercury, Venus in 9th House (Cancer)
#     planets_9th = houses.get("9", {}).get("planets", [])
#     if all(planet in planets_9th for planet in ["Sun", "Mercury", "Venus"]):
#         results.append("You are intelligent, creative, and charming with a deep interest in higher knowledge, arts, and travel.")

#     # Rule 7: Empty 10th House (Leo)
#     # if not houses.get("10", {}).get("planets", []):
#     #     results.append("Your career path is determined more by your own efforts and the influence of your Ascendant lord.")

#     return results

def run_rules(kundali_data: dict) -> list[str]:
    results = []

    # Rule 1: Jupiter in 1st house
    jupiter = kundali_data.get("Jupiter", {})
    if jupiter.get("house") == 1:
        results.append("Jupiter in the 1st house suggests a wise, optimistic, and generous nature. You may have a spiritual bent and a strong moral compass.")

    # Rule 2: Saturn in 4th house
    saturn = kundali_data.get("Saturn", {})
    if saturn.get("house") == 4:
        results.append("Saturn in the 4th house can indicate responsibilities related to home or family, or a sense of restriction in early domestic life.")

    # Rule 3: Ketu in 6th house
    ketu = kundali_data.get("Ketu", {})
    if ketu.get("house") == 6:
        results.append("Ketu in the 6th house is often favorable, indicating the ability to overcome enemies, diseases, and debts through spiritual or unconventional means.")

    # Rule 4: Sun, Mercury, and Venus in 9th house
    sun = kundali_data.get("Sun", {})
    mercury = kundali_data.get("Mercury", {})
    venus = kundali_data.get("Venus", {})
    if sun.get("house") == 9 and mercury.get("house") == 9 and venus.get("house") == 9:
        results.append("Sun, Mercury, and Venus in the 9th house suggests a strong inclination toward higher learning, philosophy, travel, and good fortune.")

    # Rule 5: Mars in 11th house
    mars = kundali_data.get("Mars", {})
    if mars.get("house") == 11:
        results.append("Mars in the 11th house gives energy to achieve goals, with strong networking and friend circle support.")

    # Rule 6: Moon and Rahu in 12th house
    moon = kundali_data.get("Moon", {})
    rahu = kundali_data.get("mean Node", {})  # Assuming Rahu is stored as 'mean Node'
    if moon.get("house") == 12 and rahu.get("house") == 12:
        results.append("Moon and Rahu in the 12th house may cause emotional turbulence, sleep disturbances, and a tendency toward escapism or foreign connections.")

    return results
