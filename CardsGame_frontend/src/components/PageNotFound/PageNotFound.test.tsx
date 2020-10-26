import React from 'react';
import { cleanup, render } from '@testing-library/react';
import PageNotFound from './PageNotFound';

describe('PageNotFound', () => {
  afterEach(cleanup);

  it('should take a snapshot', () => {
    const { asFragment } = render(<PageNotFound />);
    expect(asFragment()).toMatchSnapshot();
  });

  it('should render a not found message', () => {
    const { getByText } = render(<PageNotFound />);
    expect(getByText('404 Not Found')).toBeInTheDocument();
  });
});
