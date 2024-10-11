#!/usr/bin/env python
import os
from pathlib import Path

import automol
import click


@click.command()
@click.argument("xyz_path")
@click.option("-r", "--rxn_path", default=None, help="Path to a zmat.r.yaml file")
@click.option(
    "-o", "--out_path", default="geom.zmat", help="Path to z-matrix output file"
)
def main(xyz_path: str, rxn_path: str = None, out_path: str = "geom.zmat"):
    geo = automol.geom.from_xyz_string(Path(xyz_path).read_text())
    if rxn_path is None:
        zma = automol.geom.zmatrix(geo)
        write_zmatrix(zma, out_path)
        return

    rxn = automol.reac.from_string(Path(rxn_path).read_text())
    grxn = automol.reac.with_structures(rxn, struc_typ="geom")
    grxn = automol.reac.update_structures(grxn, ts_struc=geo)
    zrxn = automol.reac.with_structures(grxn, struc_typ="zmat")
    zma = automol.reac.ts_structure(zrxn)
    write_zmatrix(zma, out_path)


def write_zmatrix(zma: object, out_path: str) -> None:
    """Write a z-matrix to a file

    :param zma: Z-matrix
    :param out_path: File path to write to
    """
    zma_str = automol.zmat.string(zma, one_indexed=True)
    Path(out_path).write_text(zma_str)


if __name__ == "__main__":
    os.chdir(os.environ.get("INIT_CWD", "."))
    main()
