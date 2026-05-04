import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "monthly.csv"


def load_csv(path: Path) -> dict[str, tuple[int, int]]:
    data: dict[str, tuple[int, int]] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            data[row["date"]] = (int(row["torveny"]), int(row["rendelet"]))
    return data


def main():
    cif = load_csv(BASE / "cif.csv")
    expired = load_csv(BASE / "expired.csv")

    all_dates = sorted(set(cif) | set(expired))

    monthly_new_t: dict[str, int] = defaultdict(int)
    monthly_new_r: dict[str, int] = defaultdict(int)
    monthly_exp_t: dict[str, int] = defaultdict(int)
    monthly_exp_r: dict[str, int] = defaultdict(int)

    for ds in all_dates:
        month = ds[:7]
        new_t, new_r = cif.get(ds, (0, 0))
        exp_t, exp_r = expired.get(ds, (0, 0))
        monthly_new_t[month] += new_t
        monthly_new_r[month] += new_r
        monthly_exp_t[month] += exp_t
        monthly_exp_r[month] += exp_r

    months = sorted(set(monthly_new_t) | set(monthly_exp_t))

    with open(OUTPUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "new_torveny", "new_rendelet", "expired_torveny", "expired_rendelet"])
        for m in months:
            writer.writerow([m, monthly_new_t[m], monthly_new_r[m], monthly_exp_t[m], monthly_exp_r[m]])

    print(f"Wrote {len(months)} months to {OUTPUT}")


if __name__ == "__main__":
    main()
