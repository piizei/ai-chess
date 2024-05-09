<script lang="ts">
	import MenuLink from '$lib/components/MenuLink.svelte';
	import logo from '$lib/images/logo.png';

	export let activeUrl: string;
</script>

<header>
	<nav class="px-6 py-8 mx-auto md:flex md:justify-between md:items-center">
		<div class="">
			<a class="text-xl font-bold md:text-2xl hover:text-primary-3" href="/">
				<span class="inline-flex items-center">
					<span class="px-4 text-xl">GPT + Enterprise data | IT OT Knowledge Management</span>
				</span>
			</a>
		</div>

		<!-- Mobile Menu open: "block", Menu closed: "hidden" -->
		<div
			class="flex-col mt-8 space-y-4 md:flex md:space-y-0 md:flex-row md:items-center md:space-x-10 md:mt-0 flex"
		>
			<MenuLink {activeUrl} href="/" content="Home" />
			<MenuLink {activeUrl} href="/diagnostics" content="Diagnostics" />
			<MenuLink {activeUrl} href="/prompts" content="Prompts" />
			<MenuLink {activeUrl} href="/about" content="About Us" />
		</div>
	</nav>
</header>
