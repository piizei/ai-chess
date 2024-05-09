<script lang="ts">
    export let activeUrl: string;
    export let href: string;
    export let content: string
</script>

<a class="{activeUrl == href ? "text-grey-3" : "text-grey-1"} hover:text-blue-400" href={href}>{content}</a>

