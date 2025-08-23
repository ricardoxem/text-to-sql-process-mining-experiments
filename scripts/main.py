from execute_analysis import execute as execute_analysis_execute
from execute_analysis_by_model import execute as execute_by_model_execute
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql_complexity", type=str)
    parser.add_argument("--metric", type=str)
    parser.add_argument("--lang", type=str)
    parser.add_argument("--file", type=str)
    parser.add_argument("--execution", type=str)

    args = parser.parse_args()

    if args.metric == "EX":
        metric_label = 'Execution Acc. (%)'
    else:
        metric_label = 'Exact Match Acc. (%)'

    if args.execution == 'byModel':
        execute_by_model_execute(args.sql_complexity, args.file)
    else:
        execute_analysis_execute(args.lang, args.metric, args.sql_complexity, args.file, metric_label)