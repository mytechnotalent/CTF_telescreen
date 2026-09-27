#!/usr/bin/env python3
"""Generate Appendix J: the function-by-function reverse-engineering report.

For every application function in the stripped TELESCREEN target this writes:

  * its address and the meaningless name Ghidra shows for it,
  * what it really is (module + role),
  * the machine-disassembly call graph around it (who calls it / it calls),
  * the exact evidence that resolves it, and
  * its decompiled C body.

Nothing here is guessed: the call graph comes from `objdump -d` of the
unstripped twin, and every address is matched 1:1 against `nm`.
"""
from __future__ import annotations

import re
from pathlib import Path

import resolve_functions as rf

HERE = rf.HERE
GT = rf.GT
OUT = HERE.parent / "CTF-XX-J-ghidra-function-resolution.md"


def load_disasm():
    """Return (funcs_by_addr, calls) parsed from ground_truth/disasm.txt.

    Both `bl` (call) and unconditional `b` (tail call) are captured, because the
    compiler emits tail calls for many of the dispatcher's edges.  Conditional
    branches (`b.eq`, `b.ne`, ...) are excluded by requiring whitespace after the
    mnemonic.
    """
    funcs: dict[int, str] = {}
    calls: list[tuple[int, int]] = []
    cur = None
    fn_re = re.compile(r"^([0-9a-f]{16}) <(.+)>:")
    br_re = re.compile(r"(?:^|\s)(bl?)\s+([0-9a-f]+) <")
    for line in (GT / "disasm.txt").read_text().splitlines():
        m = fn_re.match(line)
        if m:
            cur = int(m.group(1), 16)
            funcs[cur] = m.group(2)
            continue
        m = br_re.search(line)
        if m and cur is not None:
            calls.append((cur, int(m.group(2), 16)))
    # Keep only edges into a real function/symbol start; drop tail branches to
    # internal basic blocks (objdump prints those as `<func+0x..>`).
    return funcs, [(a, b) for a, b in calls if b in funcs]


