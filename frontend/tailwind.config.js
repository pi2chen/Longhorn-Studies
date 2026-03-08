/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./components/**/*.{js,jsx,ts,tsx}", "./app/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Primary
        'white': '#FFFFFF',
        'burnt-orange': '#BF5700',  // study spot building names/abbrevs
        'main-text': '#333F48',     // Used with all main texts
        'card-border': '#BAC1CC',   // All card borders
        'gray-text': '#94A3B8',     // Gray text

        // Opaque colors
        // Note: You can also use Tailwind's built-in opacity modifier like `bg-brand-orange/50` 
        'active-filter': 'rgba(191, 87, 0, 0.5)',     // #BF5700 at 0.5 opacity
        'saved-bg': 'rgba(214, 210, 196, 0.5)',       // #D6D2C4 at 0.5 opacity

        // Hours Color States
        'status-open': '#579D42',
        'status-closing': '#F8971F',
        'status-closed': '#D10000',
      },
      fontFamily: {
        roboto: ['"Roboto Flex"', 'sans-serif'],
      },
      fontSize: {
        'heading': '25.63px',         // Heading
        'details-header': '22.78px',  // Study Spot Details Header
        'filter-header': '20.25px',   // Filter Header
        'base-16': '16px',            // Filter Option, Details, Search Bar
        'spot-name': '14.22px',       // Study Spot Name, Details
        'status': '12.64px',          // Open Status + Distance
        'tag': '10px',                // Tags
      }
    },
  },
  presets: [require("nativewind/preset")],
  plugins: [],
}