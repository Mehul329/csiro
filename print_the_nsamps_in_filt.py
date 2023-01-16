from sigpyproc.readers import FilReader as F
import argparse, os

def main(args):
    outdir = "/scratch1/aga017/output/"
    infile = args.f
    infile = infile.strip().split("/")
    outname = outdir + infile[-5] + "_" + infile[-2] + "_" + infile[-1][:-3] + "cand"
    f = F(args.f)
    nsamps = f.header.nsamples

    with open(outname, 'w') as t:
        t.write(f"Nsamples in {args.f} are {nsamps}")


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument("-f", type=str, help="Path to the filterbank")
    args = a.parse_args()
    main(args)

