const API_URL = "http://127.0.0.1:8000";

const loginSection = document.querySelector("#login-section");
const contactsSection = document.querySelector("#contacts-section");
const loginForm = document.querySelector("#login-form");
const contactForm = document.querySelector("#contact-form");
const contactsList = document.querySelector("#contacts-list");
const contactsCount = document.querySelector("#contacts-count");
const message = document.querySelector("#message");
const loading = document.querySelector("#loading");

let accessToken = "";
let refreshToken = "";
let editingId = null;
let contacts = [];

function showMessage(text) {
    message.textContent = text;
    message.classList.remove("hidden");
}

function clearMessage() {
    message.textContent = "";
    message.classList.add("hidden");
}

function showContactsPage() {
    loginSection.classList.add("hidden");
    contactsSection.classList.remove("hidden");
}

function showLoginPage() {
    loginSection.classList.remove("hidden");
    contactsSection.classList.add("hidden");
    accessToken = "";
    refreshToken = "";
}

async function sendRequest(path, options = {}, retry = true) {
    const headers = { ...options.headers };
    if (accessToken) {
        headers.Authorization = `Bearer ${accessToken}`;
    }

    let response = await fetch(`${API_URL}${path}`, { ...options, headers });

    if (response.status === 401 && refreshToken && retry) {
        const refreshResponse = await fetch(`${API_URL}/api/token/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        if (refreshResponse.ok) {
            const tokens = await refreshResponse.json();
            accessToken = tokens.access;
            return sendRequest(path, options, false);
        }

        showLoginPage();
        throw new Error("Tu sesión terminó. Inicia sesión nuevamente.");
    }

    const data = response.status === 204 ? null : await response.json();
    if (!response.ok) {
        const details = data && Object.values(data).flat().join(" ");
        throw new Error(details || "No se pudo completar la solicitud.");
    }
    return data;
}

function renderContacts() {
    contactsList.replaceChildren();
    contactsCount.textContent = `${contacts.length} contacto${contacts.length === 1 ? "" : "s"}`;

    if (contacts.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty";
        empty.textContent = "Todavía no hay contactos.";
        contactsList.append(empty);
        return;
    }

    for (const contact of contacts) {
        const card = document.createElement("article");
        card.className = "contact-card";

        const name = document.createElement("h3");
        name.textContent = contact.name;
        card.append(name);

        for (const [label, value] of [
            ["Teléfono", contact.phone],
            ["Correo", contact.email],
            ["Dirección", contact.address],
        ]) {
            const detail = document.createElement("p");
            detail.textContent = `${label}: ${value}`;
            card.append(detail);
        }

        const actions = document.createElement("div");
        actions.className = "contact-actions";

        const editButton = document.createElement("button");
        editButton.className = "button button-light";
        editButton.textContent = "Editar";
        editButton.addEventListener("click", () => editContact(contact));

        const deleteButton = document.createElement("button");
        deleteButton.className = "button button-danger";
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener("click", () => deleteContact(contact));

        actions.append(editButton, deleteButton);
        card.append(actions);
        contactsList.append(card);
    }
}

async function loadContacts() {
    clearMessage();
    loading.classList.remove("hidden");
    contactsList.replaceChildren();
    try {
        contacts = await sendRequest("/api/contacts/");
        renderContacts();
    } catch (error) {
        showMessage(error.message);
    } finally {
        loading.classList.add("hidden");
    }
}

function editContact(contact) {
    editingId = contact.id;
    for (const field of ["name", "phone", "email", "address"]) {
        contactForm.elements[field].value = contact[field];
    }
    document.querySelector("#form-title").textContent = "Editar contacto";
    document.querySelector("#save-button").textContent = "Guardar cambios";
    contactForm.scrollIntoView({ behavior: "smooth", block: "start" });
}

function resetContactForm() {
    editingId = null;
    contactForm.reset();
    document.querySelector("#form-title").textContent = "Agregar contacto";
    document.querySelector("#save-button").textContent = "Guardar contacto";
}

async function deleteContact(contact) {
    if (!window.confirm(`¿Eliminar a ${contact.name}?`)) {
        return;
    }
    clearMessage();
    try {
        await sendRequest(`/api/contacts/${contact.id}/`, { method: "DELETE" });
        await loadContacts();
    } catch (error) {
        showMessage(error.message);
    }
}

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();
    const values = new FormData(loginForm);
    try {
        const response = await fetch(`${API_URL}/api/token/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username: values.get("username"),
                password: values.get("password"),
            }),
        });
        const tokens = await response.json();
        if (!response.ok) {
            throw new Error("Usuario o contraseña incorrectos.");
        }
        accessToken = tokens.access;
        refreshToken = tokens.refresh;
        showContactsPage();
        await loadContacts();
    } catch (error) {
        showMessage(error.message);
    }
});

contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearMessage();
    const contact = Object.fromEntries(new FormData(contactForm));
    const path = editingId ? `/api/contacts/${editingId}/` : "/api/contacts/";
    const method = editingId ? "PATCH" : "POST";

    try {
        await sendRequest(path, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(contact),
        });
        resetContactForm();
        await loadContacts();
    } catch (error) {
        showMessage(error.message);
    }
});
