from db import session, User, Game


def save_game_report(winners, losers, reporter):
    existing_users = session.query(User).filter(
        User.discord_id.in_(
            [w.id for w in winners] + [l.id for l in losers] + [reporter.id]
        )
    ).all()

    discord_id_to_user = {}
    for user in existing_users:
        discord_id_to_user[user.discord_id] = user

    for member in winners + losers + [reporter]:
        if member.id not in discord_id_to_user:
            user = User(discord_id=member.id, discord_mention_string=member.mention)
            session.add(user)
            discord_id_to_user[member.id] = user

    game = Game(
        reported_by=discord_id_to_user[reporter.id],
        winner_1=discord_id_to_user[winners[0].id],
        winner_2=discord_id_to_user[winners[1].id] if len(winners) > 1 else None,
        loser_1=discord_id_to_user[losers[0].id],
        loser_2=discord_id_to_user[losers[1].id],
        loser_3=discord_id_to_user[losers[2].id],
        loser_4=discord_id_to_user[losers[3].id],
        loser_5=discord_id_to_user[losers[4].id] if len(losers) > 4 else None,
    )
    session.add(game)

    session.commit()

    return game


def report(message, tokens):
    if '>' not in tokens:
        return 'report must have `>` in it'

    winners_tokens = []
    losers_tokens = []
    seen_gt = False
    for token in tokens:
        if seen_gt:
            losers_tokens.append(token)
        elif token == '>':
            seen_gt = True
        else:
            winners_tokens.append(token)

    if len(winners_tokens) + len(losers_tokens) != 6:
        return 'Only 6 player games can be reported'

    if len(winners_tokens) < 1 or len(winners_tokens) > 2:
        return 'There must be one or two winners'
    if len(losers_tokens) > 5 or len(losers_tokens) < 4:
        return 'There must be 4 or 5 losers'

    mention_to_member = {}
    for member in message.mentions:
        mention_to_member[member.mention] = member

    try:
        winners = [mention_to_member[m.replace('!', '')] for m in winners_tokens]
        losers = [mention_to_member[m.replace('!', '')] for m in losers_tokens]
    except KeyError:
        return 'Players must be mentioned'

    game = save_game_report(winners, losers, message.author)

    return game.human_report()
