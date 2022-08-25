const toggleTable = (ids) => {
    const table = document.getElementById(ids)
    if(table.style.display === "none") {
        table.style.display = "table"
        table.style.display = "600px"
    } else {
        table.style.display = "none"
    }
}

