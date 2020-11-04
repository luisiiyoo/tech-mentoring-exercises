import { NavItem } from '../model/navItem';

export const ROUTES = {
  HOME: 'home',
  GAMES: 'games',
  GAMES_FINISHED: 'games/finished',
  GAMES_IN_PROGRESS: 'games/in-progress'
}

export const navigationItems: NavItem[] = [
  {
    route: ROUTES.HOME,
    title: 'Home',
    iconClass: 'fa fa-fw fa-home',
  },
  {
    route: ROUTES.GAMES,
    title: 'Games',
    iconClass: 'fa fa-fw fa-gamepad',
    childs: [
      {
        idChild: ROUTES.GAMES_IN_PROGRESS,
        route: ROUTES.GAMES_IN_PROGRESS,
        title: 'In Progress',
      },
      {
        idChild: ROUTES.GAMES_FINISHED,
        route: ROUTES.GAMES_FINISHED,
        title: 'Finished',
      },
    ],
  }
];
