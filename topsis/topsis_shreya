"""TOPSIS: Multi-criteria decision-making implementation."""

import sys
import pandas as pd
import numpy as np


def error_and_exit(message: str) -> None:
    print(f"Error: {message}")
    sys.exit(1)


def parse_and_validate(weights_arg: str, impacts_arg: str, ncols: int):
    try:
        weights = np.array([float(w.strip()) for w in weights_arg.split(",") if w.strip()])
    except ValueError:
        error_and_exit("Weights must be numeric and separated by commas")
    
    impacts = [imp.strip() for imp in impacts_arg.split(",") if imp.strip()]
    if not all(imp in ("+", "-") for imp in impacts):
        error_and_exit("Impacts must be '+' or '-' and separated by commas")
    
    if len(weights) != ncols or len(impacts) != ncols:
        error_and_exit(f"Weights and impacts count must equal criteria count ({ncols})")
    
    return weights, np.array(impacts)


def read_and_validate_csv(path: str):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        error_and_exit("File not found")
    except Exception as e:
        error_and_exit(f"Unable to read file: {e}")
    
    if df.shape[1] < 3:
        error_and_exit("Input file must have at least 3 columns")
    
    if not df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").notna().all().all():
        error_and_exit("Columns 2 onwards must contain only numeric values")
    
    return df


def topsis_calculation(data: np.ndarray, weights: np.ndarray, impacts: np.ndarray):
    norms = np.linalg.norm(data, axis=0)
    if np.any(norms == 0):
        error_and_exit("Column with all zeros detected")
    
    weighted = (data / norms) * weights
    ideal_best = np.where(impacts == "+", weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(impacts == "+", weighted.min(axis=0), weighted.max(axis=0))
    
    s_best = np.linalg.norm(weighted - ideal_best, axis=1)
    s_worst = np.linalg.norm(weighted - ideal_worst, axis=1)
    
    scores = np.divide(s_worst, s_best + s_worst, out=np.zeros_like(s_worst), where=(s_best + s_worst) != 0)
    ranks = np.argsort(-scores).argsort() + 1
    
    return scores, ranks


def run_topsis(input_path: str, weights_arg: str, impacts_arg: str, output_path: str) -> None:
    df = read_and_validate_csv(input_path)
    ncols = df.shape[1] - 1
    
    weights, impacts = parse_and_validate(weights_arg, impacts_arg, ncols)
    data = df.iloc[:, 1:].to_numpy(dtype=float)
    scores, ranks = topsis_calculation(data, weights, impacts)
    
    df["Topsis Score"] = scores
    df["Rank"] = ranks
    df.to_csv(output_path, index=False)


def main(argv=None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 4:
        error_and_exit("Usage: <InputDataFile> <Weights> <Impacts> <OutputResultFile>")
    run_topsis(*args)
    print(f"Result written to {args[3]}")


def cli() -> None:
    main()
