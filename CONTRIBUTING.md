# Contributing to ForgeCMS

Thanks for your interest in contributing to ForgeCMS.

## Local setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd forgecms
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows PowerShell:
   # .\\venv\\Scripts\\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   Then update `.env` values for your local MariaDB instance.
5. Run database migrations:
   ```bash
   flask db upgrade
   ```
6. Start the app:
   ```bash
   flask run
   ```

## Branching workflow

- Create a branch from `main` for each change.
- Use a descriptive branch name, for example:
  - `feature/add-post-preview`
  - `fix/login-validation`
  - `docs/update-contributing`

Example:

```bash
git checkout main
git pull
git checkout -b feature/your-change
```

## Pull request process

1. Keep each PR focused on a single change.
2. Ensure the app runs locally and migrations are included when schema changes are made.
3. Write clear commit messages.
4. Open a pull request with:
   - a concise title
   - a summary of what changed
   - testing notes
   - screenshots for UI changes when helpful
5. Respond to review feedback and update your branch.

## Code style expectations

- Follow existing project patterns and keep changes minimal.
- Use clear, descriptive names for variables, functions, and templates.
- Prefer small, focused functions and readable logic.
- Avoid unrelated refactors in the same PR.
- Update documentation when behavior or developer workflow changes.
