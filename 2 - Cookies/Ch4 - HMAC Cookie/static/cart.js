document.addEventListener("DOMContentLoaded", function() {
    let total = 0;
    document.querySelectorAll(".add-item").forEach(button => {
        button.addEventListener("click", function() {
            let price = parseInt(this.dataset.price);
            total += price;
            document.getElementById("total").textContent = total;
        });
    });

    document.getElementById("checkout").addEventListener("click", function() {
        fetch("/checkout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ total: total })
        })
            .then(response => response.json())
            .then(data => alert(data.message));
    });
});
