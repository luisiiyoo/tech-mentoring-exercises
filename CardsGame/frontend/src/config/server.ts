/**
 * Interface for FrontEnd application configuration settings
 *
 * @interface FrontendConfig
 */
interface FrontendConfig {
  serverName: string;
  backendProtocol: string;
  backendHost: string;
  backendPort: number;
}

if (
  !process.env.REACT_APP_BACKEND_HOST &&
  !process.env.REACT_APP_BACKEND_PORT
) {
  console.warn(
    '.env file was not created, default values will used.'.toUpperCase(),
  );
}

// default settings are for development environment
const frontConfig: FrontendConfig = {
  serverName: process.env.REACT_APP_SERVER_NAME || 'Front-End app',
  backendProtocol: process.env.REACT_APP_BACKEND_PROTOCOL || 'http',
  backendHost: process.env.REACT_APP_BACKEND_HOST || '0.0.0.0',
  backendPort: Number(process.env.REACT_APP_BACKEND_PORT) || 8080,
};

export default frontConfig;
