export function getHelp(equ,sol,colors,essai) {
    console.log("getHelp");
    console.log(equ);
    console.log(colors);
    const [returnEqs,returnColors] = formatHelp(equ,colors,essai)
    console.log(returnEqs)
    console.log(returnColors)
    const response = fetch("http://localhost:5000/gethelp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            equation: returnEqs,
            colors: returnColors,
            token: sol
        })
    })
    .then(response => response.json());
    return response;
}

function formatHelp(eqs,colors,essai) {
    let trueEqus = []
    let trueColors = []
    for (let index = 0; index < essai; index++) {
        let eq = ""
        eqs[index].forEach(element => {
            eq += element
        });
        trueEqus.push(eq)
        let col = ""
        colors[index].forEach(element => {
            if(element=="correct"){
                col +="2"
            }
            else if(element=="misplaced"){
                col +="1"
            }
            else{
                col +="0"
            }
        });
        trueColors.push(col)
    }
    return [trueEqus,trueColors]
}