document.getElementById("uploadForm").onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append("dataset", document.getElementById("dataset").files[0]);
    formData.append("features", document.getElementById("features").files[0]);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("results").innerHTML = JSON.stringify(result);
};
