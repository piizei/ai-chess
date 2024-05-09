<script lang="ts">
  import type { ActionData, PageData } from "./$types";
  import { Input, Label, Checkbox, Button, Textarea } from "flowbite-svelte";
  import { ArrowLeft } from "svelte-heros-v2";
  import type { PromptFragment } from "$lib/prompt";
  import type { ActionResult } from "@sveltejs/kit";
  import { applyAction, deserialize } from "$app/forms";
  import { invalidateAll } from "$app/navigation";

  function handleBeforeUnload(event: BeforeUnloadEvent) {
    if (isDirty) {
      event.preventDefault();
      event.returnValue = "You have unsaved changes. Are you sure you want to leave?";
      return event.returnValue;
    }
  }

  function addFragment(fragment: PromptFragment = { id: "", name: "", content: "" }) {
    isDirty = true;
    data.prompt.fragments = [...data.prompt.fragments || [], fragment];
  }

  function unassignFragment(index: number) {
    isDirty = true;
    data.prompt.fragments = data.prompt.fragments.filter((_, i) => i !== index);
  }


  async function handleSubmit(event: { currentTarget: EventTarget & HTMLFormElement }) {
    isDirty = false;
    const data = new FormData(event.currentTarget);

    const response = await fetch(event.currentTarget.action, {
      method: "POST",
      body: data
    });

    const result: ActionResult = deserialize(await response.text());

    if (result.type === "success") {
      // rerun all `load` functions, following the successful update
      await invalidateAll();
    }

    applyAction(result);
  }

  async function deleteFragmentFromAPI(fragment: PromptFragment) {
    let result = await fetch(`/api/fragments/${fragment.id}`, { method: "DELETE" });
    let resultJson = await result.json();
    console.log(resultJson);
    console.log(fragment)
    if (resultJson.error) {
      form.error = resultJson.error;
    } else {
      console.log('was here')
      data.prompt.fragments = data.prompt.fragments.filter(f => f.id !== fragment.id);
    }
  }


  export let data: PageData;
  export let form: ActionData;
  let isDirty = false;
  let selectedFragmentIndex: number;
  $: isNew = data.prompt.id === "new";
  $: prompt = data.prompt;
  $: id = isNew ? "" : prompt.id;
  $: fragments = data.prompt.fragments || [];
  $: unusedFragments = data.fragments.filter(fragment => !fragments.find(f => f.id === fragment.id));
  $: selectedFragment = unusedFragments[selectedFragmentIndex] || { id: "", name: "", content: "" };

</script>
<svelte:window on:beforeunload={handleBeforeUnload}></svelte:window>
<div class="container md-auto flex flex-col items-start bg-gray-100 border border-gray-200 rounded-lg p-4 shadow-sm">
  <div class="flex-1 p:2 sm:p-6 min-h-[calc(100vh-128px)]">
    <div>
      <a href="/prompts"
         class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
        <ArrowLeft />
        Back
      </a>
    </div>
    {#if form}
      {#if form.error || form.success}
        {#if form.success}
          <div class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50" role="alert">
            <span class="font-medium">Successfully saved!</span>
          </div>
        {:else }
          <div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50" role="alert">
            <span class="font-medium">Failed to save!</span> {form.error}
          </div>
        {/if}
      {/if}
    {/if}
    <form method="POST" action="?/save" on:submit|preventDefault={handleSubmit}>
      <div class="p-2">
        <Label>
          ID: {id || "new"}
          <Input type="text" name="id" bind:value={id} readonly class="hidden" />
        </Label>
      </div>
      <div class="p-2">
        <Label>
          Name:
          <Input type="text" name="name" bind:value={prompt.name} />
        </Label>
      </div>
      <div class="p-2">
        <Label>
          Current:
          <Checkbox name="current" bind:checked={prompt.current} />
        </Label>
      </div>
      <ol class="border border-gray-200 p-4">
        {#each fragments as fragment, index}
          <li draggable="true" class="border-b border-gray-300 p-2 ${index % 2 === 0 ? 'bg-gray-100' : 'bg-gray-200'}">
            <div>
              <Label>
                <h3>{index + 1}</h3>
                ID: {fragment.id}
                <Input name={`fragments[${index}][id]`} type="text" bind:value={fragment.id} readonly class="hidden" />
              </Label>
            </div>
            <div>
              <Label>
                Name:
                <Input type="text" name={`fragments[${index}][name]`} bind:value={fragment.name} />
              </Label>
            </div>
            <div>
              <Label>
                Content:
                <Textarea rows="20" cols="60" name={`fragments[${index}][content]`}
                          bind:value={fragment.content} class="resize-y text-sm"></Textarea>
              </Label>
            </div>
            <div>
              <button
                class="bg-yellow-400 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded"
                on:click|preventDefault={() => unassignFragment(index)}
              >
                Unassign Fragment '{fragment.name}'
              </button>

              <button
                class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                on:click|preventDefault={() => deleteFragmentFromAPI(fragment)}
              >
                Delete Fragment '{fragment.name}'
              </button>
            </div>
          </li>
        {/each}

        <li class="p-2 border-b border-gray-300">
          <select name="fragments_not_in_prompt" bind:value={selectedFragmentIndex}>
            {#each unusedFragments as fragment, index}
              <option value={index}>{fragment.name}</option>
            {/each}
          </select>
          <button
            on:click|preventDefault={() => addFragment(selectedFragment)}
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition-colors duration-200"
          >
            Add Fragment: '{selectedFragment.name}'
          </button>
        </li>
        <li class="p-2">
          <button
            on:click|preventDefault={() => addFragment()}
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition-colors duration-200"
          >
            Create new Fragment....
          </button>
        </li>
      </ol>
      <div class="p-2">
        <Button type="submit" class="bg-green-500 hover:bg-green-700 text-white text-xl">
          Save{isDirty ? '!' : ''}</Button>
      </div>
    </form>
    {#if !isNew}
      <form method="POST" action="?/delete" on:submit|preventDefault={handleSubmit}>
        <div class="p-2">
          <Button type="submit" class="bg-red-500 hover:bg-red-700 text-white text-xl">
            Delete
          </Button>
        </div>
      </form>
    {/if}
  </div>
</div>