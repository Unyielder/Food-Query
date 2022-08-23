const toggleTable = (ids) => {
    const table = document.getElementById(ids)
    if(table.style.display === "none") {
        table.style.display = "block"
    } else {
        table.style.display = "none"
    }
}

