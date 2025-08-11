/bu# Vexel: A Google Cloud Sales Assistant

Vexel is a powerful, AI-driven application designed to assist Google Cloud sales teams. It provides tools for managing customer interactions, analyzing sales data, and streamlining the sales workflow.

This repository contains the backend services and the frontend application for Vexel.

## Repository Structure

The project is organized as a monorepo with two main parts:

-   **`/` (Backend):** The core backend is a Python application built using Poetry. It contains various agents (`calendar_agent`, `charts_agent`, etc.) that handle specific business logic and integrations with Google Cloud services.
-   **`vexel-app/` (Frontend):** The frontend is a Next.js application built with pnpm. It provides the user interface for interacting with the Vexel agents and services.

## Getting Started

Follow these instructions to set up your local development environment.

### Prerequisites

Before you begin, ensure you have the following installed:

-   **Python:** `v3.12` or higher
-   **Poetry:** For managing Python dependencies.
-   **Node.js:** `v20` or higher
-   **pnpm:** For managing JavaScript dependencies.

### Backend Setup

1.  **Install Python Dependencies:**
    From the root directory of the project, run:
    ```bash
    poetry install
    ```

2.  **Activate the Virtual Environment:**
    ```bash
    poetry shell
    ```

### Frontend Setup

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd vexel-app
    ```

2.  **Install JavaScript Dependencies:**
    ```bash
    pnpm install
    ```

3.  **Run the Development Server:**
    ```bash
    pnpm dev
    ```
    The application will be available at [http://localhost:3000](http://localhost:3000).

## Configuration

The project uses `.env` files for managing environment variables.

### Backend Configuration (`.env`)

The Python backend requires credentials for authenticating with Google Cloud services. Create a `.env` file in the root directory of the project with the following content:

```env
# .env

# Google Cloud Project ID
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

# Path to your Google Cloud service account key file
# Ensure this file is not committed to version control.
GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

### Frontend Configuration (`.env.local`)

The Next.js frontend requires OAuth client credentials for user authentication. Create a `.env.local` file in the `vexel-app/` directory. You can use the following template:

```env
# vexel-app/.env.local

# Google OAuth 2.0 Client Credentials
OAUTH_CLIENT_ID="your-google-oauth-client-id.apps.googleusercontent.com"
OAUTH_CLIENT_SECRET="your-google-oauth-client-secret"

# The redirect URI must match the one configured in your Google Cloud Console.
REDIRECT_URI="http://localhost:3000/api/auth/callback"

# A secret string for signing session cookies.
SESSION_SECRET="generate-a-strong-random-secret"
```
