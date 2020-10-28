import React, { useState } from 'react';
import { Provider } from 'react-redux';
import configureStore from 'src/redux/store';
import Routes from 'src/routers';
import connector from 'src/connector';
import Loader from '../Loader';
import ErrorDisplay from '../ErrorDisplay';
import './App.css';

const store = configureStore();

const useConstructor = (callBack: () => void) => {
  const [hasBeenCalled, setHasBeenCalled] = useState(false);
  if (hasBeenCalled) return;
  callBack();
  setHasBeenCalled(true);
};

const App: React.FC = () => {
  const [error, setError] = useState({
    statusCode: -1,
    messaje: '',
  });
  const [isLoading, setIsLoading] = useState(true);

  useConstructor(async () => {
    try {
      await connector.checkBackendHealth();
    } catch (error_) {
      setError({
        statusCode: error_.statusCode,
        messaje: error_.message,
      });
    } finally {
      setIsLoading(false);
    }
  });

  const isError = !!error.messaje;
  const Component = isError ? (
    <ErrorDisplay message={error.messaje} statusCode={error.statusCode} />
  ) : (
      <Routes />
    );

  return (
    <Provider store={store}>
      <div className="App" data-testid="App">
        {isLoading ? <Loader /> : Component}
      </div>
    </Provider>
  );
};

export default App;
