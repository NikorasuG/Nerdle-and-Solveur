<script>
    import { grille } from "../stores/gameStore.js";
    import Cellule from "./Cellule.svelte";
</script>
<div class="jeux my-12 mx-auto w-fit">
    {#each $grille as column,y}
        <div class="row flex">
            {#each column as row,x}
                <Cellule {y} {x}/>
            {/each}
        </div>
    {/each}
</div>