<script lang="ts">
	import Accordion, { Panel, Header, Content } from '@smui-extra/accordion';
</script>

<div class="accordion-container">
	<Accordion>
		<Panel>
			<Header>Panel 1</Header>
			<Content />
		</Panel>
		<Panel>
			<Header>Panel 2</Header>
			<Content>The content for panel 2.</Content>
		</Panel>
		<Panel>
			<Header>Panel 3</Header>
			<Content />
		</Panel>
		<Panel>
			<Header>Panel 4</Header>
			<Content />
		</Panel>
	</Accordion>
</div>
