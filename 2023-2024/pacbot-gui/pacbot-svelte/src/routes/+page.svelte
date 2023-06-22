<script lang="ts">
	import TopAppBar, { Row, Section, Title as TopTitle } from '@smui/top-app-bar';
	import Paper from '@smui/paper';
	import Fab, { Label, Icon } from '@smui/fab';
	import IconButton from '@smui/icon-button';
	import Drawer, { AppContent, Content, Header, Title, Subtitle } from '@smui/drawer';
	import List, { Item, Separator, Text } from '@smui/list';
	import Accordion, {
		Panel,
		Header as AccHeader,
		Content as AccContent
	} from '@smui-extra/accordion';

	let open = true;
	let active = 'Gray Kittens';

	function setActive(value: string) {
		active = value;
	}
</script>

<div id="container">
	<div>
		<TopAppBar variant="static" color="primary">
			<Row>
				<Section>
					<IconButton class="material-icons" on:click={() => (open = !open)}>menu</IconButton>
					<TopTitle>RIT Pacbot</TopTitle>
				</Section>
				<Section align="end" toolbar>
					<IconButton class="material-icons" aria-label="Open Project Location">folder</IconButton>
				</Section>
			</Row>
		</TopAppBar>
	</div>

	<div id="under-app-bar">
		<div id="drawer-container">
			<Drawer variant="dismissible" bind:open style="position: relative">
				<Content>
					<List>
						<Item
							href="javascript:void(0)"
							on:click={() => setActive('Gray Kittens')}
							activated={active === 'Gray Kittens'}
						>
							<Text>Gray Kittens</Text>
						</Item>
						<Item
							href="javascript:void(0)"
							on:click={() => setActive('A Space Rocket')}
							activated={active === 'A Space Rocket'}
						>
							<Text>A Space Rocket</Text>
						</Item>
						<Item
							href="javascript:void(0)"
							on:click={() => setActive('100 Pounds of Gravel')}
							activated={active === '100 Pounds of Gravel'}
						>
							<Text>100 Pounds of Gravel</Text>
						</Item>
						<Item
							href="javascript:void(0)"
							on:click={() => setActive('All of the Shrimp')}
							activated={active === 'All of the Shrimp'}
						>
							<Text>All of the Shrimp</Text>
						</Item>
						<Item
							href="javascript:void(0)"
							on:click={() => setActive('A Planet with a Mall')}
							activated={active === 'A Planet with a Mall'}
						>
							<Text>A Planet with a Mall</Text>
						</Item>
					</List>
				</Content>
			</Drawer>
		</div>
		<div id="content">
			<div id="accordion">
				<div class="accordion-container">
					<Accordion multiple>
						<Panel>
							<AccHeader>Panel 1</AccHeader>
							<AccContent>
								The content for panel 1.

								<ul>
									<li>Some</li>
									<li>List</li>
									<li>Items</li>
								</ul>
							</AccContent>
						</Panel>
						<Panel>
							<AccHeader>Panel 2</AccHeader>
							<AccContent>The content for panel 2.</AccContent>
						</Panel>
						<Panel>
							<AccHeader>Panel 3</AccHeader>
							<AccContent>
								The content for panel 3.

								<ul>
									<li>Some</li>
									<li>More</li>
									<li>List</li>
									<li>Items</li>
									<li>To</li>
									<li>Show</li>
									<li>Big</li>
									<li>Height</li>
								</ul>
							</AccContent>
						</Panel>
						<Panel>
							<AccHeader>Panel 4</AccHeader>
							<AccContent>The content for panel 4.</AccContent>
						</Panel>
					</Accordion>
				</div>
			</div>
			<div id="drawing-content" />
		</div>
	</div>
</div>

<style>
	#container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		width: 100vw;
	}

	#under-app-bar {
		display: flex;
		flex-direction: row;
		flex-grow: 1;
		z-index: 7;
	}

	#drawer-container {
		position: relative;
		display: flex;
		z-index: 6;
	}

	#content {
		flex-grow: 1;
		display: flex;
	}

	#accordion {
		display: flex;
		flex-direction: column;
	}

	#accordion,
	#drawing-content {
		width: 50%;
	}
</style>
