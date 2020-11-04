import React, { useState } from 'react';

const SearchGame: React.FC = () => {
  const [idGame, setIdGame] = useState('')

  const handleOnChangeIdSearch = (e) => { 
    setIdGame(e.target.value)
  };
  const handleOnSearch = (e) => { console.log(idGame)};
  const handleOnDelete = (e) => { };

  return (
    <div className="SearchGame">
      <h2>Search Game by ID</h2>
      <div className="SearchPanel">
        <input placeholder="Search player" value={idGame} onChange={handleOnChangeIdSearch} />
        <button onClick={handleOnSearch}>Search</button>
        <button onClick={handleOnDelete}>Delete</button>
        <button onClick={() => window.location.reload(true)}>Refresh</button>
      </div>
    </div>
  )
}

export default SearchGame;