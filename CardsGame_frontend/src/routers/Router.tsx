import React from 'react';
import { useSelector } from 'react-redux';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { NavItemChild } from 'src/model/navItem';
import { RouterProps, MainComponentProps } from './Router.types';
import PageNotFound from '../components/PageNotFound';
import NavBar from '../components/NavBar';
import HomePage from '../components/HomePage';
import frontConfig from 'src/config/server';
import './Router.css';

const MainComponent: React.FC<MainComponentProps> = ({
  isExpandedNavBar,
  navBarItems,
}) => {
  const routes: NavItemChild[] = [];
  navBarItems.forEach(({ childs = [] }) => {
    childs.forEach((journeyRoute: NavItemChild) => {
      routes.push(journeyRoute);
    });
  });

  return (
    <div
      className="MainComponent"
      data-testid="mainComponent"
      style={{ marginLeft: isExpandedNavBar ? 240 : 64 }}
    >
      <Switch>
        <Route path="/" exact={true} component={() => <HomePage />} />
        <Route path="/home" component={() => <HomePage />} />
        <Route component={() => <PageNotFound />} />
      </Switch>
    </div>
  );
};

const Routes: React.FC<RouterProps> = ({ navBarItems }) => {
  const { main } = useSelector((state) => state);
  const { expand: isExpandedNavBar } = main;

  return (
    <BrowserRouter>
      <Route
        render={({ history }) => (
          <NavBar history={history} navBarItems={navBarItems} navBarTitle={frontConfig.serverName}/>
        )}
      />
      <div className="Container">
        <MainComponent
          isExpandedNavBar={isExpandedNavBar}
          navBarItems={navBarItems}
        />
      </div>
    </BrowserRouter>
  );
};

export default Routes;
