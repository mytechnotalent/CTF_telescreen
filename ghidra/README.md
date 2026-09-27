# ghidra/ - the reverse-engineering workspace

Everything you need to open `../firmware/ctfnode.stripped` in Ghidra and give every
function its name back.

## Contents

| item | what it is |
| ---- | ---------- |
| `make_project.sh` | headless: import + full auto-analysis + save |
| `decompile.sh` | export one `.c` file per function |
| `ExportDecomp.java` | the Ghidra script `decompile.sh` runs |
| `proj/CTFNodeRE.gpr` | the analysed Ghidra project (open this in the GUI) |
| `decomp/` | raw decompilation, `FUN_00400960`-style names |
| `resolved/` | the same files renamed to their real functions |
| `ground_truth/` | `nm`, `readelf`, `objdump` evidence (instructor) |
| `RESOLUTION_MAP.md` | every function -> its real name + the rule that proves it |
| `resolution.json` | the same data, machine-readable |
| `resolve_functions.py` | generates `RESOLUTION_MAP.md`, `resolution.json`, `resolved/` |
| `gen_appendix_j.py` | generates `../CTF-XX-J-ghidra-function-resolution.md` |

## Quick start

```bash
../firmware/build_target.sh     # build the target first
./make_project.sh               # analyse it (headless) -> proj/CTFNodeRE.gpr
./decompile.sh                  # export every function to C (optional)

# open the GUI and load proj/CTFNodeRE.gpr, then:
#   G 0x400800 ; F   -> main (thunk to ctf_dispatch)
#   G 0x400960 ; F   -> ctf_crc32_le
#   G 0x4009b0 ; F   -> ctf_weak_key (defect B6)
#   G 0x400c20 ; F   -> ctf_dispatch (the subcommand dispatcher)
```

## Regenerate the reports

```bash
python3 resolve_functions.py    # -> RESOLUTION_MAP.md + resolution.json + resolved/
python3 gen_appendix_j.py       # -> ../CTF-XX-J-ghidra-function-resolution.md
```

## The four resolution rules

- **R1** exact address match against the unstripped twin (`../firmware/ctfnode.unstripped`)
- **R2** `.plt` stub -> `JUMP_SLOT` relocation -> import name
- **R3** the `.plt` PLT0 lazy resolver at `0x4006f0`
- **R4** phantom/overlapping function on alignment padding (`0x400adc`)

Read `RESOLUTION_MAP.md` after you have tried each function yourself. See
`../docs/33-ghidra-nation-state-re.md` for the full workflow.
