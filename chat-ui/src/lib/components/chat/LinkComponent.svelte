<script>
    export let href = "";
    export let title = undefined;
</script>

<a  {href} {title} class="font-medium text-blue-600 dark:text-blue-500 hover:underline" target="_blank"><slot /></a>
