import { NavItem } from '../model/navItem';

export const navigationItems: NavItem[] = [
  {
    route: 'home/',
    title: 'Home',
    iconClass: 'fa fa-fw fa-home',
  },
  {
    route: 'games/',
    title: 'Games',
    iconClass: 'fa fa-fw fa-gamepad',
    childs: [
      {
        idChild: 'in-progress',
        route: `games/in-progress`,
        title: 'In Progress',
      },
      {
        idChild: 'finished',
        route: 'games/finished',
        title: 'Finished',
      },
    ],
  }
];
