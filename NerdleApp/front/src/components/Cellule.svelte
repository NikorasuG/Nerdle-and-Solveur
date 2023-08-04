<script>
    import { grille, couleurs } from "../stores/gameStore.js";
    export let x;
    export let y;
    $: lettre = $grille[y][x];
    $: couleur = $couleurs[y][x];
</script>

<div  class={`bg-slate-700 h-16 w-16 m-1 flex items-center justify-center text-white ${couleur}`}>
    {lettre}
</div>

<style>
    .correct{
        background-color: rgb(15 118 110);
    }
    .incorrect{
        background-color: rgb(153 27 27);
    }
    .misplaced{
        background-color: rgb(161 98 7);
    }
</style>