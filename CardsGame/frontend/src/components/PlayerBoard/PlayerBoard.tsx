import React, { useState } from 'react';
import { PlayerBoardProps } from './PlayerBoard.types';
import { PokerCard, PokerCardFaceDown } from '../PokerCard';
import ReactTooltip from 'react-tooltip';
import './PlayerBoard.css';

const PlayerBoard: React.FC<PlayerBoardProps> = ({ cardsDeck, playerName, cardsHand, cardsSelected = [] }) => {
  const isPCPlayer = playerName === 'PC';
  const cssRotate = isPCPlayer ? 'Rotate' : '';
  const [idxCardsSelected, setIdxCardsSelected] = useState<number[]>(cardsSelected);

  const lenDeck = cardsDeck.length;
  const showOnlySpace = lenDeck < 1;

  const onSelectCard = isPCPlayer ? () => { } : (indexHand: number) => {
    const posFound = idxCardsSelected.indexOf(indexHand);
    if (posFound === -1 && (idxCardsSelected.length < 2)) {
      setIdxCardsSelected([...idxCardsSelected, indexHand])
    } else {
      const idxSelected = idxCardsSelected.filter((_, idx) => (idx !== posFound));
      setIdxCardsSelected(idxSelected)
    }
  }
  const onTakeHand = isPCPlayer ? () => { } : () => {
    console.log(lenDeck)
  }
  const sumPlayerApprox: string = isPCPlayer ? '?' :
    String(idxCardsSelected
      .map(idx => cardsHand[idx].rank)
      .reduce((a, b) => a + b, 0));
  const tooltipDeckID = `deckLength-${playerName}`;
  
  return (
    <div className={`PlayerBoard ${cssRotate}`}>
      <div className={`PlayerBoard-Title ${playerName}`}>
        <span>{`${playerName}'s Hand`}</span><br></br>
        <span>{`Target sum: ${sumPlayerApprox}`}</span>
      </div>
      <div className={"PlayerBoard-Cards"}>
        <>
          <div data-tip data-for={tooltipDeckID}>
            <PokerCardFaceDown
              showOnlySpace={showOnlySpace}
              onTakeHand={onTakeHand}
              isSelected={cardsHand.length === 0}
              isPCPlayer={isPCPlayer} />
          </div>
          <ReactTooltip id={tooltipDeckID} type='dark'>
            {isPCPlayer? undefined:<p className="Tooltip">{`Take hand`}</p>}
            <p className="Tooltip">{`${cardsDeck.length} cards`}</p>
          </ReactTooltip>
        </>
        {
          cardsHand.map(({ suit, rank }, index) => {
            const tooltipCardID = `rankIndex${index}-${playerName}`;
            return (
              <>
                <div data-tip data-for={tooltipCardID}>
                  <PokerCard
                    key={index}
                    isSelected={idxCardsSelected.includes(index)}
                    suit={suit}
                    rank={rank}
                    indexHand={index}
                    onSelectCard={onSelectCard} />
                </div>
                <ReactTooltip id={tooltipCardID} type='error'>
                  <p className="Tooltip">{`${rank}`}</p>
                </ReactTooltip>
              </>
            )
          })
        }
      </div>
    </div>
  )
}

export default PlayerBoard;