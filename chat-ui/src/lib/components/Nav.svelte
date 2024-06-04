<script lang="ts">
    import { clickOutside, clickOutsideAction } from '$lib/actions/clickOutside'
    import Button from './Button.svelte'

    let y: number
    let navFloat = false
    $: navFloat = y > 10

    let showMenu = false
    const toggleMenu = () => (showMenu = !showMenu)
    let hambugerEl

    const onClickOutsideAction = ({ target }) => {
        if (!hambugerEl.contains(target)) showMenu = false
    }
    const onClickOutside = ({ detail: { event: { target } } }) => {
        if (!hambugerEl.contains(target)) showMenu = false
    }
</script>

<svelte:window bind:scrollY={y} />
<!--Nav-->
<nav
        id="header"
        class={`
  fixed w-full z-30 top-0 text-white
  ${navFloat && 'bg-white'}
  `}
>
    <div class="w-full container mx-auto flex flex-wrap items-center justify-between mt-0 py-2">
        <div class="pl-4 flex items-center">
            <!-- svelte-ignore a11y-invalid-attribute -->
            <a
                    class:text-gray-800={navFloat}
                    class:text-white={!navFloat}
                    class="no-underline hover:no-underline font-bold text-2xl lg:text-4xl"
                    href="#"
            >
                <!--Icon from: http://www.potlabicons.com/ -->

                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none"><style>@keyframes pulsate{0%,to{transform:scale(1)}50%{transform:scale(.9)}}</style><g style="animation:pulsate .5s ease-in-out infinite both;transform-origin:center center" stroke-width="1.5"><path class="plane-take-off" stroke="#0A0A30" d="M11.515 6.269l.134.132a.5.5 0 00.702 0l.133-.132A4.44 4.44 0 0115.599 5c.578 0 1.15.112 1.684.33a4.41 4.41 0 011.429.939c.408.402.733.88.954 1.406a4.274 4.274 0 010 3.316 4.331 4.331 0 01-.954 1.405l-6.36 6.259a.5.5 0 01-.702 0l-6.36-6.259A4.298 4.298 0 014 9.333c0-1.15.464-2.252 1.29-3.064A4.439 4.439 0 018.401 5c1.168 0 2.288.456 3.114 1.269z"/><path stroke="#265BFF" stroke-linecap="round" stroke-linejoin="round" d="M15.5 7.5c.802.304 1.862 1.43 2 2"/></g></svg>
                LIVE DEMO
            </a>
        </div>
        <div bind:this={hambugerEl} class="block lg:hidden pr-4">
            <button
                    on:click={toggleMenu}
                    id="nav-toggle"
                    class="flex items-center p-1 text-pink-800 hover:text-gray-900 focus:outline-none focus:shadow-outline transform transition hover:scale-105 duration-300 ease-in-out"
            >
                <svg class="fill-current h-6 w-6" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <title>Menu</title>
                    <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
                </svg>
            </button>
        </div>
        <!-- use:clickOutsideAction={onClickOutsideAction} -->
        <!-- use:clickOutside on:clickOutside={onClickOutside} -->
        <div
                use:clickOutside on:clickOutside={onClickOutside}
                class:hidden={!showMenu}
                class="hidden w-full flex-grow lg:flex lg:items-center lg:w-auto mt-2 lg:mt-0 bg-white lg:bg-transparent text-black p-4 lg:p-0 z-20"
                id="nav-content"
        >
            <ul class="list-reset lg:flex justify-end flex-1 items-center">

            </ul>
            <button
                    id="navAction"
                    class="mx-auto lg:mx-0 hover:underline bg-white text-gray-800 font-bold rounded-full mt-4 lg:mt-0 py-4 px-8 shadow opacity-75 focus:outline-none focus:shadow-outline transform transition hover:scale-105 duration-300 ease-in-out"
            >
                Chess
            </button>
            <Button secondary={navFloat} center={false}>Chat</Button>
        </div>
    </div>
    <hr class="border-b border-gray-100 opacity-25 my-0 py-0" />
</nav>
