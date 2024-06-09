<script lang="ts">
    import ChatMessage from '$lib/components/chat/ChatMessage.svelte';
    import ChatMessagesBody from '$lib/components/chat/ChatMessagesBody.svelte';
    import ConversationHeader from '$lib/components/chat/ConversationHeader.svelte';
    import { Alert } from 'flowbite-svelte';
    import MenuLink from "$lib/components/MenuLink.svelte";
    const botAvatarUrl =
        'images/avatar_architect.jpeg';
    const userAvatarUrl =
        'https://images.unsplash.com/photo-1590031905470-a1a1feacbb0b?ixlib=rb-1.2.1&amp;ixid=eyJhcHBfaWQiOjEyMDd9&amp;auto=format&amp;fit=facearea&amp;facepad=3&amp;w=144&amp;h=144';

    const randomGuid =  Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

    type message = {
        content: string;
        type: 'me' | 'other';
        imageUrl?: string | null;
    };

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
            content: "Welcome, I'm expert AI for building chatbots. How can I help?",
            type: 'other'
        }
    ];



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


    async function sendChatMessage() {
        let search = ''
        if (trimmedNewMessage) {
            search = trimmedNewMessage
            messages = [...messages, {content: trimmedNewMessage, type: 'me'}];
            newMessage = '';
        }


        const chatResult = await sendMessage('/api/chat', search);
        if(chatResult.answer) {
            messages = [...messages, { content: chatResult.answer, type: 'other' }];
        }
    }

    function  getAnonGuid() {
        return randomGuid
    }


    async function sendMessage(endpoint: string, message: string) {
        error = null;
        const data = { message };
        isLoadingANewMessage = true;
        const response = await fetch(endpoint, {
            method: 'POST', // Specify the method
            headers: {
                'Content-Type': 'application/json',
                'x-client-anon-guid': getAnonGuid()
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
                content: "Welcome, I'm expert AI for building chatbots. How can I help?",
                type: 'other'
            }
        ];
    }
</script>
<div class="container md-auto">
    <div class="flex-1 p:2 sm:p-6 justify-between flex flex-col h-[calc(100vh-128px)]">
        <MenuLink activeUrl="false" href="/" content="Home" />
        <ConversationHeader username="Architect" jobTitle="Chat AI" avatarUrl={botAvatarUrl} on:message={clearMessages}/>
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
