<script>
    import { onMount } from "svelte";
	import Touche from "./Touche.svelte";
    import {grille,info,couleurs,equation,solution,createGrid} from "../stores/gameStore.js";
    import {checkequ} from "../requests/checkEqu.js";
    import {getSol} from "../requests/getSol.js";

    const ligne1 = ['1','2','3','4','5','6','7','8','9','0'];
    const ligne2 = ['Entrer','+', '-','*','/','=','Supprimer'];
    const ligne3 = ['Aide','Recommencer','Quitter'];

    const sleep = (ms) => {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    const supr =  ()=>{
        if($info.char === 0){
            return;
        }
        info.update((previous)=>{
            console.log(previous);
            return {
                essai:previous.essai,
                char:previous.char-1
            }
        });
        grille.update((previous)=>{
            const newGrille = previous;
            newGrille[$info.essai][$info.char] = "";
            return newGrille;
        });
    }
    const entrer = async ()=>{
        if($info.char < 4){
            return;
        }
        handleTry();
        console.log($info.essai);
        if ($info.essai == 5){
            handleEndGame('fail');
        }
        else {
            info.update((previous)=>{
            return {
                essai:previous.essai+1,
                char:0
            }});
        }
    }
    const reset = async () =>{
        let sol = await getSol();
        solution.set(sol.token);
        console.log($solution);
        info.set({essai:0,char:0});
        grille.set(createGrid());
        couleurs.set(createGrid());
        equation.set("");
    }
    const quitter = () =>{
        window.location.href = "/";
    }
    const aide = () =>{
        alert("git gud (solveur not implemented)");
    }
    const handleTry = async () => {
        const newCouleurs = $couleurs;
        const previous = $info.essai;
        $equation = "";
        for (let i =0; i<8;i++ ){
            let char = $grille[previous][i];
            equation.update((previous)=> previous + char);
        }
        let data = await checkequ($equation,$solution);
        if (data.message == "invalid equation"){
            console.log("invalid equation");
            info.update((previous)=>{
                console.log(previous);
                return {
                    essai:previous.essai -1,
                    char:8
                }});}
        else if (data.message == 'success') {
            for (let i = 0; i<8;i++ ){
            newCouleurs[previous][i] = 'correct';
            console.log(newCouleurs[previous][i]);
            }
            couleurs.set(newCouleurs);
            await sleep(1000);
            handleEndGame('success');
        }
        else{
            for (let i = 0; i<8;i++ ){
            newCouleurs[previous][i] = data.message[i];
        }
        couleurs.set(newCouleurs);
    }}

    const handleEndGame = (result) =>{
        if (result == 'success'){
            alert("Bravo vous avez gagné");
        }
        else if (result == 'fail'){
            alert("Vous avez perdu");
        }
        reset();
    }
    const press = (key ="") => {
        if (key == "Supprimer") supr();
        else if (key == "Entrer") entrer();
        else if (key == "Recommencer") reset();
        else if (key == "Aide") aide();
        else if (key == "Quitter") quitter();
        else {
            let {essai, char} = $info;
            if(char>7)
                return;
            grille.update((previous)=>{
                const newGrille = previous;
                newGrille[essai][char++] = key;
                return newGrille;
            });
            info.set({essai,char});
        }}
    onMount( () => {
        reset();
    });
</script>

<div class="clavier fixed w-fit bottom-3 left-1/2 transform translate-y-0 -translate-x-1/2">
    <div class="row flex items-center justify-center">
        {#each ligne1 as char}
                <Touche {char} {press}/>
        {/each}
    </div>
    <div class="row flex items-center justify-center">
        {#each ligne2 as char}
                <Touche {char} {press}/>
        {/each}
    </div>
    <div class="row flex items-center justify-center">
        {#each ligne3 as char}
                <Touche {char} {press}/>
        {/each}
    </div>
</div>