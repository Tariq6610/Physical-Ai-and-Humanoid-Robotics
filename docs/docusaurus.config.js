// @ts-check
// A list of all available themes: https://docusaurus.io/docs/api/themes/configuration

const {themes} = require('prism-react-renderer');
const lightTheme = themes.github;
const darkTheme = themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI and Humanoid Robotics',
  tagline: 'Building intelligent robots, from code to deployment.',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://physical-ai-robotics-docs.onrender.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'giaic', // Usually your GitHub org/user name.
  projectName: 'physical-ai-and-humanoid-robotics', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          routeBasePath: 'docs',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      metadata: [
        {name: 'keywords', content: 'robotics, AI, physical AI, humanoid robotics, ROS 2, machine learning'},
      ],
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI and Humanoid Robotics',
        logo: {
          alt: 'Physical AI and Humanoid Robotics Logo',
          src: 'img/logo.svg',
        },
        items: [
          {
            to: '/docs/intro',
            label: 'Book',
            position: 'left',
          },
          {
            href: 'https://github.com/Tariq6610/Physical-Ai-and-Humanoid-Robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Book',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Tariq6610/Physical-Ai-and-Humanoid-Robotics',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} GIAIC. Built with Docusaurus.`,
      },
      prism: {
        theme: lightTheme,
        darkTheme: darkTheme,
      },
    }),
};

export default config;
