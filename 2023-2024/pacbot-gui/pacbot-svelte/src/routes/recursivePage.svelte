<script lang="ts">
	import TopAppBar, { Row, Section, Title } from '@smui/top-app-bar';
	import IconButton from '@smui/icon-button';
	import RecursivePage from './recursivePage.svelte';
	import { onMount } from 'svelte';

	export let is_top_level: boolean = false;

	let content_type: '' | 'horizontal' | 'vertical' | 'settings' = '';

	let vertical_split_width = 0;
	let horizontal_split_width = 0;

	let content: any;

	onMount(() => {
		vertical_split_width = content.offsetWidth / 2;
		horizontal_split_width = content.offsetHeight / 2;
	});

	let vertical_move_start = -1;
	let vertical_move_client_start = -1;

	let horizontal_move_start = -1;
	let horizontal_move_client_start = -1;

	function onVerticalPointerDown(e: any) {
		vertical_move_start = vertical_split_width;
		vertical_move_client_start = e.clientX;
	}

	function onHorizontalPointerDown(e: any) {
		horizontal_move_start = horizontal_split_width;
		horizontal_move_client_start = e.clientY;
	}

	function onPointerMove(e: any) {
		if (horizontal_move_start != -1) {
			horizontal_split_width = horizontal_move_start - (horizontal_move_client_start - e.clientY);
		}
		if (vertical_move_start != -1) {
			vertical_split_width = vertical_move_start - (vertical_move_client_start - e.clientX);
		}
	}

	function onPointerUp(e: any) {
		vertical_move_start = -1;
		horizontal_move_start = -1;
	}
</script>

<div id="container" on:pointermove={onPointerMove} on:pointerup={onPointerUp}>
	<div>
		<TopAppBar variant="static" color="primary" dense>
			<Row>
				<Section>
					<IconButton
						class="material-icons"
						on:click={() => (content_type = content_type == 'horizontal' ? '' : 'horizontal')}
						>{content_type == 'horizontal' ? 'close' : 'horizontal_split'}</IconButton
					>
					<IconButton
						class="material-icons"
						on:click={() => (content_type = content_type == 'vertical' ? '' : 'vertical')}
						>{content_type == 'vertical' ? 'close' : 'vertical_split'}</IconButton
					>

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

	<div id="content" bind:this={content}>
		{#if content_type == 'vertical'}
			<div id="content-vertical">
				<div id="content-left" style="width: {vertical_split_width}px">
					<RecursivePage />
				</div>
				<div id="vertical-split-resizer" on:pointerdown={onVerticalPointerDown} />
				<div id="content-right">
					<RecursivePage />
				</div>
			</div>
		{:else if content_type == 'horizontal'}
			<div id="content-horizontal">
				<div id="content-top" style="height: {horizontal_split_width}px">
					<RecursivePage />
				</div>
				<div id="horizontal-split-resizer" on:pointerdown={onHorizontalPointerDown} />
				<div id="content-bottom">
					<RecursivePage />
				</div>
			</div>
		{:else if content_type == 'settings'}
			<p>settings</p>
			<IconButton class="material-icons" on:click={() => (content_type = '')}>close</IconButton>
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

	#vertical-split-resizer {
		width: 5px;
		background-color: gray;
		border: 1px solid black;
		cursor: grab;
	}

	#content-right {
		flex-grow: 1;
	}

	#content-horizontal {
		display: flex;
		flex-direction: column;

		height: 100%;
	}

	#horizontal-split-resizer {
		height: 5px;
		background-color: gray;
		border: 1px solid black;
		cursor: grab;
	}

	#content-bottom {
		flex-grow: 1;
	}
</style>
