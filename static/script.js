async function loadDashboard() {
    const response = await fetch("/dashboard");

    const data = await response.json();

    document.getElementById("income").innerText =
        data.total_income;

    document.getElementById("expense").innerText =
        data.total_expense;

    document.getElementById("balance").innerText =
        data.balance;

    document.getElementById("category").innerText =
        data.top_category;
}

loadDashboard();