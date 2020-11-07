import axios from 'axios';
import frontConfig from 'src/config/server';

import {
  BackendUnavailableError,
  GameNotFoundError,
  AbstractError,
} from 'src/utils/error.types';
import {
  HealthResponse,
  TakeHandResponse,
  PlayTurnResponse,
  CreateGameResponse,
  DeleteGameResponse,
} from '../model/backendResponse';
import { Game } from '../model/game';

const { backendProtocol, backendHost, backendPort } = frontConfig;
const BACKEND_URL = `${backendProtocol}://${backendHost}:${backendPort}`;

export class BackendConnector {
  async checkBackendHealth(): Promise<boolean> {
    try {
      const url = `${BACKEND_URL}/health`;
      const response = await axios.get(url);
      const healthResponse: HealthResponse = response.data;
      return !!healthResponse;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async getGames(finished: boolean): Promise<Game[]> {
    try {
      const ONLY_ID = false;
      const url = `${BACKEND_URL}/game?finished=${finished}&onlyId=${ONLY_ID}`;
      const response = await axios.get(url);
      const games: Game[] = response.data;
      return games;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async getGameById(idGame: string): Promise<Game> {
    try {
      const url = `${BACKEND_URL}/game/${idGame}`;
      const response = await axios.get(url);
      const games: Game = response.data;
      return games;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (message.includes('Not found')) throw new GameNotFoundError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async getGameTurnHand(idGame: string): Promise<TakeHandResponse> {
    try {
      const url = `${BACKEND_URL}/game/${idGame}/hand`;
      const response = await axios.get(url);
      const handResp: TakeHandResponse = response.data;
      return handResp;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async playGameTurn(
    idGame: string,
    cardIndexes: number[],
  ): Promise<PlayTurnResponse> {
    try {
      const url = `${BACKEND_URL}/game/${idGame}/hand`;
      const body = { cardIndexes };
      const response = await axios.put(url, body);
      const turnDetails: PlayTurnResponse = response.data;
      return turnDetails;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async createGame(playerName: string): Promise<string> {
    try {
      const url = `${BACKEND_URL}/game`;
      const body = { playerName };
      const response = await axios.post(url, body);
      const { _id: idGame }: CreateGameResponse = response.data;
      return idGame;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }

  async deleteGame(idGame: string): Promise<boolean> {
    try {
      const url = `${BACKEND_URL}/game/${idGame}`;
      const response = await axios.delete(url);
      const { success }: DeleteGameResponse = response.data;
      return success;
    } catch (err) {
      const { message } = err;
      if (message.includes('ECONNREFUSED')) throw new BackendUnavailableError();
      if (!!err.response) {
        const {
          data: { error },
          status,
        } = err.response;
        throw new AbstractError(error || message, status);
      }
      throw err;
    }
  }
}

export default new BackendConnector();
