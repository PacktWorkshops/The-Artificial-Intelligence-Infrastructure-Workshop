BEGIN {
    FPAT = "([^,]+)|(\"[^\"]+\")"
}

{
    gsub(",,", ", ,")
    print "NF = " NF
    for (i = 1; i <= NF; i++) {

        if (substr($i, 1, 1) == "\"") {
            len = length($i)
            $i = substr($i, 2, len - 2)    # Get text within the two quotes
        }

        printf("#%d = %s\n", i, $i)
    }
}
