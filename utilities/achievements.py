class SteamAchievements(object):
    achievements = [
        dict(id=0, api_name="UNLOCK_SIDEWINDER", unlock_id=2, unlock_type="ship"),
        dict(id=1, api_name="UNLOCK_PENDRAGON", unlock_id=3, unlock_type="ship"),
        dict(id=2, api_name="UNLOCK_NEEDLE", unlock_id=4, unlock_type="ship"),
        dict(id=3, api_name="UNLOCK_TESLA_COIL", unlock_id=17, unlock_type="asset"),
        dict(id=4, api_name="UNLOCK_CHARGE_ENGINE", unlock_id=42, unlock_type="asset"),
        dict(id=5, api_name="UNLOCK_BURST_LASER", unlock_id=5, unlock_type="asset"),
        dict(
            id=6, api_name="UNLOCK_ILMENITE_ENGINE", unlock_id=25, unlock_type="asset"
        ),
        dict(
            id=7, api_name="UNLOCK_ILMENITE_ROUNDS", unlock_id=27, unlock_type="asset"
        ),
        dict(id=8, api_name="UNLOCK_ILMENITE_HULL", unlock_id=23, unlock_type="asset"),
        dict(id=9, api_name="GOOD_ENDING", unlock_type="game_stat"),
        dict(id=10, api_name="BAD_ENDING", unlock_type="game_stat"),
        dict(id=11, api_name="RICH", unlock_type="game_stat"),
        dict(id=12, api_name="UNLOCK_DAMAGE_TWICE", unlock_id=61, unlock_type="asset"),
        dict(id=13, api_name="SWALLOW_WIN", unlock_id=38, unlock_type="asset"),
        dict(id=14, api_name="SIDEWINDER_WIN", unlock_id=70, unlock_type="asset"),
        dict(id=15, api_name="PENDRAGON_WIN", unlock_id=65, unlock_type="asset"),
        dict(id=16, api_name="NEEDLE_WIN", unlock_id=20, unlock_type="asset"),
        dict(id=17, api_name="VOLTON_WIN", unlock_id=68, unlock_type="asset"),
        dict(id=18, api_name="UNLOCK_VOLTON", unlock_id=5, unlock_type="ship"),
        dict(
            id=19, api_name="UNLOCK_DAMAGE_REDUCTION", unlock_id=71, unlock_type="asset"
        ),
    ]

    @property
    def achievement_names(self):
        return [a["api_name"] for a in self.achievements]

    def ship_id_to_name(self, unlock_id):
        ships = [s for s in self.achievements if s["unlock_type"] == "ship"]
        for ship in ships:
            if ship["unlock_id"] == unlock_id:
                return ship["api_name"]
        return None

    def modifier_id_to_name(self, unlock_id):
        modifiers = [m for m in self.achievements if m["unlock_type"] == "asset"]
        for modifier in modifiers:
            if modifier["unlock_id"] == unlock_id:
                return modifier["api_name"]
        return None

    def game_stat_id_to_name(self, unlock_id):
        game_stats = [g for g in self.achievements if g["unlock_type"] == "game_stat"]
        for game_stat in game_stats:
            if game_stat["unlock_id"] == unlock_id:
                return game_stat["api_name"]
        return None

    def __init__(self, game):
        self.game = game

    def check_steam_achievements(self):
        if not self.game.steamworks_initialised:
            return

        for achievement_name in self.achievement_names:
            unlocked = self.game.steamworks.GetAchievement(achievement_name)
            print(f"Unlocked {achievement_name}: {unlocked}")

    def unlock_steam_achievement(self, api_name):
        if not self.game.steamworks_initialised:
            return
        name = str.encode(api_name)
        self.game.steamworks.SetAchievement(name)
        status = self.game.steamworks.StoreStats()
        return status
