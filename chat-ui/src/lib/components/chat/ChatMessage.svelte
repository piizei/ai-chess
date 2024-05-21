<script lang="ts">
	import { marked } from 'marked';
	export let who: 'me' | 'other' = 'me';
	export let content: {content: string, imageUrl: string}[] = [];
	export let avatarUrl = '';
	export let username = 'User Name';
</script>

<div class="chat-message mt-auto">
	<div class="flex items-end {who === 'other' ? 'justify-start' : 'justify-end'}">
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
					<span>{@html marked(line.content)}</span>

				</div>
				{#if line.imageUrl}
					<img src={line.imageUrl} alt="board" />
				{/if}
			{/each}
		</div>
		<img
			src={avatarUrl}
			alt={username}
			class="w-6 h-6 rounded-full {who === 'other' ? 'order-1' : 'order-2'}"
		/>
	</div>
</div>
