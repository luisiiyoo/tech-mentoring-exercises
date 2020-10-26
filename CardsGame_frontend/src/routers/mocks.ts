import { NavItem } from '../model/navItem';

export const navBarItemsMock: NavItem[] = [
  {
    route: 'home',
    title: 'Home',
    iconClass: 'fa fa-fw fa-home',
  },
  {
    route: 'engineering',
    title: 'Engineering',
    iconClass: 'fa fa-fw fa-graduation-cap',
    childs: [
      {
        journeyID: '1',
        route: 'basic-back-end',
        title: 'Basic Back-End',
      },
      {
        journeyID: '2',
        route: 'avanced-back-end',
        title: 'Avanced Back-End',
      },
      {
        journeyID: '3',
        route: 'basic-front-end',
        title: 'Basic Front-End',
      },
      {
        journeyID: '4',
        route: 'avanced-front-end',
        title: 'Avanced Front-End',
      },
      {
        journeyID: '5',
        route: 'qa',
        title: 'Q&A',
      },
    ],
  },
];

export const stateMock = {
  main: {
    expand: true,
  },
  topicDetails: {
    visible: false,
    topic: {
      id: -1,
      name: '',
      level: -1,
      shortDescription: '',
      description: '',
      type: '',
      tags: [],
      metadata: {},
      resources: [
        {
          id: -1,
          name: '',
          shortDescription: '',
          description: '',
          url: '',
          complexity: '',
          tags: [],
          metadata: {},
        },
      ],
    },
  },
};
