<script>
    //objet clavier c'est l'objet le plus gros et complexe du projet les desc de fonction seront faite en anglais
    import { onMount } from "svelte";
	import Touche from "./Touche.svelte";
    import {grille,info,couleurs,equation,solution,createGrid} from "../stores/gameStore.js";
    import {checkequ} from "../requests/checkEqu.js";
    import {getSol} from "../requests/getSol.js";
    import {getHelp} from "../requests/getHelp.js";

    const ligne1 = ['1','2','3','4','5','6','7','8','9','0'];
    const ligne2 = ['Entrer','+', '-','*','/','=','Supprimer'];
    const ligne3 = ['Aide','Recommencer','Quitter'];
    //for more information about the stores check the file gameStore.js basicly all update are done by updating the store and displaying dynamicly with svelte elements
    const sleep = (ms) => {
        //sleep function used to wait for promise
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    const supr =  ()=>{
        //supr function used to delete the last char of the current line
        if($info.char === 0){ //avoid deleting if there is no char
            return;
        }
        info.update((previous)=>{ //update the state of the game
            console.log(previous);
            return {
                essai:previous.essai,
                char:previous.char-1
            }
        });
        grille.update((previous)=>{ //update the grid to delete the char
            const newGrille = previous;
            newGrille[$info.essai][$info.char] = "";
            return newGrille;
        });
    }
    const entrer = async ()=>{
        //entrer function used to check the current line and update the game state accordingly
        if($info.char < 4){ //avoid checking if the line is not complete
            return;
        }
        handleTry(); //check the line
        console.log($info.essai);
        if ($info.essai == 5){ //check if the game is over
            handleEndGame('fail');
        }
        else {
            info.update((previous)=>{ //update the state of the game
            return {
                essai:previous.essai+1,
                char:0
            }});
        }
    }
    const reset = async () =>{
        //reset function used to reset the game reset all stores and request a new solution
        let sol = await getSol();
        solution.set(sol.token);
        console.log($solution);
        info.set({essai:0,char:0});
        grille.set(createGrid());
        couleurs.set(createGrid());
        equation.set("");
    }
    const quitter = () =>{
        //quitter function used to quit the game and go back to the home page
        window.location.href = "/";
    }
    const aide = async () =>{
        //aide function used to get a hint from the server and display it to the user
        let data = await getHelp($grille,$solution,$couleurs,$info.essai);
        alert("essayer ça : "+data.hint);
    }
    const handleTry = async () => {
        //handleTry function used to check the current line and update the game state accordingly
        const newCouleurs = $couleurs;
        const previous = $info.essai;
        $equation = "";
        for (let i =0; i<8;i++ ){ //create the equation to send to the server by adding the char char by char
            let char = $grille[previous][i];
            equation.update((previous)=> previous + char);
        }
        let data = await checkequ($equation,$solution); //send the equation to the server and get the result
        if (data.message == "invalid equation"){ //check the result and update the game state accordingly
            console.log("invalid equation"); //if the equation is invalid we don't update the grid and the user don't loose a try
            info.update((previous)=>{
                console.log(previous);
                return {
                    essai:previous.essai -1,
                    char:8
                }});}
        else if (data.message == 'success') { //if the equation is correct we update the grid and the user win setting all the cell to correct
            for (let i = 0; i<8;i++ ){
            newCouleurs[previous][i] = 'correct';
            console.log(newCouleurs[previous][i]);
            }
            couleurs.set(newCouleurs);
            await sleep(1000);
            handleEndGame('success');
        }
        else{
            for (let i = 0; i<8;i++ ){ // if the equation is valid but not the solution we update the grid and the user loose a try
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