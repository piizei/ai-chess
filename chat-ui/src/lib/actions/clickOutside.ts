// source: https://svelte.dev/repl/0ace7a508bd843b798ae599940a91783?version=3.16.7

/** Dispatch event on click outside of node */
const clickOutside = (node: HTMLElement): unknown  => {
    const handleClick = (event: { target: Node | null; defaultPrevented: never }) => {
        if (node && !node.contains(event.target) && !event.defaultPrevented) {
            const detail = { event } // see: https://www.programmersought.com/article/93843748120/
            node.dispatchEvent(new CustomEvent('clickOutside', { detail }))
        }
    }
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-expect-error
    document.addEventListener('click', handleClick, true)

    return {
        destroy() {
            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-expect-error
            document.removeEventListener('click', handleClick, true)
        },
    }
}

const clickOutsideAction = (node: HTMLElement, onEventFunction: (e: CustomEvent) => void): unknown => {
    const handleClick = (event: any) => {
        if (!node.contains(event.target)) onEventFunction(event)
    }

    document.addEventListener('click', handleClick)

    return {
        destroy() {
            document.removeEventListener('click', handleClick)
        },
    }
}

export { clickOutside, clickOutsideAction }
