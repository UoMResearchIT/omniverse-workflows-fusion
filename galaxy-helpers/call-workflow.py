import argparse
from datetime import datetime
import sys
from bioblend.galaxy import GalaxyInstance

# -----------------------------------------------------------------------------
# Parse arguments

parser = argparse.ArgumentParser(prog='Call workflow', description='')
parser.add_argument('--api-key', required=True)
parser.add_argument('--server', required=True)
parser.add_argument('--sensor', required=True)

args = parser.parse_args(sys.argv[1:])

# -----------------------------------------------------------------------------
# Get galaxy instance

gi = GalaxyInstance(url=args.server, key=args.api_key)

# -----------------------------------------------------------------------------
# Create history 

now = datetime.now()
now_str = now.strftime("%d/%m/%Y %H:%M:%S")

# -----------------------------------------------------------------------------
# Invoke workflow

workflow_id = gi.workflows.get_workflows()[0]["id"]
workflow = gi.workflows.show_workflow(workflow_id)

inputs_spec = workflow["inputs"]
inputs = {
    inputs_spec["0"]["uuid"]: args.sensor
}
gi.workflows.invoke_workflow(workflow_id,
                             inputs=inputs,
                             history_name=f'Data gathering triggered ({now_str})')
