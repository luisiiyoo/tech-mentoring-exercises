export interface SpecialRanks {
  [key: number]: string
}

export interface Suits {
  club: string;
  diamond: string;
  heart: string;
  spade: string;
}

export interface Deck {
  cards: Card[];
  num_ranks: number;
  special_ranks: SpecialRanks
  suits: Suits
}

export interface Card {
  rank: number;
  suit: string;
}

export interface Game {
  _id: string;
  _winner: string;
  _name_p1: string;
  _name_p2: string;
  _num_turns: number;
  _created_date: number;
  _current_target: number;
  _deck_p1: Deck;
  _deck_p2: Deck;
  _hand_p1: Card[];
  _hand_p2: Card[];
  _history: History;
}

export interface History {
  [key: number]: HistoryDecks | HistoryTurns;
}

export interface HistoryDecks {
  DeckPlayer1: Deck;
  DeckPlayer2: Deck;
}

export interface HistoryTurns {
  cardsSelectedPlayer1: string[];
  cardsSelectedPlayer2: string[];
  lenDeckPlayer1: number;
  lenDeckPlayer2: number;
  sumCardsSelectedPlayer1: number;
  sumCardsSelectedPlayer2: number;
  target: number;
  turn: number;
  turnWinner: string;
}