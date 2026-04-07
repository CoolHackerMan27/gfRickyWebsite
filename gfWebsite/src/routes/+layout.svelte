<script lang="ts">
	import favicon from '$lib/assets/star1.png';

	let { children } = $props();

	import { onMount } from 'svelte';

	onMount(async () => {
		// This makes wired-elements available to EVERY page
		// purely on the client-side.
		await import('wired-elements');
  });

</script>

<svelte:head>
	<title>Rickify</title>
	<link rel="icon" type="image/svg+xml" href={favicon} />
</svelte:head>

{@render children()}

<style>
	:global(html, body) {
		margin: 0;
		padding: 0;
		width: 100%;
		min-height: 100%;
		background: #f6ebc6;
	}

	:global(body) {
		overflow-x: hidden;
	}
</style>
