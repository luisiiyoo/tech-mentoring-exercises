import { Card } from '../../model/game';

export interface PlayerBoardProps {
  cardsSelected?: number[];
  cardsDeck: Card[];
  playerName: string;
  cardsHand: Card[];
}