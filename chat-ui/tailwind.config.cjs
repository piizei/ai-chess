const config = {
	content: ['./src/**/*.{html,js,svelte,ts}', './node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}'],

	plugins: [require('flowbite/plugin')],

	darkMode: 'class',

	theme: {
		fontFamily: {
			sans: ['Noto Sans'],
			serif: ['Noto Serif'],
		},
		extend: {
			colors: {
				// flowbite-svelte
				primary: {
					50: '#FFF5F2',
					100: '#FFF1EE',
					200: '#FFE4DE',
					300: '#FFD5CC',
					400: '#FFBCAD',
					500: '#FE795D',
					600: '#EF562F',
					700: '#EB4F27',
					800: '#CC4522',
					900: '#A5371B'
				},
				'dark-blue': '#022366',
				'light-blue': '#1482FA',
				'extra-light-blue': '#BDE3FF',
				neutral: {
					1: '#FAC9B5',
					2: '#FAD6C7',
					3: '#FFE8DE',
					4: '#FFF7F5',
				},
				grey: {
					1: '#544F4F',
					2: '#706B69',
					3: '#C2BAB5',
					4: '#DBD6D1',
					5: '#F5F5F2',
				},
				black: '#000000',
				white: '#FFFFFF',
			}
		},
		container: {
			center: true,
		}
	}
};

module.exports = config;
