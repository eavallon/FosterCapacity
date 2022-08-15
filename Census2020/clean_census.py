import pandas as pd
import sys
import argparse

def main(infile, moe=True):
    """Cleans US census data into a format that can be read by Tableau.

    Params:
        infile: String. Path to raw census file in .csv format. .
        moe: Boolean. True if file includes margin of error.
    Returns:
        None
    """
    df = pd.read_csv(infile)

    if moe == True:
        df.columns = df.columns.str.replace("Total:!!", "")
        df.columns = df.columns.str.replace(":!!", " ")
        df.columns = df.columns.str.replace(":", " ")
        df = df.rename(columns={"Label (Grouping)": "Zip Code"})
        df = df.replace("ZCTA5 ", "", regex=True)
        df = df.replace("±", "", regex=True)

        df_err = df.copy()

        for index, row in df.iterrows():
            if index == len(df) - 3:
                df.iloc[index][1:] = df.iloc[index + 1][1:]
                df_err.iloc[index][1:] = df_err.iloc[index + 2][1:]
                break
            else:
                df.iloc[index][1:] = df.iloc[index + 1][1:]
                df_err.iloc[index][1:] = df_err.iloc[index + 2][1:]

        drop_idx = [i for i in range(1, len(df), 3)]
        drop_idx_err = [i for i in range(2, len(df), 3)]
        df = df.drop(drop_idx + drop_idx_err)
        df_err = df_err.drop(drop_idx + drop_idx_err)

        outfile = infile + "_clean.csv"
        outfile_err = infile + "_err_clean.csv"
        df.to_csv(outfile)
        df_err.to_csv(outfile_err)
        print(outfile)
        print(outfile_err)

    else:
        df.columns = df.columns.str.replace("Total:!!","")
        df.columns = df.columns.str.replace(":!!"," ")
        df.columns = df.columns.str.replace(":"," ")
        df = df.rename(columns={"Label (Grouping)": "Zip Code"})
        df = df.replace("ZCTA5 ","",regex=True)

        for index, row in df.iterrows():
            if index == len(df) - 2:
                df.iloc[index][1:] = df.iloc[index + 1][1:]
                break
            else:
                df.iloc[index][1:] = df.iloc[index + 1][1:]

        drop_idx = [i for i in range(1, len(df), 2)]
        df = df.drop(drop_idx)

        outfile = infile.split('.')[0] + "_clean.csv"
        df.to_csv(outfile)

if __name__== "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--infile", type = str, required=True)
    parser.add_argument("--moe", type = bool, required=False)

    args = parser.parse_args()

    if args.moe:
        infile = args.infile
        moe = args.moe
        main(infile, moe)

    else:
        infile = args.infile
        main(infile)

