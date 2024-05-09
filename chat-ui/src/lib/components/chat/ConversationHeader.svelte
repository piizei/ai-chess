
<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export let username = 'User Name';
    export let jobTitle = 'Job Title';
    export let avatarUrl = '';
    function clear() {
        dispatch('message');
    }
</script>

<div class="flex sm:items-center justify-between py-3 border-b-2 border-gray-200">
    <div class="relative flex items-center space-x-4">
        <div class="relative">
            <span class="absolute text-green-500 right-0 bottom-0">
                <svg width="20" height="20">
                    <circle cx="8" cy="8" r="8" fill="currentColor" />
                </svg>
            </span>
            <img
                src={avatarUrl}
                alt=""
                class="w-10 sm:w-16 h-10 sm:h-16 rounded-full"
            />
        </div>
        <div class="flex flex-col leading-tight">
            <div class="text-2xl mt-1 flex items-center">
                <span class="text-gray-700 mr-3">{username}</span>
            </div>
            <span class="text-lg text-gray-600">{jobTitle}</span>
        </div>
    </div>
    <div class="flex items-center space-x-2">
        <button
            type="button"
            on:click={clear}
            class="inline-flex items-center justify-center rounded-lg h-10 w-20 transition duration-500 ease-in-out text-primary-1 font-bold bg-primary-2 hover:bg-accent-5 focus:outline-none"
        > Clear Chat
        </button>
    </div>
</div>
