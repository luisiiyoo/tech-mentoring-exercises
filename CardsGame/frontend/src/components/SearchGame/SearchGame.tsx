import React, { useState } from 'react';
import { store } from 'react-notifications-component';
import { createNotification } from '../../utils/helpers';
import connector from '../../connector';
import './SearchGame.css'

const SearchGame: React.FC = () => {
  const [idGame, setIdGame] = useState('')
  const [disableIdInput, setDisableIdInput] = useState(false)
  const [disableSearch, setDisableSearch] = useState(true)
  const [disableDelete, setDisableDelete] = useState(true)
  const [disableRefresh, setDisableRefresh] = useState(false)

  const disableComponents = (disabled: boolean) => {
    setDisableIdInput(disabled)
    setDisableSearch(disabled)
    setDisableDelete(disabled)
    setDisableRefresh(disabled)
  }
  const handleOnChangeIdSearch = ({ target }) => {
    const id = String(target.value).trim()
    const disable = id.length < 1
    setDisableSearch(disable)
    setIdGame(id)
  };
  const handleOnSearch = async (e) => {
    let gameFound = false;
    try {
      disableComponents(true)
      const game = await connector.getGameById(idGame)
      const notification = createNotification("success", `Game found.`, 'Success')
      store.addNotification(notification);
      gameFound = true;
    } catch (err) {
      store.addNotification(createNotification("danger", err.message, 'Error'));
    } finally {
      disableComponents(false)
      setDisableDelete(!gameFound)
    }
  };
  const handleOnDelete = (e) => {
    const notification = createNotification("danger", `Not implemented`, `Error`)
    store.addNotification(notification);
  };

  return (
    <div className="SearchGame">
      <h2>Search Game by ID</h2>
      <div className="SearchPanel">
        <input placeholder="Search game" value={idGame} onChange={handleOnChangeIdSearch} disabled={disableIdInput} />
        <button onClick={handleOnSearch} disabled={disableSearch}>Search</button>
        <button onClick={handleOnDelete} disabled={disableDelete}>Delete</button>
        <button onClick={() => window.location.reload(true)} disabled={disableRefresh}>Refresh</button>
      </div>
    </div>
  )
}

export default SearchGame;