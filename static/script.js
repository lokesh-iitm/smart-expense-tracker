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
async function loadExpenses() {
    const response = await fetch("/expenses?limit=100");

    const expenses = await response.json();

    const tableBody =
        document.getElementById("expense-body");

    tableBody.innerHTML = "";

    expenses.forEach(expense => {

        tableBody.innerHTML += `
            <tr>
                <td>${expense.title}</td>
                <td>${expense.category}</td>
                <td>${expense.amount}</td>
                <td>${expense.date}</td>
            </tr>
        `;

    });
}

loadExpenses();
async function addExpense(event) {

    event.preventDefault();

    const expense = {
        title:
            document.getElementById("title").value,

        category:
            document.getElementById(
                "expense-category"
            ).value,

        amount:
            parseFloat(
                document.getElementById("amount").value
            ),

        date:
            document.getElementById("date").value
    };

    await fetch("/expenses", {
        method: "POST",
        headers: {
            "Content-Type":
                "application/json"
        },
        body: JSON.stringify(expense)
    });

    loadDashboard();
    loadExpenses();

    document.getElementById(
        "expense-form"
    ).reset();
}


document
    .getElementById("expense-form")
    .addEventListener(
        "submit",
        addExpense
    );