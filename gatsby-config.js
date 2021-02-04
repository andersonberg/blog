module.exports = {
  plugins: [
    `gatsby-plugin-sharp`,
    {
      resolve: `gatsby-theme-blog`,
      options: {},
    },
    {
      resolve: `gatsby-transformer-remark`,
      options: {
        plugins: [
          {
            resolve: `gatsby-remark-images`,
            options: {
              maxWidth: 768,
              maxLength: 1024,
            },
          },
        ],
      },
    },
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        path: `${__dirname}/content/posts/images`,
      },
    }
  ],
  // Customize your site metadata:
  siteMetadata: {
    title: `Anderson Berg`,
    author: `Anderson Berg`,
    description: `Anderson Berg Blog`,
    social: [
      {
        name: `twitter`,
        url: `https://twitter.com/berg_pe`,
      },
      {
        name: `github`,
        url: `https://github.com/andersonberg`,
      },
    ],
  },
}
