<script lang="ts">
	import ChatMessage from '$lib/components/chat/ChatMessage.svelte';
	import ChatMessagesBody from '$lib/components/chat/ChatMessagesBody.svelte';
	import ConversationHeader from '$lib/components/chat/ConversationHeader.svelte';
	import { Alert } from 'flowbite-svelte';
	import { onDestroy, onMount } from 'svelte';
	import MenuLink from '$lib/components/MenuLink.svelte';
	const botAvatarUrl =
			'images/chess_bot.jpeg';
	const userAvatarUrl =
			'https://images.unsplash.com/photo-1590031905470-a1a1feacbb0b?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144';

	type message = {
		content: string;
		type: 'me' | 'other';
		imageUrl?: string | null;
	};

	type GameStatus = {
		timestamp: string;
		starts: string;
		is_over: boolean;
		winner: null | string;
		moves: string[];
		current_fen: string;
		game_id: string;
		last_move_at: string;
		last_move_described: string;
		turn_duration_seconds: number;
		last_move: null | string;
		last_move_img: undefined| null | string;
	}
	let error: string | null = null;
	let isLoadingANewMessage = false;

	type chatMessage = {
		content: message[];
		username: string;
		who: 'other' | 'me';
		avatarUrl?: string;
		imageUrl?: string | null;
	};

	let messages: message[] = [
		{
			content: "Welcome player.<br>This is co-operative chess.<br/>When it's white's turn, you can enter a move (in free text format).<br/>Most voted move will be executed after 3 minutes.",
			type: 'other'
		}
	];

	let gameStatus: GameStatus | null


	let newMessage = '';
	$: trimmedNewMessage = newMessage.trim();
	$: chatMessagesFromMessagesWithGroupedContentPerUser = messages.reduce((acc, message) => {
		if (acc && acc.length > 0 && acc[acc.length - 1].who === message.type) {
			acc[acc.length - 1].content.push(message);
		} else {
			// find if any message has imageUrl:
			const msg = {
				content: [message],
				who: message.type,
				username: message.type === 'other' ? 'Chat GPT' : 'User Name',
				avatarUrl: message.type === 'other' ? botAvatarUrl : userAvatarUrl,
			}
			acc.push(msg);
		}
		return acc;
	}, [] as chatMessage[]);
	// Check game status from server each 5 secs.
	let gameStartTime: Date | null = null;
	const interval = async() => {
		const result = await updateStatus();
		if (!gameStartTime) {
			gameStartTime = new Date(result.starts);
		}
		if (gameStatus?.timestamp !== result.timestamp) {
			gameStatus = result;
			const isBeforeGameStart = !result.last_move_described && new Date() < gameStartTime;
			if (isBeforeGameStart) {
				const start = gameStartTime.toLocaleTimeString();
				messages = [...messages, { content: `Game has not started yet<br>New game starts at ${start}`, type: 'other' }];
				messages = [...messages, { content: `You can vote already for first move`, type: 'other' }];
				return;
			} else if (!result.last_move_described) {
				messages = [...messages, { content: `Game has started`, type: 'other' }];
				messages = [...messages, { content: `You can vote for first move`, type: 'other' }];
				return;
			}
			messages = [...messages, { content: result.last_move_described, imageUrl: '/api/board/' + result.last_move_img ,  type: 'other' }];
			if (result.current_fen && isWhiteTurn(result.current_fen)) {
				messages = [...messages, { content: `It's your turn`, type: 'other' }];
			}
			console.log(messages);
		}
	}
	const intervalNr = setInterval(async () => {
		interval();
	}, 10000);

	onMount(async () => {
		interval();
	});

	onDestroy(() => clearInterval(intervalNr));

	async function sendChatMessage() {
		let search = ''
		if (trimmedNewMessage) {
			search = trimmedNewMessage
			messages = [...messages, {content: trimmedNewMessage, type: 'me'}];
			newMessage = '';
		}


		const chatResult = await sendMessage('/api/vote', search);
		if(chatResult.message) {
			messages = [...messages, { content: chatResult.message, type: 'other' }];
		}
	}


	async function updateStatus(): Promise<GameStatus> {
		const response = await fetch('/api/status', {
			method: 'GET', // Specify the method
			headers: {
				'Content-Type': 'application/json'
			}
		});
		const result = await response.json();
		if(result.error) {
			console.log(result.error)
			error = JSON.stringify(result.error);
		} else {
			error = null;
		}
		return result

	}

	async function sendMessage(endpoint: string, message: string) {
		error = null;
		const data = { message };
		isLoadingANewMessage = true;
		const response = await fetch(endpoint, {
			method: 'POST', // Specify the method
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});
		const result = await response.json();
		if(result.error) {
			console.log(result.error)
			error = JSON.stringify(result.error);
		}
		isLoadingANewMessage = false;
		return result

	}

	async function clearMessageSession() {
		await fetch('/api/chat/clear', {
			method: 'POST', // Specify the method
			headers: {
				'Content-Type': 'application/json' // Specify the content type
			}
		});
	}

	function clearMessages() {
		clearMessageSession()
		messages = [
			{
				content: 'Welcome player',
				type: 'other'
			}
		];
	}
	function isWhiteTurn(fen: string): boolean {
		const parts = fen.split(" ");
		if (parts.length < 2) {
			return false;
		}
		const playerToMove = parts[1];
		return playerToMove === 'w';
	}
</script>
<div class="container md-auto">
	<div class="flex-1 p:2 sm:p-6 justify-between flex flex-col h-[calc(100vh-64px)]">
		<MenuLink activeUrl="false" href="/" content="Home" />
		<ConversationHeader username="Chessy" jobTitle="Chess AI" avatarUrl={botAvatarUrl} on:message={clearMessages}/>
		<ChatMessagesBody>
			{#each chatMessagesFromMessagesWithGroupedContentPerUser as chatMessage}
				<ChatMessage {...chatMessage} />
			{/each}
			{#if isLoadingANewMessage}
				<div class="flex justify-center items-center">
					<div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-900"></div>
				</div>
			{/if}
			{#if error}
				<div class="flex justify-center items-center">
					<Alert>
						<span class="font-medium">Upps!</span>
						{error}
					</Alert>
				</div>
			{/if}
		</ChatMessagesBody>
		<div class="border-t-1 border-gray-200 px-0 pt-0 mb-2 sm:mb-0">
			<div class="relative flex">
				<input
						type="text"
						name="message"
						placeholder="Write your message!"
						bind:value={newMessage}
						on:keydown={(event) => event.key === 'Enter' && sendChatMessage()}
						class="w-full text-black focus:outline-none focus:placeholder-gray-400 text-primary-3 placeholder-gray-600 pl-3 bg-gray-100 rounded-md py-3"
				/>
				<div class="absolute right-0 items-center inset-y-0 hidden sm:flex">
					<button
							type="button"
							on:click={sendChatMessage}
							class="inline-flex items-center justify-center rounded-lg px-4 py-3 transition duration-500 ease-in-out text-gray-700 bg-primary-2 hover:bg-accent-5 focus:outline-none"
					>
						<span class="font-bold">Send</span>
						<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								class="h-6 w-6 ml-2 transform rotate-90"
						>
							<path
									d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"
							/>
						</svg>
					</button>
				</div>
			</div>
		</div>
	</div>
</div>
