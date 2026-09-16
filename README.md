# TaskPulse API

TaskPulse is a small FastAPI task-tracking service created to test real CI/CD outcomes against the hosted DeployPilot API.

## Demo order

### Phase 1 - Build successful repository history

The repository starts with the incompatible dependency commented out:

```text
fastapi==0.116.1
# starlette==0.20.4
uvicorn==0.35.0
pytest==8.4.1
httpx==0.28.1
```

Push the clean project first. Then create 4-5 small legitimate successful commits so DeployPilot builds a PASS-heavy repository history.

Examples of harmless successful changes:

1. Change the FastAPI description text in `app/main.py`.
2. Add a short comment in `app/service.py`.
3. Change the version from `1.0.0` to `1.0.1`.
4. Add one more passing test.
5. Update this README.

Each push should keep dependency installation, configuration validation and tests green.

### Phase 2 - Create a REAL dependency failure

Edit `requirements.txt` and uncomment:

```text
starlette==0.20.4
```

Commit and push. Pip should genuinely fail because this old Starlette version conflicts with FastAPI 0.116.1. The workflow captures pip's real error log and sends it to DeployPilot.

Expected real CI result:

```text
Actual CI Result: FAIL
Real Failed Stage: dependency
Failure Type: Dependency Error
GitHub Actions: RED
```

### Phase 3 - Fix the dependency

Comment the line again or remove it:

```text
# starlette==0.20.4
```

Then commit and push. Pip installs compatible dependencies automatically and tests pass.

Expected real CI result:

```text
Actual CI Result: PASS
Real Failed Stage: none
Failure Type: N/A - no CI failure
GitHub Actions: GREEN
```

## GitHub secret

Create this repository secret before running the workflow:

```text
DEPLOYPILOT_API_KEY
```

The workflow calls:

```text
https://deploypilot-ai-api-korea-2026.azurewebsites.net/github/predict
```

## Local test

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

## Exact five-clean-run sequence

The initial repository push is successful run 1.

For runs 2-5, make one tiny documentation change per commit so each GitHub Actions execution is a real new run while application code remains healthy.

```powershell
Add-Content demo-history.md "- Clean validation run 2."
git add demo-history.md
git commit -m "Record clean validation run 2"
git push

Add-Content demo-history.md "- Clean validation run 3."
git add demo-history.md
git commit -m "Record clean validation run 3"
git push

Add-Content demo-history.md "- Clean validation run 4."
git add demo-history.md
git commit -m "Record clean validation run 4"
git push

Add-Content demo-history.md "- Clean validation run 5."
git add demo-history.md
git commit -m "Record clean validation run 5"
git push
```

After all five clean runs, uncomment `starlette==0.20.4`, commit and push to create the real dependency-resolution failure. After capturing the failure, comment it again and push the fix.
