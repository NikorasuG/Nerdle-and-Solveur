export function getHelp(equ,sol,colors,essai) {
    /*this function is used to request a hint for the current game given the current state of tries an colors*/
    const [returnEqs,returnColors] = formatHelp(equ,colors,essai)

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
    // This function is used to format the data to send to the server in order to get the help
    // The server needs the data to be in a specific format a liste of string for the equations and a list of string for the colors
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