export function checkequ(equ,sol) {
    // This function is used to check with the back if the equation is correct
    const response = fetch("http://localhost:5000/checkequ", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            equation: equ,
            token: sol
        })
    })
    .then(response => response.json());
    return response;
}
