export function getSol(sol) {
    const response = fetch("http://localhost:5000/getequ?length=8", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    })
    .then(response => response.json());
    return response;
}