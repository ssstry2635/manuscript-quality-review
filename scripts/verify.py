"""Compare scoped manuscript claims and verify review evidence."""
import argparse
from decimal import Decimal, InvalidOperation
from evidence import anchor, dump, index, inventory, load, normalize, require

SCOPE = ("population", "outcome", "timepoint", "analysis", "unit")
TYPES = {"fact_error", "insufficient_evidence", "reporting", "standards", "suggestion"}
SEVERITIES = {"major", "moderate", "minor"}

def bounds(value, places):
    require(type(value) in (int, float, str), "Expected a numeric value")
    value = Decimal(str(value))
    require(value.is_finite(), "Value must be finite")
    require(type(places) is int and 0 <= places <= 12, "Invalid reported precision")
    half = Decimal(1).scaleb(-places) / 2
    return value - half, value + half

def audit(model, root):
    sources, metadata = inventory(root, model["sources"])
    claims = index(model["claims"], "claim")
    anchors = {cid: anchor(item["anchor"], sources) for cid, item in claims.items()}
    comparisons = []
    for rid, item in index(model.get("comparisons", []), "comparison").items():
        left, right = item["left"], item["right"]
        require(left != right, "Comparison needs separate claims")
        a, b = claims[left], claims[right]
        unresolved = [k for k in SCOPE if any(not isinstance(c.get("scope", {}).get(k), str)
                     or not c["scope"][k].strip() for c in (a, b))]
        different = [k for k in SCOPE if k not in unresolved and
                     normalize(a["scope"][k]) != normalize(b["scope"][k])]
        result = {"id": rid, "claim_ids": [left, right], "anchors": [anchors[left], anchors[right]],
                  "unknown_scope_fields": unresolved, "different_scope_fields": different}
        if unresolved or different:
            result["status"] = "scope_review_required"
        else:
            lo_a, hi_a = bounds(a["value"], a["places"])
            lo_b, hi_b = bounds(b["value"], b["places"])
            result["status"] = "rounding_compatible" if max(lo_a, lo_b) <= min(hi_a, hi_b) else "numeric_discrepancy"
            result["rounding_intervals"] = [[str(lo_a), str(hi_a)], [str(lo_b), str(hi_b)]]
        comparisons.append(result)
    citations = []
    for cid, item in index(model.get("citations", []), "citation").items():
        claim = item["claim_id"]
        require(claim in claims, f"Unknown cited claim: {claim}")
        if item.get("reference") is None:
            require(str(item.get("reason", "")).strip(), f"Explain unavailable citation {cid}")
            citations.append({"id": cid, "claim": anchors[claim], "status": "pending", "reason": item["reason"]})
            continue
        reference = anchor(item["reference"], sources)
        require(item["verdict"] in {"supports", "partial", "contradicts", "unrelated", "uncertain"},
                f"Invalid citation verdict: {cid}")
        require(str(item.get("rationale", "")).strip(), f"Missing rationale: {cid}")
        citations.append({"id": cid, "claim": anchors[claim], "reference": reference,
                          "status": "human_or_agent_judgment", "verdict": item["verdict"],
                          "rationale": item["rationale"]})
    findings = []
    for fid, item in index(model.get("findings", []), "finding").items():
        require(item["type"] in TYPES and item["severity"] in SEVERITIES, f"Invalid finding classification: {fid}")
        require(item["status"] in {"confirmed", "pending"}, f"Invalid finding status: {fid}")
        for field in ("rationale", "impact", "revision"):
            require(isinstance(item.get(field), str) and item[field].strip(), f"Missing {field}: {fid}")
        refs = [anchor(ref, sources) for ref in item.get("anchors", [])]
        require(refs or (item["status"] == "pending" and item.get("missing_material")),
                f"Finding {fid} needs evidence or a named pending material")
        findings.append({**item, "anchors": refs})
    return {"case_id": model["case_id"], "sources": metadata, "comparisons": comparisons,
            "citations": citations, "findings": findings,
            "scope": "Numerical comparison and anchoring only. Scientific and citation interpretations are supplied judgments."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        dump(args.out, audit(load(args.input), args.root))
    except (ValueError, KeyError, TypeError, OSError, InvalidOperation) as exc:
        dump(args.out, {"status": "input_or_execution_error", "detail": str(exc)})
        parser.exit(2, f"{exc}\n")

if __name__ == "__main__":
    main()
