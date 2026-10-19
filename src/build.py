# Builds the single-file app: injects the Korean/English/Japanese Pokémon species name tables and the
# set extras (logos found elsewhere, Japanese set names and dates) into app.html.
import json, pathlib
here = pathlib.Path(__file__).parent
def names(f):
    rows = json.loads((here / f).read_text(encoding="utf-8"))["data"]["pokemonspeciesname"]
    rows.sort(key=lambda r: r["pokemon_species_id"])
    return [r["name"] for r in rows]
ko, en, ja = names("ko_names.json"), names("en_names.json"), names("ja_names.json")
assert len(ko) == len(en) == len(ja)
extra = json.loads((here / "sets_extra.json").read_text(encoding="utf-8"))
src = (here / "app.html").read_text(encoding="utf-8")
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
js = f"const KO_NAMES={dump(ko)};\nconst EN_NAMES={dump(en)};\nconst JA_NAMES={dump(ja)};\nconst SET_EXTRA={dump(extra)};"
out = src.replace("/*__NAMES__*/", js)
(here.parent / "index.html").write_text(out, encoding="utf-8")
print("built", len(out), "bytes")
