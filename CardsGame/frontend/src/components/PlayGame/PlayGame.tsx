import React, { useState } from 'react';
import { store } from 'react-notifications-component';
import { createNotification } from '../../utils/helpers';
import { Game, defaultGame } from 'src/model/game';
import { SearchPanelProps, ControlGameProps } from './PlayGame.types';
import PlayerBoard from '../PlayerBoard';
import connector from '../../connector';
import './PlayGame.css';

const SearchPanel: React.FC<SearchPanelProps> = ({ idGame, handleOnChangeIdSearch, disableIdInput, handleOnSearch,
  disableSearch, handleOnDelete, disableDelete, disableRefresh }) => {
  return (
    <div className="SearchPanel">
      <input placeholder="Search game" value={idGame} onChange={handleOnChangeIdSearch} disabled={disableIdInput} />
      <button onClick={handleOnSearch} disabled={disableSearch}>Search</button>
      <button onClick={handleOnDelete} disabled={disableDelete}>Delete</button>
      <button onClick={() => window.location.reload(true)} disabled={disableRefresh}>Clean</button>
    </div>
  );
}

const PlayGame: React.FC = () => {
  const [idGame, setIdGame] = useState('ec4dbc3b8b40') // HERE
  const [game, setGame] = useState<Game>(defaultGame)
  const [disableIdInput, setDisableIdInput] = useState(false)
  const [disableSearch, setDisableSearch] = useState(!idGame.length)
  const [disableDelete, setDisableDelete] = useState(true)
  const [disableRefresh, setDisableRefresh] = useState(false)

  const disableComponents = (disabled: boolean) => {
    setDisableIdInput(disabled)
    setDisableSearch(disabled)
    setDisableDelete(disabled)
    setDisableRefresh(disabled)
  }
  const handleOnChangeIdSearch = ({ target }) => {
    const id = String(target.value).trim();
    const disable = id.length < 1
    setDisableSearch(disable)
    setIdGame(id)
  };
  const handleOnSearch = async (e) => {
    let gameFound = false;
    try {
      disableComponents(true)
      setGame(await connector.getGameById(idGame))
      const notification = createNotification("success", `Game found.`, 'Success')
      store.addNotification(notification);
      gameFound = true;
    } catch (err) {
      store.addNotification(createNotification("danger", err.message, 'Error'));
      setGame(defaultGame)
    } finally {
      disableComponents(false)
      setDisableDelete(!gameFound)
    }
  };
  const handleOnDelete = (e) => {
    store.addNotification(createNotification("danger", `Not implemented`, `Error`));
  };

  const searchPanelProps: SearchPanelProps = {
    idGame, handleOnChangeIdSearch, disableIdInput, handleOnSearch,
    disableSearch, handleOnDelete, disableDelete, disableRefresh
  }
  const Player1Board = <PlayerBoard cardsDeck={game._deck_p1.cards} playerName={game._name_p1} cardsHand={game._hand_p1} />
  const Player2Board = <PlayerBoard cardsDeck={game._deck_p2.cards} playerName={game._name_p2} cardsHand={game._hand_p2} />
  return (
    <div className="PlayGame">
      <h2>Play Game</h2>
      <SearchPanel {...searchPanelProps} />
      {
        !game._id ? undefined :
          <>
            {Player2Board}
            <ControlGame numTurns={game._num_turns}
              target={game._current_target}
              disablePlayTurn={false}
              handlePlayTurn={() => { store.addNotification(createNotification("danger", `Not implemented`, `Error`)); }} />
            {Player1Board}
          </>
      }
    </div>
  )
}

const ControlGame: React.FC<ControlGameProps> = ({ numTurns, target, disablePlayTurn, handlePlayTurn }) => {
  return (
    <div className="ControlGame">
      <div className="ControlGame-Item">
        <span className="Label">{`Turn:`}</span>
        <span className="Value">{`${numTurns}`}</span>
      </div>
      <div className="ControlGame-Button">
        <button onClick={handlePlayTurn} disabled={disablePlayTurn}>Play Turn</button>
      </div>
      <div className="ControlGame-Item">
        <span className="Label">{`Target:`}</span>
        <span className="Value">{`${target}`}</span>
      </div>
    </div>
  )
}


export default PlayGame;