
class Game():

    def __init__(self, first_player):
        self.players = [first_player]
        self.died_players = []

    def join_game(self, new_player):
        check = True        #проверка на то присоединен ли уже этот игрок
        for player in self.players:
            if new_player.id == player.id:
                check = False
        if check:
            self.players.append(new_player)
            return True

    def action(self, move, player,  player_under_action):
        if move == 'прибыль':
            player.coins += 1
        elif move == 'взятка':
            if player_under_action.coins < 2:
                player.coins += player_under_action.coins
                player_under_action.coins = 0
            else:
                player.coins += 2
                player_under_action.coins -=2
        elif move == 'ресурсы':
            player.coins += 1
        elif move == 'обман':
            player.coins -= 3
            playerplayer_under_action.coins += 3
        elif move == 'завещание':
            player.coins += player_under_action.coins
            player_under_action.coins = 0
        elif move == 'перестройка':
            player.coins -= 7

    def check(self, move, player):
        check_result = False
        for card in player.cards:
            if move == card.action:
                check_result = True
                break
        return check_result

    def find_player_id(self, id):
        for player in self.players:
            if player.id == id:
                return player

class Player():

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.last_message = None
        self.last_message_block = None
        self.coins = 2
        self.cards = [] 
        self.open_cards = ''
        self.pluralizm_cards = []
        self.is_alive = True
