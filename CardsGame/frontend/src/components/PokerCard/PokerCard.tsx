import React from 'react';
import { CardProps, CardFaceDownProps } from './PokerCard.types';
import cardFaceDownImg from '../../img/card_face_down.png';
import cardBlackFaceDownImg from '../../img/back.svg';
import './PokerCard.css'

const suitCharToString = (suit: String) => {
  switch (suit) {
    case '♣':
      return "club";
    case '♦':
      return "diamond";
    case '♥':
      return "heart";
    case '♠':
      return "spade";
    default:
      return suit
  }
}

export const PokerCard: React.FC<CardProps> = ({ indexHand, suit, rank, onSelectCard, isSelected }) => {
  const selected = isSelected ? "Selected" : '';
  const cssRank = `_${rank}`;
  const cssSuit = suitCharToString(suit);
  return (
    <div className={`PokerCard ${cssRank} ${cssSuit} ${selected}`} onClick={() => onSelectCard(indexHand)}>{suit}</div>
  )
}

export const PokerCardFaceDown: React.FC<CardFaceDownProps> = ({ showOnlySpace, onTakeHand, isPCPlayer}) => {
  const image = isPCPlayer ? cardBlackFaceDownImg: cardFaceDownImg;
  const Component = showOnlySpace ?
    <div className={`PokerCard FaceDown`}></div > :
    <img className={`PokerCard FaceDown`} src={image} alt="Deck" onClick={onTakeHand} />
  return Component;
}
