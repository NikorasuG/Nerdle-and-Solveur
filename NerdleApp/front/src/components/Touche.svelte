<script>
    //objet des touches du clavier
    export let press;
    export let char;
</script>

<div class="touche bg-slate-700 text-white p-5 m-1 cursor-pointer rounded hover:bg-teal-500" on:click={()=> press(char)}>
    {char}
</div>