from db import session, Game


def all_games():
    games = session.query(Game).all()
    game_strings = [g.human_report() for g in games]
    return '\n'.join(game_strings)
