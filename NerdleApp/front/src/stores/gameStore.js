import { writable } from "svelte/store";

export function createGrid() { 
    // Create a 6x8 grid of empty strings
    const grid = [];
    for (let i = 0; i < 6; i++) {
        grid.push([]);
        for (let j = 0; j < 8; j++) grid[i][j] = "";
    }
    return grid;
}

export const info = writable({ 
    // The game info number of tries and number of characters
    char: 0,
    essai: 0,
});

export const equation = writable(""); // The equation given by the user
export const solution = writable(""); // The solution given by the server encrypted to avoid cheating
export const couleurs = writable(createGrid()); // The colors grid same size as the play grid containing the classes to give to the cells
export const grille = writable(createGrid()); // The play grid containing the characters given by the user