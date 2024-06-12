<script lang="ts">
	import '../app.postcss';
	import { fade } from 'svelte/transition';
	import type { LayoutData } from './$types';

	export let data: LayoutData;
</script>
<div
		class="leading-normal tracking-normal text-white gradient"
		style="font-family: 'Source Sans Pro', sans-serif;"
>

{#key data.currentRoute}
	<main class="" in:fade={{ duration: 150, delay: 150 }} out:fade={{ duration: 150 }}>
		<slot />
	</main>
{/key}

</div>
<style>
	.gradient {
		@apply bg-gradient-to-r from-pink to-yellow;
	}
</style>
