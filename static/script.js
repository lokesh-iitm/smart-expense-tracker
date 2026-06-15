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

                                <td>
                <button
                    onclick="editExpense(${expense.id})"
                >
                    Edit
                </button>

                <button
                    onclick="deleteExpense(${expense.id})"
                >
                    Delete
                </button>
            </td>
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
    async function addIncome(event) {

    event.preventDefault();

    const income = {
        source:
            document.getElementById(
                "income-source"
            ).value,

        amount:
            parseFloat(
                document.getElementById(
                    "income-amount"
                ).value
            )
    };

    await fetch("/income", {
        method: "POST",
        headers: {
            "Content-Type":
                "application/json"
        },
        body: JSON.stringify(income)
    });

    loadDashboard();
    loadIncome();

    document
        .getElementById("income-form")
        .reset();
}

document
    .getElementById("income-form")
    .addEventListener(
        "submit",
        addIncome
    );
 loadExpenses();
 async function loadIncome() {

    const response =
        await fetch("/income");

    const incomes =
        await response.json();

    const tableBody =
        document.getElementById(
            "income-body"
        );

    tableBody.innerHTML = "";

    incomes.forEach(income => {

        tableBody.innerHTML += `
            <tr>
                <td>${income.source}</td>
                <td>${income.amount}</td>
            </tr>
        `;

    });

}
loadIncome();

async function loadCategoryChart() {

    const response =
        await fetch("/analytics/top-categories");

    const data =
        await response.json();

    const labels =
        data.map(item => item.category);

    const amounts =
        data.map(item => item.total_spent);

    const ctx =
        document.getElementById(
            "categoryChart"
        );

    new Chart(ctx, {
        type: "bar",

        data: {
            labels: labels,

            datasets: [{
                label: "Total Spent",

                data: amounts
            }]
        }
    });
}
loadDashboard();
loadExpenses();
loadIncome();
loadCategoryChart();

document
    .getElementById("expense-form")
    .addEventListener(
        "submit",
        addExpense
    );
async function deleteExpense(id) {

    await fetch(`/expenses/${id}`, {
        method: "DELETE"
    });

    loadDashboard();
    loadExpenses();
    loadCategoryChart();
}
async function editExpense(id) {

    const title =
        prompt("Enter new title");

    const category =
        prompt("Enter new category");

    const amount =
        parseFloat(
            prompt("Enter new amount")
        );

    const date =
        prompt("Enter new date (YYYY-MM-DD)");

    await fetch(`/expenses/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type":
                "application/json"
        },

        body: JSON.stringify({
            title,
            category,
            amount,
            date
        })
    });

    loadDashboard();
    loadExpenses();
    loadCategoryChart();
}