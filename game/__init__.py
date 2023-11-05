from otree.api import *


doc = """
mini ultimatum game
"""

class C(BaseConstants):
    NAME_IN_URL = 'game'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass

class Player(BasePlayer):
    endowed_amount = 200
    amount_sent = models.CurrencyField(min=0, max=200, label="How much money will you send to Player 2?")


class Group(BaseGroup):
    punish_decision = models.BooleanField(
        label="Do you want to punish Player 1? (If you think the offer is unfair, select 'Punish'. If you think it's fair, select 'Not Punish.')",
        choices=[(True, 'Punish'), (False, 'Not Punish')]
    )


    def set_payoffs(self):
        amount_sent = self.player.amount_sent
        if self.punish_decision:
            self.player.payoff = 0
        else:
            self.player.payoff = self.player.endowed_amount - amount_sent
            self.get_player_by_id(2).payoff = amount_sent
        self.player.participant.vars['punish_decision'] = self.punish_decision


    def vars_for_admin_report(self):
        return dict(
            total_payoffs=sum([p.payoff for p in self.get_players()])
        )

def set_amount_sent(player):
    return player.group.get_player_by_id(1).amount_sent

def set_punish_decision(player):
    return player.group.punish_decision

# class Player1(Player):
#     pass

class Player3(Player):
    pass


class Player1(Page):
    form_model = 'player'
    form_fields = ['amount_sent']

# class Survey(Page):

class Player3(Page):
     form_model = 'group'
     form_fields = ['punish_decision']

def is_displayed(self):
        return self.player.id_in_group == 3

# def vars_for_template(self):
#         amount_sent = set_amount_sent(self.player)
#         return dict(amount_sent=amount_sent)

#     form_model = 'group'
#     form_fields = ['punish_decision']

class Results(Page):
    def vars_for_template(self):
        return {
            'amount_sent': self.player.get_others_in_group()[0].amount_sent,
            'punish_decision': self.group.punish_decision,
        }
        # punish_decision = set_punish_decision(self.player)
        # return dict(punish_decision=punish_decision)

    def before_next_page(self):
        self.group.set_payoffs()




page_sequence = [Player1, Player3, Results]