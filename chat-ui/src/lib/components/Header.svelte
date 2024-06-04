<script lang="ts">
	import MenuLink from '$lib/components/MenuLink.svelte';
	export let activeUrl: string;
</script>

<nav class="px-6 py-8 mx-auto md:flex md:justify-between md:items-center">
	<div class="">
		<a class="text-xl font-bold md:text-2xl hover:text-primary-3" href="/">
<span class="inline-flex items-center">
</span>
		</a>
	</div>

	<!-- Mobile Menu open: "block", Menu closed: "hidden" -->
	<div
			class="flex-col mt-8 space-y-4 md:flex md:space-y-0 md:flex-row md:items-center md:space-x-10 md:mt-0 flex"
	>
		<MenuLink {activeUrl} href="/" content="Home" />
		<MenuLink {activeUrl} href="/chess" content="Chess" />
		<MenuLink {activeUrl} href="/architect" content="Architect" />
	</div>
</nav>
