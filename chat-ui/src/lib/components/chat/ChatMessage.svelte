<script lang="ts">
	import { LightBulb } from 'svelte-heros-v2';
	import { marked } from 'marked';
	export let who: 'me' | 'other' = 'me';
	export let content: string[] = [];
	export let citations: string[] = [];
	export let reasoning: string;
	export let avatarUrl = '';
	export let username = 'User Name';

	let showDialog = false;
</script>

<div class="chat-message mt-auto">
	<div class="flex items-end {who === 'other' ? 'justify-start' : 'justify-end'}">
		<!-- The diagnostics dialog -->
		<div
			class="{showDialog
				? ''
				: 'hidden'} fixed left-10 top-10 z-[1055] h-[calc(100%-3rem)] w-[calc(100%-5rem)] overflow-y-auto overflow-x-hidden outline-none bg-grey-4 shadow-2xl rounded-lg scrollbar"
		>
			<h1 class="text-2xl font-semibold underline p-4 text-center bg-grey-3">Reasoning</h1>
			<div class="p-5 border-t border-b border-gray-300">
				{#if reasoning}
					{@html marked(reasoning)}
				{:else}
					<p>No reasoning available</p>
				{/if}
			</div>
			<div class="flex justify-end p-4">
				<button
					class="px-5 py-2 bg-indigo-500 hover:bg-indigo-700 text-white cursor-pointer rounded-md"
					on:click={(_) => (showDialog = false)}>Close</button
				>
			</div>
		</div>
		<div
			class="flex flex-col space-y-2 text-xs sm:text-base max-w-xs sm:max-w-[75%] mx-2 order-2 {who ===
			'other'
				? 'items-start'
				: 'items-end'} drop-shadow-lg"
		>
			{#each content as line}
				<div
					class="px-4 py-2 rounded-lg inline-block {who === 'other'
						? 'bg-gray-200'
						: 'bg-blue-600'} {who === 'other' ? 'text-gray-600' : 'text-white'}"
				>
					{#if reasoning}
						<div class="flex justify-end p-2">
							<LightBulb
								class="hover:bg-gray-100 hover:cursor-pointer"
								on:click={(_) => (showDialog = true)}
							/>
						</div>
					{/if}
					<span>{@html marked(line)}</span>
					{#if citations && citations.length}
						<div>
							<h3 class="font-semibold">Citations:</h3>
							<ol class="list-decimal list-inside">
								{#each citations as citation}
									<li><a class="bg-blue-600 text-white" href="{citation}">{citation}</a></li>
								{/each}
							</ol>
						</div>
					{/if}
				</div>
			{/each}
		</div>
		<img
			src={avatarUrl}
			alt={username}
			class="w-6 h-6 rounded-full {who === 'other' ? 'order-1' : 'order-2'}"
		/>
	</div>
</div>
