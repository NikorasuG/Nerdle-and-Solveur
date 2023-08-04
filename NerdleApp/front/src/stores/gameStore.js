import { writable } from "svelte/store";

export function createGrid() {
    const grid = [];
    for (let i = 0; i < 6; i++) {
        grid.push([]);
        for (let j = 0; j < 8; j++) grid[i][j] = "";
    }
    return grid;
}

export const info = writable({
    char: 0,
    essai: 0,
});

export const equation = writable("");
export const solution = writable("");
export const couleurs = writable(createGrid());
export const grille = writable(createGrid());