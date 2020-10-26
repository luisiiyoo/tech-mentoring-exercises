import axios from 'axios';
import frontConfig from 'src/config/server';

import {
  BackendUnavailableError
} from 'src/utils/error.types';
import { HealthResponse } from './connector.types';

const { backendProtocol, backendHost, backendPort } = frontConfig;
const BACKEND_URL = `${backendProtocol}://${backendHost}:${backendPort}`;

export class BackendConnector {
  async checkBackendHealth(): Promise<boolean> {
    try {
      const url = `${BACKEND_URL}/health`;      
      const healthResponse: HealthResponse = await axios.get(url);
      return !!healthResponse;
    } catch {
      throw new BackendUnavailableError();
    }
  }
  
}

export default new BackendConnector();
