
from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import Session, declarative_base, relationship

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, index=True, unique=True, nullable=False)
    discord_mention_string = Column(String, index=True, unique=True, nullable=False)
    true_skill_mu = Column(Float)
    true_skill_sigma = Column(Float)


class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    reported_by_id = Column(Integer, ForeignKey(User.id), nullable=False)
    winner_1_id = Column(Integer, ForeignKey(User.id), nullable=False)
    winner_2_id = Column(Integer, ForeignKey(User.id))
    loser_1_id = Column(Integer, ForeignKey(User.id), nullable=False)
    loser_2_id = Column(Integer, ForeignKey(User.id), nullable=False)
    loser_3_id = Column(Integer, ForeignKey(User.id), nullable=False)
    loser_4_id = Column(Integer, ForeignKey(User.id), nullable=False)
    loser_5_id = Column(Integer, ForeignKey(User.id))

    reported_by = relationship(User, primaryjoin='User.id == Game.reported_by_id')
    winner_1 = relationship(User, primaryjoin='User.id == Game.winner_1_id')
    winner_2 = relationship(User, primaryjoin='User.id == Game.winner_2_id')
    loser_1 = relationship(User, primaryjoin='User.id == Game.loser_1_id')
    loser_2 = relationship(User, primaryjoin='User.id == Game.loser_2_id')
    loser_3 = relationship(User, primaryjoin='User.id == Game.loser_3_id')
    loser_4 = relationship(User, primaryjoin='User.id == Game.loser_4_id')
    loser_5 = relationship(User, primaryjoin='User.id == Game.loser_5_id')

    def human_report(self):
        winners_tokens = [self.winner_1.discord_mention_string]
        if self.winner_2:
            winners_tokens.append(self.winner_2.discord_mention_string)
        losers_tokens = [
            self.loser_1.discord_mention_string,
            self.loser_2.discord_mention_string,
            self.loser_3.discord_mention_string,
            self.loser_4.discord_mention_string,
        ]
        if self.loser_5:
            losers_tokens.append(self.loser_5.discord_mention_string)

        report = ' and '.join(winners_tokens)
        report += ' defeats '
        report += ', '.join(losers_tokens[:-1])
        report += ', and ' + losers_tokens[-1]
        return report


Base.metadata.create_all(engine)
session = Session(bind=engine)
