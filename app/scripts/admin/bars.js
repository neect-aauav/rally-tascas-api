const urlParams = new URLSearchParams(window.location.search);
let id = parseInt(urlParams.get('id'));
if (id && id >= 0) {
    fetch("/api/bars?id="+id)
        .then(response => response.json())
        .then(result => {
            const bar = result["data"][0];
            document.querySelector(".form p").innerText = bar["name"];
            document.querySelector(".form div").id = "bar-content";

            fetch("/api/teams?")
                .then(response => response.json())
                .then(result => {
                    listSelection(document.querySelector("#bar-content"), result["data"].map(team => ({
                        "text": team["name"],
                        "url": "#"
                    })));
            });

        });
}
else {
    const barsList = document.querySelector("#bars-list");

    fetch("/api/bars")
        .then(response => response.json())
        .then(result => {
            listSelection(barsList, result["data"].map(bar => ({
                "text": bar["name"],
                "url": "bars?id="+bar["id"]
            })));
        });
}

const listSelection = (list, rows) => {
    if (list) {
        list.classList.add("list");
        rows.forEach(row => {
            const barElem = document.createElement("a");
            list.appendChild(barElem);
            barElem.appendChild(document.createTextNode(row["text"]));
            barElem.classList.add("clickable");
            barElem.href = row["url"];
        });
    }
}