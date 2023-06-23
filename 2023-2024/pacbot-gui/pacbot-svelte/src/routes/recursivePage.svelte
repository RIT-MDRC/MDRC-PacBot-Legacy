<script lang="ts">
	import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
	import IconButton from '@smui/icon-button';
	import RecursivePage from './recursivePage.svelte';

	export let is_top_level: boolean = false;

	let content_type: '' | 'horizontal' | 'vertical' | 'settings' = '';
</script>

<div id="container">
	<div>
		<TopAppBar variant="static" color="primary" dense>
			<Row>
				<Section>
					{#if content_type == ''}
						<IconButton class="material-icons" on:click={() => (content_type = 'horizontal')}
							>horizontal_split</IconButton
						>
						<IconButton class="material-icons" on:click={() => (content_type = 'vertical')}
							>vertical_split</IconButton
						>
					{:else}
						<IconButton class="material-icons" on:click={() => (content_type = '')}
							>close</IconButton
						>
					{/if}

					{#if is_top_level}
						<Title>RIT Pacbot</Title>
					{/if}
				</Section>
				<Section align="end" toolbar>
					{#if content_type != 'horizontal' && content_type != 'vertical'}
						<IconButton
							class="material-icons"
							on:click={() => (content_type = 'settings')}
							aria-label="Settings">settings</IconButton
						>
					{/if}
					{#if is_top_level}
						<IconButton class="material-icons" aria-label="Open Project Location">folder</IconButton
						>
					{/if}
				</Section>
			</Row>
		</TopAppBar>
	</div>

	<div id="content">
		{#if content_type == 'vertical'}
			<div id="content-vertical">
				<div id="content-left">
					<RecursivePage />
				</div>
				<div id="content-right">
					<RecursivePage />
				</div>
			</div>
		{:else if content_type == 'horizontal'}
			<div id="content-horizontal">
				<div id="content-top">
					<RecursivePage />
				</div>
				<div id="content-bottom">
					<RecursivePage />
				</div>
			</div>
		{:else if content_type == 'settings'}
			<p>settings</p>
		{:else if content_type == ''}
			<p>hello</p>
		{/if}
	</div>
</div>

<style>
	#container {
		display: flex;
		flex-direction: column;

		height: 100%;
	}

	#content {
		flex-grow: 1;
		height: 100%;
	}

	#content-vertical {
		display: flex;
		flex-direction: row;

		width: 100%;
		height: 100%;
	}

	#content-left {
		width: 50%;
	}

	#content-right {
		flex-grow: 1;
	}

	#content-horizontal {
		display: flex;
		flex-direction: column;

		height: 100%;
	}

	#content-top {
		height: 50%;
	}

	#content-bottom {
		flex-grow: 1;
	}
</style>
