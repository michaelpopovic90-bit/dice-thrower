import os

collect_ignore = []
if not os.environ.get("E2E_BASE_URL") and not os.environ.get("RUN_E2E"):
    collect_ignore.append("e2e")
