<script>
    //objet cellule trois classe sont predéfinie pour les cellules correct incorrect et misplaced
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
        background-color: #0f766e;
    }
    .incorrect{
        background-color: #991b1b;
    }
    .misplaced{
        background-color: #a16207;
    }
</style>