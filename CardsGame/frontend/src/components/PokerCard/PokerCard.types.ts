export interface CardProps {
  isSelected: boolean;
  indexHand: number;
  suit: string; //"♣" | "♦" | "♥" | "♠";
  rank: number;
  onSelectCard(indexHand: number): any;
}

export interface CardFaceDownProps {
  isPCPlayer:boolean;
  showOnlySpace: boolean;
  onTakeHand(): any;
}