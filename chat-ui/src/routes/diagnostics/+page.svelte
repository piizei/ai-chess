<script lang="ts">
	import type { PageData } from './$types';
	import {
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		TableSearch
	} from 'flowbite-svelte';
	let searchTerm = '';
	export let data: PageData;

	$: filteredHeaders = data.headers.filter(
		(header) => header.key.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1
	);
</script>

<svelte:head>
	<title>Diagnostics</title>
	<meta name="description" content="Diagnostics" />
</svelte:head>
<TableSearch
	striped={false}
	hoverable={true}
	placeholder="Search by key"
	bind:inputValue={searchTerm}
>
	<TableHead>
		<TableHeadCell>Http Header</TableHeadCell>
		<TableHeadCell>Value</TableHeadCell>
	</TableHead>
	<TableBody>
		{#each filteredHeaders as header}
			<TableBodyRow>
				<TableBodyCell>{header.key}</TableBodyCell>
				<TableBodyCell>{header.value}</TableBodyCell>
			</TableBodyRow>
		{/each}
	</TableBody>
</TableSearch>
