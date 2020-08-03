import math

#Credit to www.hackerearth.com
class elo:
    def getExpectation(rating_1, rating_2):
        calc = (1.0 / (1.0 + math.pow(10, ((rating_2 - rating_1) / 400))))
        return calc
    def modifiedRating(rating1, rating2, actual, kfactor):
        expected = elo.getExpectation(rating1, rating2)
        calc = (rating1 + kfactor * (actual - expected))
        return calc
    def winnerFirstsNewElo(winner_elo, loser_elo, kfactor):
        return elo.modifiedRating(winner_elo, loser_elo, 1, kfactor)
    def loserFirstsNewElo(loser_elo, winner_elo, kfactor):
        return elo.modifiedRating(loser_elo, winner_elo, 0, kfactor)