def main() -> None:
    symbols = rf.load_symbols()
    sources = rf.parse_sources()
    funcs, calls = load_disasm()

    name_of: dict[int, str] = {}
    for addr, (typ, name) in symbols.items():
        name_of[addr] = name
    for addr, raw in funcs.items():
        if addr not in name_of:
            name_of[addr] = raw

    callers: dict[int, set[int]] = {}
    callees: dict[int, set[int]] = {}
    for a, b in calls:
        callees.setdefault(a, set()).add(b)
        callers.setdefault(b, set()).add(a)

    def resolve_name(addr: int) -> str:
        return name_of.get(addr, f"sub_{addr:x}")

    rows = [r for r in rf.resolve() if r["kind"] == "application"]
    # Prefer the curated Doxygen briefs in resolution.json (the source of truth
    # for the roles), falling back to whatever the source parser found.
    import json
    curated = {r["addr"]: r.get("brief", "")
               for r in json.loads((rf.HERE / "resolution.json").read_text())}
    for r in rows:
        if not r.get("brief"):
            r["brief"] = curated.get(r["addr"], "")
    rows.sort(key=lambda r: r["addr"])

    out: list[str] = []
    w = out.append
    w("# Appendix J - Function-by-Function Reverse Engineering")
    w("")
    w("This appendix is the complete reverse-engineering record of the stripped")
    w("target `firmware/ctfnode.stripped`.  For every one of the 10 application")
    w("functions it gives the address, the meaningless label Ghidra shows, what")
    w("the function really is, the call graph around it extracted from the real")
    w("machine code, the evidence that resolves it, and its decompiled body.")
    w("")
    w("Everything here is reproducible from `firmware/ctfnode.stripped` alone plus")
    w("the instructor's `firmware/ctfnode.unstripped` answer key.")
    w("")
    w("> **The four resolution rules** (see `ghidra/RESOLUTION_MAP.md`):")
    w(">")
    w("> - **R1** exact address match against the unstripped twin (certain),")
    w("> - **R2** `.plt` stub -> `JUMP_SLOT` relocation -> import name (certain),")
    w("> - **R3** the `.plt` PLT0 lazy resolver (certain),")
    w("> - **R4** phantom/overlapping function on alignment padding (certain).")
    w("")
    w("---")
    w("")

    for r in rows:
        addr = r["addr"]
        name = r["name"]
        module = r["module"]
        brief = r.get("brief", "")
        w(f"## `0x{addr:08x}` - `{name}`  ({module})")
        w("")
        w(f"- **Ghidra shows:** `{r['ghidra']}` (a stripped binary has no names).")
        w(f"- **Resolved name:** `{name}`")
        w(f"- **Module:** `ctf/{module}.c`")
        w(f"- **Role:** {brief or '(see source)'}")
        w(f"- **Evidence:** {r['evidence']}.")
        if addr in callers:
            cs = ", ".join(f"`{resolve_name(c)}`" for c in sorted(callers[addr]))
            w(f"- **Called by ({len(callers[addr])}):** {cs}")
        else:
            w("- **Called by:** _(entry points only)_")
        if addr in callees:
            ce = ", ".join(f"`{resolve_name(c)}`" for c in sorted(callees[addr]))
            w(f"- **Calls ({len(callees[addr])}):** {ce}")
        else:
            w("- **Calls:** _(leaf function)_")
        w("")
        w("```c")
        body = (rf.RESOLVED / f"{addr:08x}_{re.sub(r'[^A-Za-z0-9_.-]', '_', name)}.c")
        if body.exists():
            w(body.read_text().rstrip())
        else:
            w((rf.DECOMP / r["file"]).read_text().rstrip())
        w("```")
        w("")

    # --- Lessons section -----------------------------------------------------
    w("---")
    w("")
    w("## Reverse-engineering lessons this binary teaches")
    w("")
    w("### Lesson 1 - Static helpers are inlined away")
    w("")
    w("The source has more functions than the compiled binary.  A student who")
    w("greps the stripped listing for a helper name will not find it, because the")
    w("compiler inlined every `static` one:")
    w("")
    w("- `ctf_crc32_byte` is inlined into both `ctf_crc32_le` and `ctf_weak_key`,")
    w("  so the reflected fold appears **twice** as straight-line machine code.")
    w("- `ctf_cmd`, `ctf_print_key`, `ctf_try_path`, and `ctf_try_misc` are inlined")
    w("  into `ctf_dispatch`, which is why the dispatcher is the largest function.")
    w("")
    w("Always read the call graph, not just the symbol count, before concluding a")
    w("function is missing.")
    w("")
    w("### Lesson 2 - Phantom functions on alignment padding")
    w("")
    w("Modern toolchains align functions to 16 bytes and pad with `nop`.  Ghidra")
    w("can mistake the padding for the start of a small function, producing a")
    w("phantom that overlaps the real one:")
    w("")
    w("- `0x00400adc` is a phantom whose body is identical to `ctf_config_run`")
    w("  (`0x00400ae0`) sitting on the 4-byte alignment pad.")
    w("")
    w("Always confirm a function's true entry with the call graph and the")
    w("prologue (`stp x29, x30, [sp, #-N]!`), never by Ghidra's guess alone.")
    w("")
    w("### Lesson 3 - The PLT and the GOT")
    w("")
    w("Every imported libc function is indirected through the `.plt`: the stub")
    w("loads a slot from `.got.plt` and branches to it (`br x17`).  The relocation")
    w("at `0x420000`-`0x420060` names the target, so `bl 0x400770` is `system`, not")
    w("some anonymous `FUN_`.  Reading the `.rela.plt` relocations is how a")
    w("reverse engineer recovers library calls from a stripped binary.")
    w("")
    out_text = "\n".join(out) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out_text)
    print(f"wrote {OUT} ({len(out_text.splitlines())} lines, {len(rows)} functions)")


if __name__ == "__main__":
    main()
