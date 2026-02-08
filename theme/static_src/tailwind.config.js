/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../templates/**/*.html",        // theme/templates/...
    "../../templates/**/*.html",     // project-level templates (if you have)
    "../../**/templates/**/*.html",  // other apps templates
  ],
  theme: {
    extend: {},
  },
  corePlugins: {
    preflight: false, // IMPORTANT: keep Bootstrap styling stable
  },
  plugins: [],
};
