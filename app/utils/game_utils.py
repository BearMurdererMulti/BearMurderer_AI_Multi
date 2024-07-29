def get_weapon_name(weapon_key, weapons, lang):
    weapon = next((weapon for weapon in weapons if weapon["id"] == weapon_key), None)
    return weapon["weapon"][lang] if weapon else weapon_key

def get_location_name(location_key, places, lang):
    location = next((location for location in places if location["id"] == location_key), None)
    return location["place"][lang] if location else location_key

def get_personality_detail(personality_key, personalities, lang):
    personality = next((p for p in personalities if p["id"] == personality_key), None)
    return personality["personality"]["detail"][lang] if personality else personality_key

def get_feature_detail(feature_key, features, lang):
    feature = next((f for f in features if f["id"] == feature_key), None)
    return feature["feature"]["detail"][lang] if feature else feature_key

def get_name(name_data, lang, names):
    name_info = next((n for n in names if n["id"] == name_data), None)
    return name_info["name"][lang] if name_info else name_data

def create_context(game_state, personalities, features, weapons, places, names):
    lang = game_state["language"]
    npc_info = [
        {
            "name": get_name(npc["name"], lang, names),
            "age": npc["age"],
            "gender": npc["gender"],
            "personality": get_personality_detail(npc["personality"], personalities, lang),
            "feature": get_feature_detail(npc["feature"], features, lang),
            "preferredWeapons": [get_weapon_name(weapon, weapons, lang) for weapon in npc["preferredWeapons"]],
            "preferredLocations": [get_location_name(location, places, lang) for location in npc["preferredLocations"]]
        }
        for npc in game_state["npcs"]
    ]
    return {
        "suspects": npc_info,
        "murderer": {
            "name": get_name(game_state["murderer"]["name"], lang, names),
            "age": game_state["murderer"]["age"],
            "gender": game_state["murderer"]["gender"],
            "personality": get_personality_detail(game_state["murderer"]["personality"], personalities, lang),
            "feature": get_feature_detail(game_state["murderer"]["feature"], features, lang)
        },
        "murdered_npc": {
            "name": get_name(game_state["murdered_npc"]["name"], lang, names),
            "age": game_state["murdered_npc"]["age"],
            "gender": game_state["murdered_npc"]["gender"],
            "personality": get_personality_detail(game_state["murdered_npc"]["personality"], personalities, lang),
            "feature": get_feature_detail(game_state["murdered_npc"]["feature"], features, lang)
        },
        "murder_weapon": get_weapon_name(game_state["murder_weapon"], weapons, lang),
        "murder_location": get_location_name(game_state["murder_location"], places, lang)
    }
