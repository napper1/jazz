const path = require("path");

module.exports = {
  devServer: {
    writeToDisk: true,
    progress: false,
  },
  outputDir:
    process.env.NODE_ENV === "development"
      ? path.resolve(__dirname, "devdist")
      : path.resolve(__dirname, "dist"),
};
