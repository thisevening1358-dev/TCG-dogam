# Builds the single-file app: injects the Korean/English Pokémon species name tables into app.html.
import json, pathlib
here = pathlib.Path(__file__).parent
def names(f):
    rows = json.loads((here / f).read_text(encoding="utf-8"))["data"]["pokemonspeciesname"]
    rows.sort(key=lambda r: r["pokemon_species_id"])
    return [r["name"] for r in rows]
ko, en = names("ko_names.json"), names("en_names.json")
assert len(ko) == len(en)
src = (here / "app.html").read_text(encoding="utf-8")
js = "const KO_NAMES=" + json.dumps(ko, ensure_ascii=False) + ";\nconst EN_NAMES=" + json.dumps(en, ensure_ascii=False) + ";"
out = src.replace("/*__NAMES__*/", js)
(here.parent / "index.html").write_text(out, encoding="utf-8")
print("built", len(out), "bytes")
