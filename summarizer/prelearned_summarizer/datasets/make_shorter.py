# for test purposes
with open("summarizer/prelearned_summarizer/datasets/trimmed.txt") as fin:
    with open("summarizer/prelearned_summarizer/datasets/trimmed2.txt", 'w') as fout:
        for i, line in enumerate(fin):
            if i >= 204951:
                break
            fout.write(line)
            fout.write("\n")
print("Done!")