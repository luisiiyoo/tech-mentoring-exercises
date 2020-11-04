import axios from 'axios';
import frontConfig from 'src/config/server';

import {
  BackendUnavailableError
} from 'src/utils/error.types';
import { HealthResponse } from '../model/backendResponse';
import { Game } from '../model/game';

const { backendProtocol, backendHost, backendPort } = frontConfig;
const BACKEND_URL = `${backendProtocol}://${backendHost}:${backendPort}`;

export class BackendConnector {
  async checkBackendHealth(): Promise<boolean> {
    try {
      const url = `${BACKEND_URL}/health`;
      const response = await axios.get(url);
      const healthResponse: HealthResponse = response.data
      return !!healthResponse;
    } catch {
      throw new BackendUnavailableError();
    }
  }

  async getGames(finished: boolean): Promise<Game[]> {
    try {
      const ONLY_ID = false;
      const url = `${BACKEND_URL}/game?finished=${finished}&onlyId=${ONLY_ID}`;
      const response = await axios.get(url);
      const games: Game[] = response.data
      return games;
    } catch {
      throw new BackendUnavailableError();
    }
  }

  async getGameById(idGame: string): Promise<Game> {
    try {
      const url = `${BACKEND_URL}/game/${idGame}`;
      const response = await axios.get(url);
      const games: Game = response.data
      return games;
    } catch {
      throw new BackendUnavailableError();
    }
  }
}

export default new BackendConnector();
