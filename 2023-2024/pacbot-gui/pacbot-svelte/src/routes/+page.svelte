<script lang="ts">
	import RecursivePage from './recursivePage.svelte';
	import { onMount } from 'svelte';
	import { websocketClient } from './websocket';
	import { WEBSOCKET_SERVER_PORT } from './websocketMessages';

	onMount(() => {
		let wsUrl: string;
		if (typeof window !== 'undefined') {
			const wsPort = WEBSOCKET_SERVER_PORT;
			const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
			wsUrl = `${protocol}//${window.location.hostname}:${wsPort}`;
		} else {
			console.error(
				'WebSocket client cannot be used because the current environment does not support it'
			);
			wsUrl = ''; // or provide a default URL if appropriate
		}
		websocketClient.setUrl(wsUrl);
		websocketClient.connect();
	});
</script>

<div>
	<RecursivePage is_top_level={true} />
</div>

<style>
	* {
		height: 100vh;
	}
</style>
