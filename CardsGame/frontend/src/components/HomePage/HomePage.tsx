import React from 'react';
import './HomePage.css';

const HomePage: React.FC = () => (
  <div className="HomePage">
    <h2>Cards Game App</h2>
    <h3>App Description</h3>
    {/* <h4>Instructions</h4> */}
    <p>
      This App creates Interactive CardsGame between two players (a human and
      the computer). Each game initially contains a single deck containing 52
      cards from a regular Poker deck, each player has a random shuffled deck
      partition divided into 2 equal parts.{' '}
    </p>
    <p>
      In each turn, a random number is selected as target and the first 3 cards
      from each deck are selected as player's hand. Your objective is to select
      2 cards from your hand and adding their ranks to get closer to the target,
      the computer will do the same with its own hand. Comparing both
      approaches, the player who comes closest to the objective will win the
      turn and so on. The game will end until any player has less than 2 cards
      in their deck and loses the game.
    </p>

    <div className="AuthorContainer">
      <h3>Authors</h3>
      <ul>
        <li>
          Luis Gonzalez Guzman,{' '}
          <span className="AuthorEmail">luis.gonzalez@wizeline.com</span>
        </li>
        <li>
          Victor Macedo Madrigal,{' '}
          <span className="AuthorEmail">victor.macedo@wizeline.com</span>
        </li>
      </ul>
    </div>
  </div>
);

export default HomePage;
