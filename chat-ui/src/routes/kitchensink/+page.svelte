<script>
	import { AccordionItem, Accordion, Label, Input, Helper, Button, Tabs, TabItem, Timeline, TimelineItem, Progressbar } from 'flowbite-svelte';
	import { ArrowRightOutline } from 'flowbite-svelte-icons';

	const items = Array(3);

	const open_all = () => items.forEach((_, i) => (items[i] = true));
	const close_all = () => items.forEach((_, i) => (items[i] = false));
</script>

<div class="mb-6">
	<Label for="success" color="green" class="block mb-2">Your name</Label>
	<Input id="success" color="green" placeholder="Success input" />
	<Helper class="mt-2" color="green">
	  <span class="font-medium">Well done!</span>
	  Some success message.
	</Helper>
  </div>
  <div class="mb-6">
	<Label for='error' color='red' class='block mb-2'>Your name</Label>
	<Input id='error' color='red' placeholder="Error input" />
	<Helper class='mt-2' color='red'><span class="font-medium">Not so well done!</span> Some error message.</Helper>
  </div>

  
<Button>Default</Button>
<Button color="alternative">Alternative</Button>
<Button color="dark">Dark</Button>
<Button color="light">Light</Button>
<Button color="blue">Blue</Button>
<Button color="green">Green</Button>
<Button color="red">Red</Button>
<Button color="yellow">Yellow</Button>
<Button color="purple">Purple</Button>

<Button on:click={open_all}>Open all</Button>
<Button on:click={close_all}>Close all</Button>
<Accordion multiple>
	<AccordionItem bind:open={items[0]}>
		<span slot="header">My Header 1</span>
		<p class="mb-2 text-gray-500 dark:text-gray-400">
			Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
			explicabo ...
		</p>
		<p class="text-gray-500 dark:text-gray-400">
			Check out this guide to learn how to <a
				href="/"
				target="_blank"
				rel="noreferrer"
				class="text-blue-600 dark:text-blue-500 hover:underline"
			>
				get started
			</a>
			and start developing websites even faster with components on top of Tailwind CSS.
		</p>
	</AccordionItem>
	<AccordionItem bind:open={items[1]}>
		<div slot="header">My Header 2</div>
		<p class="mb-2 text-gray-500 dark:text-gray-400">
			Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
			explicabo ...
		</p>
		<p class="mb-2 text-gray-500 dark:text-gray-400">
			Lorem ipsum dolor sit amet, consectetur adipisicing elit. Illo ab necessitatibus sint
			explicabo ...
		</p>
		<p class="mb-2 text-gray-500 dark:text-gray-400">Learn more about these technologies:</p>
	</AccordionItem>
	<AccordionItem bind:open={items[2]}>
		<div slot="header">My Header 3</div>
		<p>Something more</p>
	</AccordionItem>
</Accordion>
  
  <Tabs>
	<TabItem open>
	  <span slot="title">Profile</span>
	  <Timeline>
		<TimelineItem title="Application UI code in Tailwind CSS" date="February 2022">
		  <p class="mb-4 text-base font-normal text-gray-500 dark:text-gray-400">Get access to over 20+ pages including a dashboard layout, charts, kanban board, calendar, and pre-order E-commerce & Marketing pages.</p>
		  <Button color="alternative">
			Learn more
			<ArrowRightOutline class="ml-2 w-3 h-3" />
		  </Button>
		</TimelineItem>
		<TimelineItem title="Application UI code in Tailwind CSS" date="March 2022">
		  <p class="text-base font-normal text-gray-500 dark:text-gray-400">All of the pages and components are first designed in Figma and we keep a parity between the two versions even as we update the project.</p>
		</TimelineItem>
		<TimelineItem title="Application UI code in Tailwind CSS" date="April 2022">
		  <p class="text-base font-normal text-gray-500 dark:text-gray-400">Get started with dozens of web components and interactive elements built on top of Tailwind CSS.</p>
		</TimelineItem>
	  </Timeline>
	</TabItem>
	<TabItem>
	  <span slot="title">Dashboard</span>
	  <p class="text-sm text-gray-500 dark:text-gray-400">
		<b>Dashboard:</b>
		Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
	  </p>
	</TabItem>
	<TabItem>
	  <span slot="title">Settings</span>
	  <p class="text-sm text-gray-500 dark:text-gray-400">
		<b>Settings:</b>
		Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
	  </p>
	</TabItem>
	<TabItem>
	  <span slot="title">Users</span>
	  <p class="text-sm text-gray-500 dark:text-gray-400">
		<b>Users:</b>
		Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
	  </p>
	</TabItem>
  </Tabs>

  <div class="my-4">
	<div class="mb-1 text-base font-medium dark:text-white">Small</div>
	<Progressbar progress="50" size="h-1.5" />
  </div>
  
  <div class="my-4">
	<div class="mb-1 text-base font-medium dark:text-white">Default</div>
	<Progressbar progress="50" size="h-2.5" />
  </div>
  
  <div class="my-4">
	<div class="mb-1 text-lg font-medium dark:text-white">Large</div>
	<Progressbar progress="50" size="h-4" />
  </div>
  
  <div class="my-4">
	<div class="mb-1 text-lg font-medium dark:text-white">Extra Large</div>
	<Progressbar progress="50" size="h-6" />
  </div>