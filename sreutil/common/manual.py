# sreutil/common/manual.py
def sreutil_top_level_man_func(args):
    print("SREUTIL - Site Reliability Engineering Toolkit")
    print("----------------------------------------------")
    print("This toolkit provides a collection of utilities to assist with SRE tasks.")
    print("\nAvailable Tools:")
    print("  pyaws         - A suite of commands for interacting with AWS services.")
    # Add other tools here as they are developed, e.g.:
    # print("  k8shelper     - Utilities for Kubernetes cluster management.")
    # print("  gcpbuddy      - Commands for Google Cloud Platform resources.")
    print("\nUsage:")
    print("  sreutil <tool> <command> [options]")
    print("  sreutil man                  # Shows this top-level manual.")
    print("  sreutil <tool> man           # Shows the manual for a specific tool.")
    print("  sreutil <tool> <command> -h  # Shows help for a specific command.")