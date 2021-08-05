name: FastAPI CI/CD

on:
  # Trigger the workflow on push
  push:
    # Push events on main branch
    branches: [ main ]

# The Job defines a series of steps that execute on the same runner.
jobs:
  CI:
    # Define the runner used in the workflow
    runs-on: ubuntu-latest
    steps:   
      # Check out repo so our workflow can access it
      - name: Check out repo
      - uses: actions/checkout@v2

      # Step-1 Setup Python
      - name: Set up Python
        # This action sets up a Python environment for use in actions
        uses: actions/setup-python@v2
        with:
          python-version: 3.7
          # optional: architecture: x64 x64 or x86. Defaults to x64 if not specified

      # Step-2 Install Python Virtual ENV
      - name: Install Python Virtual ENV
        run: pip3 install virtualenv

      # Step-3 Setup Virtual ENV
      # https://docs.github.com/en/actions/guides/caching-dependencies-to-speed-up-workflows
      - name:  Virtual ENV
        uses: actions/cache@v2
        id: cache-venv # name for referring later
        with:
          path: venv # what we cache: the Virtual ENV
          # The cache key depends on requirements.txt
          key: ${{ runner.os }}-venv-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-venv-
          # Build a Virtual ENV, but only if it doesn't already exist
      - name: Install Dependencies
        run: python -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt

      - name: Run Tests   
        # Note that you have to activate the virtualenv in every step
        # because GitHub actions doesn't preserve the environment   
        run: . venv/bin/activate && pytest
      - name: Create archive of dependencies
        run: |
          cd ./venv/lib/python3.7/site-packages
          zip -r9 ../../../../api.zip .
      - name: Add API files to Zip file
        run: cd ./api && zip -g ../api.zip -r .
      - name: Upload zip file artifact
        # uploads artifacts from your workflow allowing you to share data between jobs 
        # Stores data once a workflow is complete
        uses: actions/upload-artifact@v2
        with:
          name: api
          path: api.zip