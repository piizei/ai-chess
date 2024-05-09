<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

</script>
<div class="container md-auto">
  <div class="container mx-auto px-4">
    <h1 class="text-2xl font-bold text-blue-700 mb-2">LLM Prompt Editing</h1>
    <p class="text-lg text-gray-700">Allows users to select and modify prompts from a navigation list. The interface
      provides a form for editing prompt details, with changes saved via a 'Submit' button.</p>
  </div>
  <div class="flex-1 p:2 sm:p-6 min-h-[calc(100vh-128px)]">
    {#if data.success && data.prompts}
      <nav>
        <ul class="flex-col space-y-4">
          <a href={`/prompts/new`} class="block text-white hover:text-white active:text-gray-300">
            <li class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
              Create new Prompt ...
            </li>
          </a>
          {#each data.prompts as prompt}
            <a href={`/prompts/${prompt.id}`} class="block text-white hover:text-white active:text-gray-300">
              <li class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                {prompt.name}
              </li>
            </a>
          {/each}
        </ul>
      </nav>
    {:else}
      <h1>Something went wrong</h1>
      <p>{data.error}</p>
    {/if}
  </div>
</div>

