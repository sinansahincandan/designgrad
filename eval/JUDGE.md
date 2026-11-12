# Blind judging protocol (independent judge, outside the loop)

The judge sees only `runs/<run>/blind/<item>/`: the specification, the final CAD code with comments removed, a 4-view render
(if the code builds) and `facts.json` (builds?, number of solids, size, mass). The judge never sees which method produced an item,
how many rounds it took, the hidden tests, or `blind_key.json`.

For every item, score 1–5 (5 = best) and write one sentence of justification per score:

1. **Engineering soundness**: Would this part do its job (strength, stability, fit, load path), judged from the render and code?
2. **Manufacturability**: Could it be 3D-printed or machined as drawn (no floating pieces, sensible walls, printable overhangs)?
3. **Specification fidelity**: How closely does it follow the stated features, positions and dimensions?
4. **Design quality / novelty**: Is the concept thoughtful (ribs, gussets, material where the load is) rather than a minimal block?
5. **Overall**: Holistic judgment.

Items that do not build get 1 on every score. Output one JSON line per item:
`{"item": "D1234", "soundness": s, "manufacturability": m, "fidelity": f, "novelty": n, "overall": o, "why": "..."}`

Pairwise preferences between methods are derived from the overall scores within each problem (ties when equal).
The first author separately ranks a subset of problems blind; agreement with the judge is reported.
