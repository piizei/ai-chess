<script lang="ts">
	import {
		beforeUpdate,
		afterUpdate
	} from 'svelte';
	let div: HTMLDivElement;
	let autoscroll = false;
	beforeUpdate(() => {
		if (div) {
			const scrollableDistance = div.scrollHeight - div.offsetHeight;
			autoscroll = div.scrollTop > scrollableDistance - 20;
		}
	});

	afterUpdate(() => {
		if (autoscroll) {
			div.scrollTo(0, div.scrollHeight);
		}
	});
</script>
<div bind:this={div}
		id="messages"
		class="shadow-inner bg-slate-100 flex flex-1 scroll-snap-y flex-col space-y-4 p-3 overflow-y-scroll scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter scrollbar-w-2 scrolling-touch"
	>
	<slot/>
</div>


<style>
	.scrollbar-w-2::-webkit-scrollbar {
		width: 0.25rem;
		height: 0.25rem;
	}

	.scrollbar-track-blue-lighter::-webkit-scrollbar-track {
		--bg-opacity: 1;
		background-color: #f7fafc;
		background-color: rgba(247, 250, 252, var(--bg-opacity));
	}

	.scrollbar-thumb-blue::-webkit-scrollbar-thumb {
		--bg-opacity: 1;
		background-color: #edf2f7;
		background-color: rgba(237, 242, 247, var(--bg-opacity));
	}

	.scrollbar-thumb-rounded::-webkit-scrollbar-thumb {
		border-radius: 0.25rem;
	}
</style>
